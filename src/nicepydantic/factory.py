from __future__ import annotations

from typing import Any, Callable, Literal, cast, get_args, get_origin, TYPE_CHECKING

from nicegui import ui
from pydantic import BaseModel
from pydantic.fields import FieldInfo

if TYPE_CHECKING:
    from .form import PydanticForm


class FieldUI:

    def __init__(self, form: PydanticForm, name: str, field: FieldInfo) -> None:
        self.name = name
        self.form = form
        self.field = field
        self.value: Any | None = None

    def build(self) -> ui.element:
        raise NotImplementedError

    def form_clearing(self):
        pass

    def render_label(self):
        ui.label(self.name.replace("_", " ").title())

    def render_value(self, value: Any):
        self.value = value
        self.build()


def default_field_factory(form: PydanticForm, name: str, field: FieldInfo) -> FieldUI:
    if get_origin(field.annotation) is list:
        return ListFieldUI(form, name, field)
    if get_origin(field.annotation) is Literal:
        return LiteralFieldUI(form, name, field)
    if isinstance(field.annotation, type) and issubclass(field.annotation, BaseModel):
        return BaseModelFieldUI(form, name, field)
    if field.annotation is str:
        return StrFieldUI(form, name, field)
    if field.annotation is int or field.annotation is float:
        return NumberFieldUI(form, name, field)
    if field.annotation is bool:
        return BoolFieldUI(form, name, field)
    return UnknownFieldUI(form, name, field)


class UnknownFieldUI(FieldUI):
    def build(self) -> ui.label:
        return ui.label(f"Unsupported type: {self.field.annotation}")


class LiteralFieldUI(FieldUI):
    def build(self) -> ui.select:
        return ui.select(
            label=self.field.title or "",
            options=list(get_args(self.field.annotation)),
            value=self.value,
        )


class StrFieldUI(FieldUI):
    def build(self) -> ui.input:
        return ui.input(label=self.field.title or "", value=str(self.value))


class NumberFieldUI(FieldUI):
    def build(self) -> ui.number:
        return ui.number(label=self.field.title or "", value=self.value)


class BoolFieldUI(FieldUI):
    def build(self) -> ui.switch:
        return ui.switch(text=self.field.title or "", value=bool(self.value))


class BaseModelFieldUI(FieldUI):
    def build(self) -> PydanticForm:
        model_class = cast(type[BaseModel], self.field.annotation)
        assert isinstance(self.value, model_class)
        with ui.row():
            ui.space()
            self._form = self.form.__class__(value=self.value)


class ListFieldUI(FieldUI):
    def build(self) -> ui.element:
        with ui.card() as card:
            ui.label(self.field.title or "")
            self.list_container = ui.column()

            # Get the type of the items in the list
            item_type = get_args(self.field.annotation)[0]

            # Create a dummy FieldInfo for the item type
            item_field = FieldInfo(annotation=item_type)

            for i, item in enumerate(self.value):
                field_ui = self.form._field_factory(self.form, f"#{i}", item_field)
                with self.list_container:
                    with ui.row() as row:
                        field_ui.render_value(item)
                        ui.button(
                            "Remove",
                            on_click=lambda e, row=row: self.list_container.remove(row),
                        )

            def add_item(value: Any | None = None) -> None:
                self.value.append(value or "???")
                count = len(self.value)
                with self.list_container:
                    with ui.row() as row:
                        field_ui = self.form._field_factory(
                            self.form, f"#{count-1}", item_field
                        )
                        field_ui.render_value(value)
                        ui.button(
                            "Remove",
                            on_click=lambda e, row=row: self.list_container.remove(row),
                        )

            ui.button("Add", on_click=lambda: add_item())

        return card
