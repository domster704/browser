from src.domain.css.computed_style import ComputedStyle
from src.domain.css.user_agent_stylesheet import USER_AGENT_STYLESHEET
from src.domain.html.dom.nodes import ElementNode


class StyleResolver:
    def resolve(
        self, element: ElementNode, parent_style: ComputedStyle | None
    ) -> ComputedStyle:
        style = ComputedStyle.inherited_from(parent_style)
        css_declaration = USER_AGENT_STYLESHEET.get(element.tag_name)

        if css_declaration:
            style = css_declaration.apply(style)

        return style
