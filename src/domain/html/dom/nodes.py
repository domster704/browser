from dataclasses import dataclass, field


class Node:
    pass


@dataclass
class DocumentNode(Node):
    children: list[Node] = field(default_factory=list)


@dataclass
class ElementNode(Node):
    tag_name: str
    attributes: dict[str, str]
    children: list[Node] = field(default_factory=list)


@dataclass
class TextNode(Node):
    data: str


@dataclass
class CommentNode(Node):
    data: str
