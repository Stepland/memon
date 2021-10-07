import json
from jschon import create_catalog, JSONSchema

def test_that_the_schema_follows_the_metaschema():
    catalog_2019_09 = create_catalog("2019-09", default=True)
    with open("schema.json") as file:
        raw = json.load(file)
    schema = JSONSchema(raw, catalog=catalog_2019_09)
    schema.validate()

