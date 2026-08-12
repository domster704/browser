from enum import Enum, auto


class TokenizerState(Enum):
    DATA = auto()
    TAG_OPEN = auto()
    TAG_NAME = auto()
    END_TAG_OPEN = auto()
    CHARACTER_REFERENCE = auto()

    SELF_CLOSING_START_TAG = auto()
    # BOGUS_COMMENT = auto()

    MARKUP_DECLARATION_OPEN = auto()

    # ATTRIBUTE START
    BEFORE_ATTRIBUTE_NAME = auto()
    ATTRIBUTE_NAME = auto()
    AFTER_ATTRIBUTE_NAME = auto()
    BEFORE_ATTRIBUTE_VALUE = auto()

    ATTRIBUTE_VALUE_DOUBLE_QUOTED = auto()
    ATTRIBUTE_VALUE_SINGLE_QUOTED = auto()
    ATTRIBUTE_VALUE_UNQUOTED = auto()

    AFTER_ATTRIBUTE_VALUE_QUOTED = auto()
    # ATTRIBUTE END

    # COMMENT START
    COMMENT_START = auto()
    COMMENT_START_DASH = auto()
    COMMENT = auto()
    COMMENT_END_DASH = auto()
    COMMENT_END = auto()
    # COMMENT END

    # DOCTYPE START
    DOCTYPE = auto()
    BEFORE_DOCTYPE_NAME = auto()
    DOCTYPE_NAME = auto()
    AFTER_DOCTYPE_NAME = auto()
    # DOCTYPE END
