import colander
from colander import Mapping, SchemaNode, Schema
from cornice.schemas import CorniceSchema


_excludes = ('id', 'creation_datetime', 'modified_datetime')


def validator_from_model(model):
    validator = Schema(Mapping())
    for key, column in model.__table__.columns.items():
        if key in _excludes:
            # skip things like ID that won't be in the body
            continue
        missing = colander.required
        if column.nullable:
            missing = colander.drop
        validator.add(
            SchemaNode(
                sqla_to_colander_type(column.type),
                name=key,
                missing=missing,
                **sqla_kwargs(column.type)
            )
        )

    return CorniceSchema.from_colander(validator)


def method_exists(cls, name):
    return hasattr(cls, name) and callable(getattr(cls, name))


def valid_uuid(uuid_string):
    from uuid import UUID
    try:
        val = UUID(uuid_string, version=4)
    except:
        return False
    return val.hex == uuid_string


validator_mapping = {
    'UUIDType': colander.Regex(
        # giant gross UUID4 regex
        r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$',
        "Not a valid UUID"),
}


def sqla_kwargs(sql_type):
    v = validator_mapping.get(sql_type.__class__.__name__, None)
    if v is None:
        return {}
    return {'validator': v}


type_mapping = {
    'Text': colander.String(),
    'UUIDType': colander.String(),
    'UnicodeText': colander.String('utf-8'),
    'DateTime': colander.DateTime(),
    'JSONType': colander.Mapping(unknown='preserve'),
    'Boolean': colander.Boolean(),
}


def sqla_to_colander_type(sql_type):
    try:
        return type_mapping[sql_type.__class__.__name__]
    except KeyError:
        raise ValueError("Uhoh, we don't map type {}".format(repr(sql_type)))
