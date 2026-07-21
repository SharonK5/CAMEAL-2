# kernel/bootstrap/tests/test_loader.py
import pytest

from kernel.bootstrap.loader import Loader
from kernel.bootstrap.exceptions import LoaderError


class DummyClass:
    pass


class TestLoader:
    def test_load_class(self):
        cls = Loader.load_class("kernel.bootstrap.tests.test_loader.DummyClass")
        assert cls is DummyClass

    def test_load_invalid_class(self):
        with pytest.raises(LoaderError):
            Loader.load_class("nonexistent.module.Class")

    def test_instantiate(self):
        obj = Loader.instantiate("kernel.bootstrap.tests.test_loader.DummyClass")
        assert isinstance(obj, DummyClass)
