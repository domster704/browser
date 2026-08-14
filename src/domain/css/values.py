from enum import StrEnum


class Display(StrEnum):
    NONE = "none"
    BLOCK = "block"
    INLINE = "inline"


class WhiteSpace(StrEnum):
    NORMAL = "normal"
    PRE = "pre"


Color = tuple[int, int, int]
