from collections.abc import Callable

from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.handlers.attribute import (
    handle_after_attribute_name,
    handle_after_attribute_value_quoted,
    handle_attribute_name,
    handle_attribute_value_double_quoted,
    handle_attribute_value_single_quoted,
    handle_attribute_value_unquoted,
    handle_before_attribute_name,
    handle_before_attribute_value,
)
from src.domain.html.tokenizer.handlers.comment import (
    handle_comment,
    handle_comment_end,
    handle_comment_end_dash,
    handle_comment_start,
    handle_comment_start_dash,
)
from src.domain.html.tokenizer.handlers.data import (
    handle_character_reference,
    handle_data,
)
from src.domain.html.tokenizer.handlers.doctype import (
    handle_after_doctype_name,
    handle_before_doctype_name,
    handle_doctype,
    handle_doctype_name,
)
from src.domain.html.tokenizer.handlers.markup import handle_markup_declaration_open
from src.domain.html.tokenizer.handlers.tag import (
    handle_end_tag_open,
    handle_self_closing_start_tag,
    handle_tag_name,
    handle_tag_open,
)
from src.domain.html.tokenizer.state import TokenizerState

type StateHandler = Callable[
    [TokenizerContext, str],
    None,
]

STATE_HANDLERS: dict[
    TokenizerState,
    StateHandler,
] = {
    TokenizerState.DATA: handle_data,
    TokenizerState.TAG_OPEN: handle_tag_open,
    TokenizerState.TAG_NAME: handle_tag_name,
    TokenizerState.END_TAG_OPEN: handle_end_tag_open,
    TokenizerState.CHARACTER_REFERENCE: handle_character_reference,
    TokenizerState.SELF_CLOSING_START_TAG: handle_self_closing_start_tag,
    TokenizerState.BEFORE_ATTRIBUTE_NAME: handle_before_attribute_name,
    TokenizerState.ATTRIBUTE_NAME: handle_attribute_name,
    TokenizerState.AFTER_ATTRIBUTE_NAME: handle_after_attribute_name,
    TokenizerState.BEFORE_ATTRIBUTE_VALUE: handle_before_attribute_value,
    TokenizerState.ATTRIBUTE_VALUE_DOUBLE_QUOTED: handle_attribute_value_double_quoted,
    TokenizerState.ATTRIBUTE_VALUE_SINGLE_QUOTED: handle_attribute_value_single_quoted,
    TokenizerState.ATTRIBUTE_VALUE_UNQUOTED: handle_attribute_value_unquoted,
    TokenizerState.AFTER_ATTRIBUTE_VALUE_QUOTED: handle_after_attribute_value_quoted,
    TokenizerState.MARKUP_DECLARATION_OPEN: handle_markup_declaration_open,
    TokenizerState.COMMENT_START: handle_comment_start,
    TokenizerState.COMMENT_START_DASH: handle_comment_start_dash,
    TokenizerState.COMMENT: handle_comment,
    TokenizerState.COMMENT_END_DASH: handle_comment_end_dash,
    TokenizerState.COMMENT_END: handle_comment_end,
    TokenizerState.DOCTYPE: handle_doctype,
    TokenizerState.BEFORE_DOCTYPE_NAME: handle_before_doctype_name,
    TokenizerState.DOCTYPE_NAME: handle_doctype_name,
    TokenizerState.AFTER_DOCTYPE_NAME: handle_after_doctype_name,
}
