from src.domain.html.dom.elements._html_element import HTMLElement


class HTMLImageElement(HTMLElement):
    @property
    def src(self) -> str | None:
        return self.attributes.get("src")

    @property
    def alt(self) -> str | None:
        return self.attributes.get("alt")
