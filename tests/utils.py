import json
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Dict, Tuple, List

from jschon.jsonschema import Scope
from jschon import create_catalog, JSONSchema, JSON
import pytest

_catalog = create_catalog('2020-12')
SCHEMA = JSONSchema.loadf("schema.json", catalog=_catalog)

def prettify_path(json_path: str) -> str:
    """turns a JSONPath /that/looks/like/this into a.dotted.path.like.this"""
    split = json_path.split("/")
    return ".".join(split[1:])

def flatten_errors(scope: Scope) -> Dict[str, List[str]]:
    """Returns a (path -> errors) mapping of the leaf nodes
    of the detailed error output"""
    def iter_errors(d: dict) -> Iterator[Tuple[str, str]]:
        if 'error' in d:
            yield prettify_path(d['instanceLocation']), d['error']
        elif 'errors' in d:
            for error in d['errors']:
                yield from iter_errors(error)

    errors = defaultdict(list)
    for path, message in iter_errors(scope.output('detailed')):
        errors[path].append(message)

    return {
        key: value[0] if len(value) == 1 else value
        for key, value in errors.items()
    }

def raise_if_invalid(scope: Scope):
    __tracebackhide__ = True
    if not scope.valid:
        raise RuntimeError(flatten_errors(scope))

def result_of(path: Path) -> Scope:
    raw = json.loads(path.read_text())
    instance = JSON(raw)
    return SCHEMA.evaluate(instance)
