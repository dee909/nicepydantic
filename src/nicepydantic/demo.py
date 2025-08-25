from typing import Literal

from nicegui import ui
from pydantic import BaseModel, Field

from .form import PydanticForm


class SimpleModel(BaseModel):
    name: str = "bob"
    age: int = 42


class ComplexModel(BaseModel):
    is_student: bool = True
    department: Literal["HR", "Engineering", "Sales"] = "Sales"
    hobbies: list[str] = ["Pizza", "PS5", "Star Wars"]


class DeepModel(SimpleModel):
    boss: SimpleModel = SimpleModel(name="Her", age=-1)
    info: ComplexModel = ComplexModel()


ui.label("nicepydantic demo").classes("text-h2")

with ui.expansion("SimpleModel", value=True).classes("bg-slate-300"):
    PydanticForm(SimpleModel())

with ui.expansion("ComplexModel", value=True).classes("bg-slate-300"):
    PydanticForm(ComplexModel())

with ui.expansion("DeepModel", value=True).classes("bg-slate-300"):
    PydanticForm(DeepModel())


ui.run()
