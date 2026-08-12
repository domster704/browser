from src.domain.html.dom.elements._html_element import HTMLElement
from src.domain.html.dom.elements.anchor import HTMLAnchorElement
from src.domain.html.dom.elements.image import HTMLImageElement
from src.domain.html.dom.elements.input import HTMLInputElement


class HTMLElementFactory:
    def create(
        self,
        tag_name: str,
        attributes: dict[str, str],
    ) -> HTMLElement:

        match tag_name:
            case "a":
                cls = HTMLAnchorElement
            case "img":
                cls = HTMLImageElement
            case "input":
                cls = HTMLInputElement
            case _:
                cls = HTMLElement

        return cls(
            tag_name=tag_name,
            attributes=attributes,
        )
