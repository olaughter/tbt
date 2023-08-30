import pytest

from tbt.loader import Loader


def test_loader_init():
    for type in ["source", "destination", "transform"]:
        loader = Loader(type)
        assert loader.meta_type_cls.ref == type

    with pytest.raises(ValueError):
        loader = Loader("invalid")


def test_loader_load_available():
    class Parent:
        pass

    class FirstChild(Parent):
        ref = "first_child"

    class SecondChild(Parent):
        ref = "second_child"

    children = Loader.load_available(None, Parent)
    assert len(children) == 2
    assert isinstance(children["first_child"](), FirstChild)
    assert isinstance(children["second_child"](), SecondChild)


def test_loader_step():
    assert Loader("source").step("from_file")().name == "FromFile"
    assert Loader("destination").step("to_stdout")().name == "ToStdout"
    assert Loader("transform").step("count_list")().name == "CountList"
