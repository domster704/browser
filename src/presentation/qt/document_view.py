import re
from dataclasses import dataclass

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QTextLayout
from PyQt6.QtWidgets import QWidget

from src.domain.html.dom.nodes import (
    DocumentNode,
    Node,
    CommentNode,
    DocumentTypeNode,
    TextNode,
    ElementNode,
)


@dataclass
class Block:
    text: str
    tag_name: str = "p"


HIDDEN_TAGS = {
    "head",
    "script",
    "style",
    "meta",
    "link",
    "title",
}


class DocumentView(QWidget):
    PADDING = 16

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self._document: DocumentNode | None = None
        self._blocks: list[Block] = []
        self._layouts: list[QTextLayout] = []

        self.setMinimumHeight(1)

    def set_document(self, document: DocumentNode) -> None:
        self._document = document
        self._blocks = []

    def _collect_blocks(self, node: Node) -> None:
        if isinstance(node, DocumentNode):
            for child in node.children:
                ...
            return

        if isinstance(node, (CommentNode, DocumentTypeNode)):
            return

        if isinstance(node, TextNode):
            text = self.__normalize_whitespace(node.data)
            if text.strip():
                self._blocks.append(
                    Block(text=text, tag_name="p")
                )  # TODO: add tag_name to TextNode
            return

        if not isinstance(node, ElementNode):
            return

        tag = node.tag_name.casefold()
        if tag in HIDDEN_TAGS:
            return

        if tag == "br":
            self._blocks.append(Block(text="", tag_name="br"))

        contains_blocks = any(
            isinstance(child, ElementNode)
            and child.tag_name.casefold() not in HIDDEN_TAGS
            for child in node.children
        )
        if contains_blocks:
            for child in node.children:
                self._collect_blocks(child)
            return

        text = self

    @staticmethod
    def __normalize_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text)
