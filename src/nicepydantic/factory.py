from __future__ import annotations

from typing import Any, Callable, Literal, cast, get_args, get_origin

from nicegui import ui
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .form import PydanticForm


class FieldUI:
    def __init__(self, field: FieldInfo) -> None:
        self.field = field

    def build(self) -> ui.element:
        raise NotImplementedError


def default_field_factory(field: FieldInfo) -> ui.element:
    if get_origin(field.annotation) is list:
        return ListFieldUI(field).build()
    if get_origin(field.annotation) is Literal:
        return LiteralFieldUI(field).build()
    if isinstance(field.annotation, type) and issubclass(field.annotation, BaseModel):
        return BaseModelFieldUI(field).build()
    if field.annotation is str:
        return StrFieldUI(field).build()
    if field.annotation is int or field.annotation is float:
        return NumberFieldUI(field).build()
    if field.annotation is bool:
        return BoolFieldUI(field).build()
    return ui.label(f"Unsupported type: {field.annotation}")


class BaseModelFieldUI(FieldUI):
    def build(self) -> PydanticForm:
        model_class = cast(type[BaseModel], self.field.annotation)
        return PydanticForm(value=model_class())


class ListFieldUI(FieldUI):
    def build(self) -> ui.element:
        with ui.card() as card:
            ui.label(self.field.title or "")
            self.list_container = ui.column()

            # Get the type of the items in the list
            item_type = get_args(self.field.annotation)[0]

            # Create a dummy FieldInfo for the item type
            item_field = FieldInfo(annotation=item_type)

            def add_item(value: Any | None = None) -> None:
                with self.list_container:
                    with ui.row() as row:
                        element = default_field_factory(item_field)
                        if value and hasattr(element, "set_value"):
                            cast(Any, element).set_value(value)
                        ui.button("Remove", on_click=lambda: self.list_container.remove(row))

            ui.button("Add", on_click=lambda: add_item())

        return card


class LiteralFieldUI(FieldUI):
    def build(self) -> ui.select:
        return ui.select(
            label=self.field.title or "",
            options=list(get_args(self.field.annotation)),
        )


class StrFieldUI(FieldUI):
    def build(self) -> ui.input:
        return ui.input(label=self.field.title or "")


class NumberFieldUI(FieldUI):
    def build(self) -> ui.number:
        return ui.number(label=self.field.title or "")


class BoolFieldUI(FieldUI):
    def build(self) -> ui.switch:
        return ui.switch(text=self.field.title or "")
