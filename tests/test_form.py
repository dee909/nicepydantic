from typing import List, Literal

import pytest
from nicegui.testing import Screen
from pydantic import BaseModel, Field

from src.nicepydantic import PydanticForm


class SimpleModel(BaseModel):
    name: str
    age: int


def test_simple_form(screen: Screen):
    model = SimpleModel(name="test", age=10)

    with screen.app:
        form = PydanticForm(value=model)

    screen.open('/')

    # Check for input with label "Name"
    name_input = screen.find('Name')
    assert name_input.value == 'test'

    # Check for number input with label "Age"
    age_input = screen.find('Age')
    assert age_input.value == '10'


class ComplexModel(BaseModel):
    is_student: bool
    department: Literal["HR", "Engineering", "Sales"]
    hobbies: List[str]


def test_complex_form(screen: Screen):
    model = ComplexModel(is_student=True, department="Engineering", hobbies=["coding", "reading"])

    with screen.app:
        form = PydanticForm(value=model)

    screen.open('/')

    # Check for switch
    switch = screen.find('Is Student')
    assert switch.value is True

    # Check for select
    select = screen.find('Department')
    assert select.value == "Engineering"

    # Check for list
    list_card = screen.find('Hobbies')
    assert list_card is not None
