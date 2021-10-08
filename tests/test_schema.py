from jschon import JSONSchema

from .utils import raise_if_invalid, SCHEMA

def test_that_the_schema_follows_the_metaschema():
    schema_validity = SCHEMA.validate()
    raise_if_invalid(schema_validity)
