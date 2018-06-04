# coding: mixt

"""Ensure that complex proptypes are correctly validated."""

import pytest
from mixt import html
from mixt.pyxl.base import Base
from mixt.exceptions import PyxlException
from mixt.proptypes import NotProvided

from typing import *


class DummyBase(Base):
    def _to_list(self, l):
        pass


def test_simple_union():

    class Foo(DummyBase):
        class PropTypes:
            value: Union[float, int]

    assert (<Foo value={1} />.value) == 1
    assert (<Foo value={1.1} />.value) == 1.1

    with pytest.raises(PyxlException):
        <Foo value={"foo"} />

    with pytest.raises(PyxlException):
        <Foo value="foo" />

    with pytest.raises(PyxlException):
        <Foo value="1" />

    with pytest.raises(PyxlException):
        <Foo value=1 />

    with pytest.raises(PyxlException):
        <Foo value={None} />

    with pytest.raises(AttributeError):
        <Foo value={NotProvided} />.value


def test_user_class():

    class User: ...

    class Hero(User): ...

    class Animal: ...

    class Foo(DummyBase):
        class PropTypes:
            user: User

    user = User()
    hero = Hero()
    animal = Animal()

    assert (<Foo user={user} />.user) == user
    assert (<Foo user={hero} />.user) == hero

    with pytest.raises(PyxlException):
        <Foo user={animal} />

    with pytest.raises(PyxlException):
        <Foo user={None} />

    with pytest.raises(AttributeError):
        <Foo user={NotProvided} />.user

    with pytest.raises(PyxlException):
        <Foo user="john" />



def test_complex_union():

    class User: ...

    class Hero(User): ...

    class Animal: ...


    class Foo(DummyBase):
        class PropTypes:
            user: Union[User, str]

    user = User()
    hero = Hero()
    animal = Animal()

    assert (<Foo user={user} />.user) == user
    assert (<Foo user="john" />.user) == "john"
    assert (<Foo user={"john"} />.user) == "john"

    with pytest.raises(PyxlException):
        <Foo user={animal} />

    with pytest.raises(PyxlException):
        <Foo user={None} />

    with pytest.raises(AttributeError):
        <Foo user={NotProvided} />.user

    with pytest.raises(PyxlException):
        <Foo user={123} />


def test_data_and_aria_are_not_validated():
    el = <div data-string="foo" aria-number={123} data-complex={{'foo': 123}} />
    assert el.data_string == 'foo'
    assert el.aria_number == 123
    assert el.data_complex == {'foo': 123}

    assert str(el) == '<div data-string="foo" aria-number="123" data-complex="{\'foo\': 123}"></div>'
