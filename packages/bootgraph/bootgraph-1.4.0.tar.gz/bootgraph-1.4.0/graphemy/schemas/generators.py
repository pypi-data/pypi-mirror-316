from datetime import date
from typing import (
    TYPE_CHECKING,
    Annotated,
    Callable,
    Dict,
    Optional,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin, Type,
)

from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKeyConstraint, func
from sqlalchemy.inspection import inspect
from strawberry.tools import merge_types
from strawberry.types.field import StrawberryField

from ..database.operations import delete_item, get_items, put_item
from ..dl import Dl, ManyRelation

if TYPE_CHECKING:
    from ..models import Graphemy

T = TypeVar("T")

class GraphemyFilterMode:
    EXACT = "EXACT"
    CONTAINS = "CONTAINS"
    STARTSWITH = "STARTSWITH"
    ENDSWITH = "ENDSWITH"


def set_schema(
        cls: "Graphemy",
        functions: Dict[str, Tuple[Callable, "Graphemy"]],
        auto_foreign_keys,
) -> None:
    """Set the Strawberry schema for a Graphemy class."""

    # Define a class to hold Strawberry schema fields
    class Schema:
        pass

    foreign_keys_info = []
    for attr in [attr for attr in cls.__dict__.values() if hasattr(attr, "dl")]:
        returned_class: "Graphemy" = Setup.classes[attr.dl]
        setattr(
            Schema,
            attr.__name__,
            strawberry.field(
                attr,
                permission_classes=[
                    Setup.get_auth(
                        returned_class,
                        "query",
                    )
                ],
            ),
        )
        if attr.foreign_key or (
                attr.foreign_key == None and auto_foreign_keys and not attr.many
        ):
            source = attr.source if isinstance(attr.source, list) else [attr.source]
            target = attr.target if isinstance(attr.target, list) else [attr.target]
            target = [returned_class.__tablename__ + "." + t for t in target]

            if (
                    len(source) > 0
                    and len(target) > 0
                    and not any(
                isinstance(item, int)
                or (isinstance(item, str) and item.startswith("_"))
                for item in source + target
            )
            ):
                cls.__table__.append_constraint(ForeignKeyConstraint(source, target))
                foreign_keys_info.append((source, target))
        if not attr.dl_name in functions:
            functions[attr.dl_name] = (
                get_dl_field(attr, returned_class),
                returned_class,
            )
    if cls.__custom_resolvers__:
        for custom_resolver in cls.__custom_resolvers__:
            setattr(Schema, custom_resolver.__name__, strawberry.field(
                resolver=custom_resolver
            ))

    if not cls.__strawberry_schema__:
        extra_schema = strawberry.type(cls.Strawberry, name=f"{cls.__name__}Schema2")
        strawberry_schema = strawberry.experimental.pydantic.type(
            cls, all_fields=True, name=f"{cls.__name__}Schema"
        )(Schema)
        if extra_schema.__annotations__:
            strawberry_schema = merge_types(
                f"{cls.__name__}Schema", (strawberry_schema, extra_schema)
            )
        cls.__strawberry_schema__ = strawberry_schema


def get_dl_field(attr, returned_class: "Graphemy") -> callable:
    returned_schema = returned_class.__strawberry_schema__
    if attr.many:
        returned_schema = list[returned_schema]
    else:
        returned_schema = Optional[returned_schema]

    async def dataloader(
            keys: list[tuple],
    ) -> returned_schema:
        return await get_items(returned_class, keys, attr.target, attr.many)

    dataloader.__name__ = attr.dl_name
    return dataloader

def get_many_relation_function(
        field_name: str,
        field_type: T,
        field_value: ManyRelation,
        source_model: Type["Graphemy"]
) -> Callable[[], Union["Graphemy", list["Graphemy"]]]:
    """Generates a DataLoader function dynamically based on the field's specifications."""
    # Determine if the field_type is a list and extract the inner type
    is_list = get_origin(field_type) == list
    class_type = get_args(field_type)[0] if is_list else field_type

    cls = field_value.response_class

    # return get_query()

    # Formulate DataLoader name with consideration for lazy-loaded types
    dl_name = (
        field_value.target
        if isinstance(field_value.target, str)
        else "_".join(field_value.target)
    )
    dl_name = f"dl_{class_type}_{dl_name}"

    # Define the return type using Strawberry's lazy type resolution
    return_type = Annotated[
        f"{class_type}Schema",
        strawberry.lazy("graphemy.router"),
    ]
    if is_list:
        return_type = CountableConnection[return_type]
    else:
        raise Exception("ManyRelation can not resolve one")


    async def loader_func(
            self,
            info: "Info",
            first: Optional[int] = None,
            after: Optional[str] = None,
            last: Optional[int] = None,
            before: Optional[str] = None,
            filters: (
                    Annotated[
                        f"{class_type}Filter",
                        strawberry.lazy("graphemy.router"),
                    ]
                    | None
            ) = None,
            orderBy: Optional[str] = None,
    ) -> return_type:
        # Check permissions asynchronously
        if not await Setup.has_permission(cls, info.context, "query"):
            # Return empty connection if no permission
            return convert_to_countable_connection([], first, after, last, before, return_type)

        # Obtain the engine for this model
        engine = Setup.engine[cls.__enginename__]

        relation_class = field_value.relation_class
        source_field = getattr(source_model, field_value.source)  # e.g., Shop.id
        source_relation_field = getattr(relation_class, field_value.source_relation)  # e.g., ReviewShop.shop_id
        target_field = getattr(cls, field_value.target)  # e.g., Review.id
        target_relation_field = getattr(relation_class, field_value.target_relation)  # e.g., Review.review_id

        # We have three models
        # cls - Review with id field
        # source_model - Shop which has field_value.source (e.g., id field)
        # relation_class - ReviewShop which has field_value.target (e.g., shop_id and review_id)

        source_value = (
            [
                (
                    attr
                    if type(attr) == int
                    else attr[1:] if attr.startswith("_") else getattr(self, attr)
                )
                for attr in field_value.source
            ]
            if isinstance(field_value.source, list)
            else getattr(self, field_value.source)
        )

        stmt = (
            select(cls)
            .join(relation_class, target_relation_field == target_field)
            .join(source_model, source_field == source_relation_field)
            .filter(source_field == source_value)
        )
        count_stmt = (select(func.count())
            .join(relation_class, target_relation_field == target_field)
            .join(source_model, source_field == source_relation_field)
            .filter(source_field == source_value).select_from(cls))

        # Apply filters if provided
        if filters:
            filter_conditions = [
                getattr(cls, k) == v
                for k, v in vars(filters).items()
                if v is not None
            ]
            count_stmt = count_stmt.filter(*filter_conditions)
            stmt = stmt.filter(*filter_conditions)

        # Apply any additional query filters defined by Setup
        qf = Setup.query_filter(cls, info.context)
        if qf and callable(qf):
            stmt = qf(stmt)
            count_stmt = qf(count_stmt)

        # Determine ordering
        # Assume `orderBy` is the name of a column in `cls`. If not provided, default to primary key.
        order_column = getattr(cls, orderBy) if orderBy else getattr(cls, "id")
        stmt = stmt.order_by(order_column.asc())

        # Handle pagination cursors: decode them and apply filters
        # We assume the cursors are encoded in a way that allows retrieval of the order_column value.
        # decode_cursor returns something like: {"order_value": ..., "id": ...}
        after_value = decode_cursor(after) if after else None
        before_value = decode_cursor(before) if before else None

        # Apply 'after' cursor filter: we want all rows strictly greater than the after_value
        if after_value is not None:
            # TODO: if we need more filters, we need to prccess them here
            after_cursor_value = after_value["o"]
            stmt = stmt.filter(order_column > after_cursor_value)

        # Apply 'before' cursor filter: we want all rows strictly less than the before_value
        if before_value is not None:
            before_cursor_value = before_value["o"]
            stmt = stmt.filter(order_column < before_cursor_value)

        # Apply limit based on `first` or `last`
        # If using forward pagination:
        if first is not None:
            stmt = stmt.limit(first + 1)  # Fetch one extra to determine if there's a next page

        # If using backward pagination (via `last`), you may need to reverse the order, fetch `last + 1` items,
        # then reverse results in memory. For simplicity:
        # If last is used, re-order descending, limit last + 1, then post-process.
        # This is a simplistic approach; a robust approach requires careful logic.
        if last is not None and before is not None:
            stmt = stmt.order_by(order_column.desc()).limit(last + 1)

        # Execute query depending on sync or async engine
        if Setup.async_engine:
            async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            async with async_session() as session:
                total_count = (await session.execute(count_stmt)).scalar()
                results = (await session.execute(stmt)).scalars().all()
        else:
            with Session(engine) as session:
                total_count = session.execute(count_stmt).scalar()
                results = session.execute(stmt).scalars().all()

        # If last pagination was requested, reverse the results back to original order
        # (because we fetched them in descending order)
        if last is not None and before is not None:
            results = list(reversed(results))
        print(results) # Here are the same Review(text='The first ever shop', rating=3, id=1) multiplied by count, why?
        # Convert results to a countable connection structure
        # `convert_to_countable_connection` should handle encoding the cursors for next and previous pages.
        connection = convert_to_countable_connection(
            results,
            first,
            after,
            last,
            before,
            return_type,
            order_column=order_column,
            filters=filters,
            total_count=total_count
        )

        return connection

    # Customize the function attributes for introspection or other purposes
    loader_func.__name__ = field_name
    loader_func.dl = class_type
    loader_func.many = is_list
    loader_func.target = field_value.target
    loader_func.source = field_value.source
    loader_func.foreign_key = field_value.foreign_key
    loader_func.dl_name = dl_name

    return loader_func


def get_dl_function(
        field_name: str,
        field_type: T,
        field_value: Dl,
) -> Callable[[], Union["Graphemy", list["Graphemy"]]]:
    """Generates a DataLoader function dynamically based on the field's specifications."""
    # Determine if the field_type is a list and extract the inner type
    is_list = get_origin(field_type) == list
    class_type = get_args(field_type)[0] if is_list else field_type

    # Formulate DataLoader name with consideration for lazy-loaded types
    dl_name = (
        field_value.target
        if isinstance(field_value.target, str)
        else "_".join(field_value.target)
    )
    dl_name = f"dl_{class_type}_{dl_name}"

    # Define the return type using Strawberry's lazy type resolution
    return_type = Annotated[
        f"{class_type}Schema",
        strawberry.lazy("graphemy.router"),
    ]
    if is_list:
        return_type = list[return_type]
    else:
        return_type = Optional[return_type]

    async def loader_func(
        self,
        info: Info,
        filters: (
            Annotated[
                f"{class_type}Filter",
                strawberry.lazy("graphemy.router"),
            ]
            | None
        ) = None,
    ) -> return_type:
        """The dynamically generated DataLoader function."""
        filter_args = vars(filters) if filters else None
        source_value = (
            [
                (
                    attr
                    if type(attr) == int
                    else attr[1:] if attr.startswith("_") else getattr(self, attr)
                )
                for attr in field_value.source
            ]
            if isinstance(field_value.source, list)
            else getattr(self, field_value.source)
        )
        return await info.context[dl_name].load(source_value, {"filters": filter_args})

    # Customize the function attributes for introspection or other purposes
    loader_func.__name__ = field_name
    loader_func.dl = class_type
    loader_func.many = is_list
    loader_func.target = field_value.target
    loader_func.source = field_value.source
    loader_func.foreign_key = field_value.foreign_key
    loader_func.dl_name = dl_name

    return loader_func


from typing import Optional, List, Any, Dict, Type
from sqlalchemy.orm import Session
import strawberry
from strawberry.types import Info
from sqlmodel import SQLModel, select
from ..setup import Setup


# ----------------------------------------
# Placeholder Implementations
# ----------------------------------------

def get_one(cls: Type[SQLModel], filter_obj: Any, query_filter: callable = None):
    """
    Retrieve a single item from the database according to the fields in `filter_obj`.
    We assume `filter_obj` is a dict of {field_name: value} pairs for filtering.
    """
    session: Session = Setup.get_session(cls)
    stmt = select(cls)

    # Apply filters from filter_obj if provided
    if filter_obj:
        filter_dict = {k: v for k, v in vars(filter_obj).items() if v is not None}
        stmt = stmt.filter_by(**filter_dict)

    # Apply additional query_filter if provided
    if query_filter:
        stmt = query_filter(stmt)

    return session.execute(stmt).scalars().first()


import json
import base64


def encode_cursor(order_value: Any, unique_id: Any) -> str:
    # Encodes a dict into a base64 JSON string.
    # Structure: { "o": order_value, "id": unique_id }
    data = {"o": order_value, "id": unique_id}
    json_str = json.dumps(data)
    return base64.b64encode(json_str.encode("utf-8")).decode("utf-8")


def decode_cursor(cursor: Optional[str]) -> Optional[Dict[str, Any]]:
    if cursor is None:
        return None
    try:
        decoded = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
        data = json.loads(decoded)
        # data should contain { "o": order_value, "id": unique_id }
        return data
    except (ValueError, json.JSONDecodeError):
        # If cursor is invalid, return None or raise an error
        return None


def convert_to_countable_connection(
        results: List[Any],
        first: Optional[int],
        after: Optional[str],
        last: Optional[int],
        before: Optional[str],
        ConnectionClass: Type[Any],
        *,
        order_column: Any,
        filters: Any = None,
        total_count: Optional[int] = None
) -> Any:
    """
    Convert a list of ORM results into a countable connection structure.
    Assumes that `results` has already been fetched with any extra items included
    (one extra item to determine next/previous pages).

    Arguments:
    - results: The fetched list of items (could include one extra for pagination).
    - first, after, last, before: Relay-style pagination arguments.
    - ConnectionClass: The GraphQL connection class to instantiate.
    - order_column: The column used for ordering (e.g., cls.id).
    - filters: Filter conditions used, if needed to reconstruct the context.
    - total_count: If not provided, must be fetched separately. For demonstration,
      assume it's passed in or can be computed here.

    Returns:
    A `ConnectionClass` instance with `edges`, `pageInfo`, and `totalCount`.
    """

    # If total_count not provided, you would need to run a count query here.
    if total_count is None:
        # This is pseudo-logic. In reality, you'd need your model/class context
        # and filters to compute this. For now, assume total_count == len(results)
        # or do a proper COUNT query if you have the session and model class.
        total_count = len(results)

    # Determine if we fetched an extra item for pagination detection.
    extra_fetched = 0
    if first is not None:
        # If we wanted first items, we might have fetched first + 1
        if len(results) > first:
            extra_fetched = len(results) - first
    if last is not None:
        # Similarly, if we wanted last items, we might have fetched last + 1 in reverse.
        if len(results) > last:
            extra_fetched = len(results) - last

    # Adjust results to remove the extra item(s)
    edges_results = results
    if extra_fetched > 0:
        if first is not None:
            # For forward pagination, we keep the first 'first' items
            edges_results = results[:first]
        elif last is not None:
            # For backward pagination, we keep the last 'last' items
            edges_results = results[-last:]

    # Create edges: each edge needs a cursor.
    # We assume each result has a primary key `id` and we used `order_column` for ordering.
    edges = []

    @strawberry.type
    class EdgeClass:
        node: Any
        cursor: str

    for node in edges_results:
        # Extract order_value from the node. If order_column is a column object, access node attribute.
        order_value = getattr(node, order_column.key) if hasattr(order_column, 'key') else getattr(node,
                                                                                                   str(order_column))
        unique_id = getattr(node, "id", None)  # Assuming 'id' is the primary key
        cursor = encode_cursor(order_value, unique_id)
        # edges.append({"node": node, "cursor": cursor})
        edges.append(EdgeClass(node=node, cursor=cursor))

    # Compute pageInfo
    has_next_page = False
    has_previous_page = False

    # Logic for hasNextPage and hasPreviousPage:
    # If we had a limit (first), and we got one extra item initially (not shown in edges_results after trimming),
    # that indicates there is a next page.
    if first is not None and len(results) > first:
        has_next_page = True

    # If we had a limit (last), and we got one extra item initially,
    # that indicates there is a previous page.
    if last is not None and len(results) > last:
        has_previous_page = True

    # If no pagination arguments but total_count > len(edges_results),
    # we could deduce future pages exist. That depends on your logic.
    # For simplicity, rely on the extra item logic above.

    # startCursor and endCursor come from the first and last edges
    start_cursor = edges[0].cursor if edges else None
    end_cursor = edges[-1].cursor if edges else None

    page_info = {
        "hasNextPage": has_next_page,
        "hasPreviousPage": has_previous_page,
        "startCursor": start_cursor,
        "endCursor": end_cursor,
    }

    # Instantiate the connection object. The exact initialization depends on your schema.
    # Assume `CountableConnectionForModel` or `ConnectionClass` takes edges, pageInfo, totalCount.
    connection = ConnectionClass(
        edges=edges,
        pageInfo=page_info,
        totalCount=total_count
    )

    return connection


def create_filter_input(cls: Type[SQLModel], name_suffix="Filter"):
    """
    Dynamically create a Strawberry input type from the __annotations__ of the SQLModel class.
    All fields are optional, allowing flexible filtering.
    """
    declared_filters = getattr(cls, "__filter_attributes__", {})
    if not declared_filters:
        return None

    class FilterInput:
        pass

    for field_name, field_type in cls.__annotations__.items():
        if field_name in declared_filters:
            if declared_filters[field_name].get("required"):
                graphql_type = field_type
            else:
                graphql_type = Optional[field_type]
            setattr(
                FilterInput,
                field_name,
                strawberry.field(
                    default=declared_filters[field_name].get("default"), graphql_type=graphql_type,
                    description=declared_filters[field_name].get("description"),
                ),
            )
    return strawberry.input(name=f"{cls.__name__}{name_suffix}")(FilterInput)


from typing import Generic, TypeVar, List, Optional
import strawberry

# Type variable for node type
T = TypeVar("T")


@strawberry.type
class PageInfo:
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: Optional[str]
    endCursor: Optional[str]


@strawberry.type
class Edge(Generic[T]):
    node: T
    cursor: str


@strawberry.type
class CountableConnection(Generic[T]):
    edges: List[Edge[T]]
    pageInfo: PageInfo
    totalCount: int


# ----------------------------------------
# Integration with the refactored get_query code
# ----------------------------------------

def get_query(cls: "Graphemy"):
    # Create the filter input types
    # One-type filters (for unique lookups) might be the same as many filters, or separate if needed.
    # Here we assume one and many queries can use the same filter input.
    Filter = create_filter_input(cls, "Filter")

    async def one_resolver(self, info: Info, filter: Filter) -> Optional[cls.__strawberry_schema__]:
        if not await Setup.has_permission(cls, info.context, "query"):
            return None
        data = get_one(cls, filter, Setup.query_filter(cls, info.context))
        return data

    CountableConnectionForModel = CountableConnection[cls.__strawberry_schema__]

    async def many_resolver(
            self,
            info: "Info",
            first: Optional[int] = None,
            after: Optional[str] = None,
            last: Optional[int] = None,
            before: Optional[str] = None,
            filter: Optional[Filter] = None,
            orderBy: Optional[str] = None,
    ) -> CountableConnectionForModel:
        # Check permissions asynchronously
        if not await Setup.has_permission(cls, info.context, "query"):
            # Return empty connection if no permission
            return convert_to_countable_connection([], first, after, last, before, CountableConnectionForModel)

        # Obtain the engine for this model
        engine = Setup.engine[cls.__enginename__]

        # Prepare the base select statement
        stmt = select(cls)

        declared_filters = getattr(cls, "__filter_attributes__", {})
        # Apply filters if provided
        if filter:
            for k, v in vars(filter).items():
                if v is None or k not in declared_filters:
                    continue
                column = getattr(cls, k)
                mode = declared_filters[k].get("mode", GraphemyFilterMode.EXACT)
                if mode == GraphemyFilterMode.EXACT:
                    stmt = stmt.filter(column.ilike(v))
                elif mode == GraphemyFilterMode.CONTAINS:
                    stmt = stmt.filter(column.ilike(f"%{v}%"))
                elif mode == GraphemyFilterMode.STARTSWITH:
                    stmt = stmt.filter(column.ilike(f"{v}%"))
                elif mode == GraphemyFilterMode.ENDSWITH:
                    stmt = stmt.filter(column.ilike(f"%{v}"))

        # Apply any additional query filters defined by Setup
        qf = Setup.query_filter(cls, info.context)
        if qf and callable(qf):
            stmt = qf(stmt)

        # Determine ordering
        # Assume `orderBy` is the name of a column in `cls`. If not provided, default to primary key.
        order_column = getattr(cls, orderBy) if orderBy else getattr(cls, "id")
        stmt = stmt.order_by(order_column.asc())

        # Handle pagination cursors: decode them and apply filters
        # We assume the cursors are encoded in a way that allows retrieval of the order_column value.
        # decode_cursor returns something like: {"order_value": ..., "id": ...}
        after_value = decode_cursor(after) if after else None
        before_value = decode_cursor(before) if before else None

        # Apply 'after' cursor filter: we want all rows strictly greater than the after_value
        if after_value is not None:
            # TODO: if we need more filters, we need to prccess them here
            after_cursor_value = after_value["o"]
            stmt = stmt.filter(order_column > after_cursor_value)

        # Apply 'before' cursor filter: we want all rows strictly less than the before_value
        if before_value is not None:
            before_cursor_value = before_value["o"]
            stmt = stmt.filter(order_column < before_cursor_value)

        # Apply limit based on `first` or `last`
        # If using forward pagination:
        if first is not None:
            stmt = stmt.limit(first + 1)  # Fetch one extra to determine if there's a next page

        # If using backward pagination (via `last`), you may need to reverse the order, fetch `last + 1` items,
        # then reverse results in memory. For simplicity:
        # If last is used, re-order descending, limit last + 1, then post-process.
        # This is a simplistic approach; a robust approach requires careful logic.
        if last is not None and before is not None:
            stmt = stmt.order_by(order_column.desc()).limit(last + 1)

        # Execute query depending on sync or async engine
        if Setup.async_engine:
            async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            async with async_session() as session:
                results = (await session.execute(stmt)).scalars().all()
        else:
            with Session(engine) as session:
                results = session.execute(stmt).scalars().all()

        # If last pagination was requested, reverse the results back to original order
        # (because we fetched them in descending order)
        if last is not None and before is not None:
            results = list(reversed(results))

        # Convert results to a countable connection structure
        # `convert_to_countable_connection` should handle encoding the cursors for next and previous pages.
        connection = convert_to_countable_connection(results, first, after, last, before, CountableConnectionForModel,
                                                     order_column=order_column, filters=filter)

        return connection

    one_field = strawberry.field(permission_classes=[Setup.get_auth(cls, "query")])(one_resolver)
    many_field = strawberry.field(permission_classes=[Setup.get_auth(cls, "query")])(many_resolver)

    class ModelQuery:
        one = one_field
        many = many_field

    # Now apply strawberry.type after fields are assigned
    ModelQuery = strawberry.type(name=f"{cls.__name__}Query")(ModelQuery)

    return ModelQuery, Filter


def get_put_mutation(cls: "Graphemy") -> StrawberryField:
    pk = [pk.name for pk in inspect(cls).primary_key]

    class Filter:
        pass

    for field_name, field in cls.__annotations__.items():
        setattr(
            Filter,
            field_name,
            strawberry.field(default=None, graphql_type=Optional[field]),
        )
    input = strawberry.input(name=f"{cls.__name__}Input")(Filter)

    async def mutation(self, params: input) -> cls.__strawberry_schema__:
        return await put_item(cls, params, pk)

    return strawberry.mutation(
        mutation,
        permission_classes=[Setup.get_auth(cls, "mutation")],
    )


def get_delete_mutation(cls: "Graphemy") -> StrawberryField:
    pk = [pk.name for pk in inspect(cls).primary_key]

    class Filter:
        pass

    for field_name, field in cls.__annotations__.items():
        if field_name in pk:
            setattr(
                Filter,
                field_name,
                strawberry.field(default=None, graphql_type=Optional[field]),
            )
    input = strawberry.input(name=f"{cls.__name__}InputPk")(Filter)

    async def mutation(self, params: input) -> cls.__strawberry_schema__:
        return await delete_item(cls, params, pk)

    return strawberry.mutation(
        mutation,
        permission_classes=[Setup.get_auth(cls, "delete_mutation")],
    )


def create_input_type_for_put(cls: SQLModel):
    """
    Dynamically create a Strawberry input type for the PUT mutation.
    All fields from the model are optional for partial updates.
    """
    fields_dict = {}
    for field_name, field_type in cls.__annotations__.items():
        if get_origin(field_type) == Mapped:
            # Exclude types which can not be transformed to strawberry.input
            # Like sqlalchemy.orm.base.Mapped[typing.List[Any]]
            mapped_type = get_args(field_type)[0]  # Extract the inner type -> typing.List
            if get_origin(mapped_type) == list or get_origin(mapped_type) == List:
                continue
        fields_dict[field_name] = strawberry.field(default=None, graphql_type=Optional[field_type])

    InputType = strawberry.input(
        type(
            f"Put{cls.__name__}Input",
            (object,),
            fields_dict
        )
    )
    return InputType


def create_input_type_for_pk(cls: SQLModel, pk_fields):
    """
    Dynamically create a Strawberry input type that includes only primary key fields.
    Used for DELETE mutations or any operation needing to uniquely identify a record.
    """
    fields_dict = {}
    for field_name, field_type in cls.__annotations__.items():
        if field_name in pk_fields:
            fields_dict[field_name] = strawberry.field(default=None, graphql_type=Optional[field_type])

    PkInputType = strawberry.input(
        type(
            f"Delete{cls.__name__}InputPk",
            (object,),
            fields_dict
        )
    )
    return PkInputType


def get_put_mutation(cls: SQLModel):
    pk = [pk.name for pk in inspect(cls).primary_key]
    Input = create_input_type_for_put(cls)

    @strawberry.mutation(permission_classes=[Setup.get_auth(cls, "mutation")])
    async def putModel(self, info: Info, input: Input) -> cls.__strawberry_schema__:
        # Perform update/insert operation
        return await put_item(cls, input, pk)

    return putModel


def get_delete_mutation(cls: SQLModel):
    pk = [pk.name for pk in inspect(cls).primary_key]
    InputPk = create_input_type_for_pk(cls, pk)

    @strawberry.mutation(permission_classes=[Setup.get_auth(cls, "delete_mutation")])
    async def deleteModel(self, info: Info, input: InputPk) -> Optional[cls.__strawberry_schema__]:
        # Perform delete operation
        return await delete_item(cls, input, pk)

    return deleteModel


def get_mutations(cls: "Graphemy"):
    """
    Combine all model-specific mutations (put, delete) into a single ModelMutations type.
    If the model has put or delete enabled, add those fields.
    """
    fields = {}

    class ModelMutations:
        pass

    if cls.__enable_put_mutation__:
        fields["putModel"] = get_put_mutation(cls)
        setattr(
            ModelMutations,
            "put",
            get_put_mutation(cls),
        )

    if cls.__enable_delete_mutation__:
        fields["deleteModel"] = get_delete_mutation(cls)
        setattr(
            ModelMutations,
            "delete",
            get_delete_mutation(cls),
        )

    if cls.__custom_mutations__:
        for custom_mutation in cls.__custom_mutations__:
            setattr(ModelMutations, custom_mutation.__name__, strawberry.mutation(
                resolver=custom_mutation
            ))

    # If no mutations are enabled, return None
    if not fields:
        return None

    ModelMutations = strawberry.type(name=f"{cls.__name__}Mutations")(ModelMutations)
    return ModelMutations