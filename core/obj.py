from bs4 import BeautifulSoup as BS # bs4
from bs4.element import Tag


class Quote:
    def __init__(self, element: Tag) -> None:
        self.raw: Tag = element

    @property
    def quote(self) -> str:
        """
         Quote text
        """
        # return self.raw.select_one("div.field-item.even.last").text
        tag = self.raw.select_one("div.field.field-name-body.field-type-text-with-summary")\
                    .select_one("div.field-item.even.last")
        return tag.text.replace("...", "…")

    @property
    def qcharacter(self) -> str:
        """
         Quoted Character
        """
        return self.raw.select_one("div.field.field-type-taxonomy-term-reference")\
                    .select_one("div.field-item.even").text.replace("\n", " ").replace("-", "—")

    # @property
    # def qtags(self) -> list:
    #     return self.raw.select_one("div.node__topics")\
    #                 .select_one("div.field.field-type-taxonomy-term-reference")\
    #                 .select("div.field-item")

    def __repr__(self) -> str:
        return f"\"{self.quote.strip()}\"\n- {self.qcharacter}"


class Page:
    def __init__(self, page: str) -> None:
        self.page = BS(page, "lxml")

    def quotes(self):
        data = self.page.select_one("div.view-content").select("div.views-row")
        return [Quote(el) for el in data]
