from src.domain.html.dom.elements._html_element import HTMLElement


class HTMLInputElement(HTMLElement):
    @property
    def value(self) -> str:
        return self.attributes.get("value", "")

    @property
    def input_type(self) -> str:
        return self.attributes.get("type", "text")
