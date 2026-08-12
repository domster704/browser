from typing import Iterable

from src.domain.html.dom.element_factory import HTMLElementFactory
from src.domain.html.dom.nodes import DocumentNode, ElementNode, CommentNode, TextNode
from src.domain.html.tokenizer.tokens import (
    BaseToken,
    StartTagToken,
    EndTagToken,
    CharacterToken,
)

type DOMType = DocumentNode | ElementNode
type StackDOMType = list[DOMType]


class HTMLTreeBuilder:
    def __init__(
        self,
        element_factory: HTMLElementFactory,
    ):
        self._element_factory = element_factory

    def parse(self, tokens: Iterable[BaseToken]) -> DocumentNode:
        document = DocumentNode()
        stack: StackDOMType = [document]

        for token in tokens:
            current_node = stack[-1]

            if isinstance(token, StartTagToken):
                element = self._element_factory.create(
                    tag_name=token.name,
                    attributes=token.attributes,
                )
                current_node.children.append(element)

                if not token.self_closing:
                    stack.append(element)
            elif isinstance(token, EndTagToken):
                self.__close_element(stack, token)
            elif isinstance(token, CharacterToken):
                self.__append_text(current_node, token.data)
            elif isinstance(token, CommentNode):
                current_node.children.append(CommentNode(token.data))

        return document

    def __close_element(self, stack: StackDOMType, token: EndTagToken):
        if len(stack) == 1:
            return

        current = stack[-1]
        if isinstance(current, ElementNode) and current.tag_name == token.name:
            stack.pop()

    def __append_text(self, parent: DOMType, data: str):
        if parent.children and isinstance(parent.children[-1], TextNode):
            parent.children[-1].data += data
            return

        parent.children.append(TextNode(data=data))
