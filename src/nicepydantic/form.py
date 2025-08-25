from __future__ import annotations

from typing import Any, Callable, cast

from nicegui import ui
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .factory import default_field_factory, FieldUI


class PydanticForm(ui.column):
    def __init__(
        self,
        value: BaseModel,
        field_factory: Callable[[FieldInfo], Any] | None = None,
    ) -> None:
        super().__init__()
        self.value = value
        self._field_factory = field_factory or default_field_factory

        self._field_uis: dict[str, FieldUI] = {}
        self._build()

    def clear(self) -> None:
        for n, f in self._field_uis.items():
            f.form_clearing()
        return super().clear()

    def _build(self) -> None:
        self.clear()
        with self:
            with ui.grid(columns=2):
                for name, field in type(self.value).model_fields.items():
                    field_ui = self._field_factory(form=self, name=name, field=field)
                    self._field_uis[name] = field_ui
                    field_ui.render_label()
                    field_ui.render_value(getattr(self.value, name))
