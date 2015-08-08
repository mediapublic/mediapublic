from colander import MappingSchema, SchemaNode, String, drop

def create_validator(cls):
    class GenericSchema(MappingSchema):
        pass
