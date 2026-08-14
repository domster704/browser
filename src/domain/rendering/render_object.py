from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.css.computed_style import ComputedStyle
from src.domain.rendering.display_list import DisplayCommand
from src.domain.rendering.layout import LayoutContext


class RenderObject(ABC):
    def __init__(self, style: ComputedStyle):
        self.style = style

        self.children: list[RenderObject] = []

        self.x = 0.0
        self.y = 0.0

        self.width = 0.0
        self.height = 0.0

    def append_child(self, child: RenderObject) -> None:
        self.children.append(child)

    @abstractmethod
    def layout(
        self, context: LayoutContext, *, x: float, y: float, available_width: float
    ) -> None:
        pass

    def collect_display_list(self, result: list[DisplayCommand]) -> None:
        for child in self.children:
            child.collect_display_list(result)


class RenderDocument(RenderObject):
    def layout(
        self, context: LayoutContext, *, x: float, y: float, available_width: float
    ) -> None:
        self.x = x
        self.y = y
        self.width = available_width

        # self.height = _layout_flow_children(
        #     self.children,
        #     context=context,
        #     x=x,
        #     y=y,
        #     available_width=available_width,
        # )
