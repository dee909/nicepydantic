from typing import List, Literal

from nicegui import ui
from pydantic import BaseModel, Field

from src.nicepydantic.form import PydanticForm


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class Person(BaseModel):
    name: str = Field(title="Full Name")
    age: int = Field(title="Age")
    is_student: bool = Field(title="Is Student?")
    department: Literal["HR", "Engineering", "Sales"] = Field(title="Department")
    address: Address
    hobbies: List[str] = Field(title="Hobbies")


@ui.page("/")
def main():
    person = Person(
        name="Jules",
        age=42,
        is_student=False,
        department="Engineering",
        address=Address(street="123 Main St", city="Anytown", zip_code="12345"),
        hobbies=["reading", "coding", "hiking"],
    )

    with ui.row():
        form = PydanticForm(value=person)
        ui.button("Save", on_click=lambda: ui.notify(f"Saved: {form.value}"))


ui.run()
