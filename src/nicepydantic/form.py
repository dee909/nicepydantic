from __future__ import annotations

from typing import Any, Callable, cast

from nicegui import ui
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .factory import default_field_factory


class PydanticForm(ui.column):
    def __init__(
        self,
        value: BaseModel,
        field_factory: Callable[[FieldInfo], Any] | None = None,
    ) -> None:
        super().__init__()
        self.value = value
        self._field_factory = field_factory or default_field_factory

        with self:
            self._build()

    def _build(self) -> None:
        for name, field in self.value.model_fields.items():
            if isinstance(field.json_schema_extra, dict) and "gui" in field.json_schema_extra:
                self.build_field(field)
            else:
                self._field_factory(field)

    def build_field(self, field: FieldInfo) -> ui.element:
        return cast(ui.element, ui.label(field.title or ""))

    def __getattr__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self.value, name)
