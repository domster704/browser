from src.domain.html.dom.elements._html_element import HTMLElement


class HTMLAnchorElement(HTMLElement):
    @property
    def href(self) -> str | None:
        return self.attributes.get("href")
