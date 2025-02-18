from urllib.request import urlopen
from json import loads as JSON


class CitatyApi:
    """
     CitatyApi
    """
    def __init__(self) -> None:
        self.domain = "https://citaty.info/{}".format

    def page(self, path: str) -> str:
        return urlopen(self.domain(path)).read().decode()

    def autocomplete(self, query: str) -> dict:
        return JSON(urlopen(self.domain(f"citaty_search_autocomplete/{query}"))\
                .read().decode())

    def append(self) -> None:
        pass # /views/ajax
