from py2gsuite.utils.format import class2dict, class2str, dict2str


class DummyTestClass:
    def __init__(self):
        self.name = "Bob"
        self.age = 50


def test_class2str():
    c = DummyTestClass()
    out = class2str(c)
    out_format = class2str(c, format=True)
    assert out == "{'age': 50, 'name': 'Bob'}"
    assert out_format == "\n{'age': 50, 'name': 'Bob'}\n"


def test_class2dict():
    c = DummyTestClass()
    out = class2dict(c)
    assert isinstance(out, dict)
    assert out == {"age": 50, "name": "Bob"}


def test_dict2str():
    d = {"age": 50, "name": "Bob"}
    out = dict2str(d)
    out_format = dict2str(d, format=True)
    assert out == "{'age': 50, 'name': 'Bob'}"
    assert out_format == "\n{'age': 50, 'name': 'Bob'}\n"
