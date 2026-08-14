from src.domain.css.declaration import CSSDeclarations
from src.domain.css.values import Display, WhiteSpace

USER_AGENT_STYLESHEET: dict[str, CSSDeclarations] = {
    "html": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "body": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "head": CSSDeclarations(
        display=Display.NONE,
    ),
    "script": CSSDeclarations(
        display=Display.NONE,
    ),
    "style": CSSDeclarations(
        display=Display.NONE,
    ),
    "meta": CSSDeclarations(
        display=Display.NONE,
    ),
    "link": CSSDeclarations(
        display=Display.NONE,
    ),
    "title": CSSDeclarations(
        display=Display.NONE,
    ),
    "div": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "main": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "section": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "article": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "header": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "footer": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "nav": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "p": CSSDeclarations(
        display=Display.BLOCK,
        margin_top=8,
        margin_bottom=8,
    ),
    "h1": CSSDeclarations(
        display=Display.BLOCK,
        font_size=32,
        font_weight=700,
        margin_top=16,
        margin_bottom=12,
    ),
    "h2": CSSDeclarations(
        display=Display.BLOCK,
        font_size=24,
        font_weight=700,
        margin_top=14,
        margin_bottom=10,
    ),
    "h3": CSSDeclarations(
        display=Display.BLOCK,
        font_size=19,
        font_weight=700,
        margin_top=12,
        margin_bottom=8,
    ),
    "h4": CSSDeclarations(
        display=Display.BLOCK,
        font_size=16,
        font_weight=700,
        margin_top=10,
        margin_bottom=6,
    ),
    "h5": CSSDeclarations(
        display=Display.BLOCK,
        font_size=13,
        font_weight=700,
        margin_top=8,
        margin_bottom=6,
    ),
    "h6": CSSDeclarations(
        display=Display.BLOCK,
        font_size=11,
        font_weight=700,
        margin_top=8,
        margin_bottom=6,
    ),
    "pre": CSSDeclarations(
        display=Display.BLOCK,
        font_family="monospace",
        white_space=WhiteSpace.PRE,
        margin_top=8,
        margin_bottom=8,
    ),
    "blockquote": CSSDeclarations(
        display=Display.BLOCK,
        margin_top=8,
        margin_bottom=8,
        margin_left=24,
    ),
    "ul": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "ol": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "li": CSSDeclarations(
        display=Display.BLOCK,
    ),
    "span": CSSDeclarations(
        display=Display.INLINE,
    ),
    "a": CSSDeclarations(
        display=Display.INLINE,
        color=(0, 0, 238),
    ),
    "strong": CSSDeclarations(
        font_weight=700,
    ),
    "b": CSSDeclarations(
        font_weight=700,
    ),
    "em": CSSDeclarations(
        font_italic=True,
    ),
    "i": CSSDeclarations(
        font_italic=True,
    ),
    "code": CSSDeclarations(
        font_family="monospace",
    ),
    "br": CSSDeclarations(
        display=Display.INLINE,
    ),
}
