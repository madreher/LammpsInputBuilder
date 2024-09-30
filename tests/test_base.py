import pytest

from lammpsinputbuilder.base import BaseObject

def test_base():
    obj = BaseObject()

    assert obj.to_dict() == {"id_name": "default_id"}

    obj2 = BaseObject("test")
    assert obj2.to_dict() == {"id_name": "test"}

    obj3 = BaseObject()
    obj3.from_dict({"id_name": "test2"}, version=0)
    assert obj3.to_dict() == {"id_name": "test2"}

    obj4 = BaseObject("test_4")
    obj4.validate_id()
    assert obj4.get_id_name() == "test_4"

    with pytest.raises(ValueError):
        obj5 = BaseObject("")
        del obj5

    with pytest.raises(ValueError):
        obj6 = BaseObject("*&^%$")
        del obj6
        