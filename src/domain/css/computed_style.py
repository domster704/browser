from __future__ import annotations

from dataclasses import dataclass, replace

from src.domain.css.values import Display, Color, WhiteSpace


@dataclass(frozen=True, slots=True)
class ComputedStyle:
    display: Display = Display.INLINE

    font_family: str = "sans-serif"
    font_size: float = 16.0
    font_weight: int = 400
    font_italic: bool = False

    color: Color = (0, 0, 0)

    white_space: WhiteSpace = WhiteSpace.NORMAL

    margin_top: float = 0.0
    margin_bottom: float = 0.0
    margin_left: float = 0.0
    margin_right: float = 0.0

    @classmethod
    def inherited_from(cls, parent: ComputedStyle | None):
        if parent is None:
            return cls()

        return cls(
            font_family=parent.font_family,
            font_size=parent.font_size,
            font_weight=parent.font_weight,
            font_italic=parent.font_italic,
            color=parent.color,
            white_space=parent.white_space,
        )

    def for_text(self) -> ComputedStyle:
        return replace(
            self,
            display=Display.INLINE,
            margin_top=0,
            margin_bottom=0,
            margin_left=0,
            margin_right=0,
        )
