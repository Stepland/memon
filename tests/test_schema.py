import json
from jschon.catalogue import jsonschema_2019_09
from jschon.jsonschema import JSONSchema

def test_that_the_schema_follows_the_metaschema():
    jsonschema_2019_09.initialize()
    with open("schema.json") as file:
        raw = json.load(file)
    schema = JSONSchema(raw)
    schema.validate()

