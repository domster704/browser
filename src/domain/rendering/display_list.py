from dataclasses import dataclass

from src.domain.css.computed_style import ComputedStyle


@dataclass(frozen=True, slots=True)
class DrawText:
    text: str

    x: float
    baseline_y: float

    style: ComputedStyle


DisplayCommand = DrawText
