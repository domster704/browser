from dataclasses import dataclass, fields, replace

from src.domain.css.computed_style import ComputedStyle
from src.domain.css.values import Display, Color, WhiteSpace


@dataclass(frozen=True, slots=True)
class CSSDeclarations:

    display: Display | None = None

    font_family: str | None = None
    font_size: float | None = None
    font_weight: int | None = None
    font_italic: bool | None = None

    color: Color | None = None

    white_space: WhiteSpace | None = None

    margin_top: float | None = None
    margin_right: float | None = None
    margin_bottom: float | None = None
    margin_left: float | None = None

    def apply(self, base: ComputedStyle) -> ComputedStyle:
        updates = {}

        for field_info in fields(self):
            value = getattr(self, field_info.name)

            if value is not None:
                updates[field_info.name] = value

        return replace(base, **updates)
