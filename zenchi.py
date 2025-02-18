# installing packages if user is 怠け者

from sys import executable
from os import system
from importlib.util import find_spec

if find_spec("bs4") is None:
    system(f"\"{executable}\" -m pip install bs4")
del executable, system, find_spec

# actual code starts here.

import textwrap
from time import time
from re import compile as RE
from argparse import ArgumentParser

from core.client import CitatyApi
from core.obj import Page


class App:
    def __init__(self, query: str, page: str, out: str) -> None:
        self.api = CitatyApi()

        self.page: list[int] = self.paging(page)
        
        self.query: str = query
        self.out_file: str = "output.txt"

        self.auto_url = RE(r"<a href=\"(.*)\" ").findall
        # self.auto_name = RE(r"data-autocomplete-value=\"(.*)\">").findall
        self.auto_name = RE(r" class=\"search__suggest__item__link\">(.*)</a>").findall

    def paging(self, page: str) -> list[int]:
        if '-' not in page:
            page = int(page)
            if page > 0:
                page -= 1
            return [page]

        first, second = map(int, page.split('-'))
        if first > 0:
            first -= 1
        return list(range(first, second))

    def get_uri(self, quote: str, page: int) -> str:
        quote = self.auto_url(quote)[0][len(self.api.domain('')):]
        return '?'.join([quote, f"page={page}"])

    def autocomplete(self):
        query = tuple(self.api.autocomplete(self.query).values())[:-1]
        for num, obj in enumerate(query, 1):
            print(f"{num:>2} : {self.auto_name(obj)[0]}")
        return query[int(input("> ")) - 1]

    def main(self) -> None:
        # quotes = tuple(self.api.autocomplete(self.query).values())[0]
        case = self.autocomplete()

        out_file = open(self.out_file, "w", encoding = "utf-8")
        for page_id in self.page:
            page_line = f"\n<{f' PAGE {page_id + 1} ':―^40}>\n"
            print(page_line)
            out_file.write(page_line + "\n")

            page = self.api.page(self.get_uri(case, page_id))
            for quote in Page(page).quotes():
                quote_line = '\n'.join(textwrap.wrap(
                    quote.quote, 40, 
                    replace_whitespace = False,
                    break_on_hyphens = False,
                    fix_sentence_endings = True,
                    drop_whitespace = True,
                    break_long_words = True,
                    expand_tabs = False
                ))
                quote_line = f"❝{quote_line}❞\n— {quote.qcharacter.strip()}\n"

                print(quote_line)
                out_file.write(quote_line + "\n")
        out_file.close()


if __name__ == "__main__":
    parser = ArgumentParser(description = "Zenchi - citaty.info quotes parser")
    parser.add_argument("quote", help = "")
    parser.add_argument("-p", "--page", default = "0", dest = "page", help = "{page} or {from}-{to} (1, 1-3)")
    args = parser.parse_args()

    App(args.quote, args.page).main()
