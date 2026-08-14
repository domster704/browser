from dataclasses import dataclass

from src.domain.rendering.text import TextMeasurer


@dataclass(frozen=True, slots=True)
class LayoutContext:
    text_measurer: TextMeasurer
