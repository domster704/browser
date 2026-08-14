from dataclasses import dataclass
from typing import Protocol

from src.domain.css.computed_style import ComputedStyle


@dataclass(frozen=True, slots=True)
class TextMetrics:
    width: float
    height: float

    ascent: float  # расстояние от baseline вверх до верхней части глифов
    descent: float  # расстояние от baseline вниз до нижней части глифов


class TextMeasurer(Protocol):
    def measure(self, text: str, style: ComputedStyle) -> TextMetrics: ...


@dataclass(frozen=True, slots=True)
class PositionedText:
    text: str

    x: float
    baseline_y: float
