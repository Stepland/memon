
import json
from functools import partial
from pathlib import Path
from typing import Any

import py.path
import pytest
from jschon import create_catalog, JSON, JSONSchema, Catalog

from .utils import raise_if_invalid, result_of


def pytest_collect_file(path: py.path.local, parent: pytest.Collector):
    fspath = Path(path)
    if fspath.name == "__init__.py" and fspath.parent.name == "data":
        return ExamplesFolder.from_parent(parent, name="data", fspath=path.dirpath())


class ExamplesFolder(pytest.Collector):
    def collect(self):
        path = Path(self.fspath)
        for thing in path.glob("*-*"):
            if thing.is_dir():
                yield ExampleSubfolder.from_parent(
                    self,
                    name=thing.name,
                    fspath=py.path.local(thing),
                )


class ExampleSubfolder(pytest.Collector):
    def collect(self):
        path = Path(self.fspath)
        for file in (path / "pass").glob("*.json"):
            yield ValidExample.from_parent(self, name=file.stem, path=file)
        
        for file in (path / "fail").glob("*.json"):
            yield InvalidExample.from_parent(self, name=file.stem, path=file)


class ItemWithPath(pytest.Item):
    def __init__(self, *a, path: Path, **kw):
        super().__init__(*a, **kw)
        self.path = path

    def reportinfo(self):
        return self.path, 0, "" 


class ValidExample(ItemWithPath):
    def runtest(self):
        raise_if_invalid(result_of(self.path))
    
    def repr_failure(self, excinfo):
        parent = self.getparent(ExampleSubfolder)
        return f"Example {parent.name}::{self.name} did not pass validation"


class InvalidExample(ItemWithPath):
    def runtest(self):
        with pytest.raises(RuntimeError):
            raise_if_invalid(result_of(self.path))

    def repr_failure(self, excinfo):
        parent = self.getparent(ExampleSubfolder)
        return f"Example {parent.name}::{self.name} passed validation but shouldn't"