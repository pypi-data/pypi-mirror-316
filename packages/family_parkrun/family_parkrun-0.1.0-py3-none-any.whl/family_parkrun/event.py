from datetime import date
import re
from dataclasses import dataclass

from .html_construct import a

NAME_URL = re.compile("https://www.parkrun.org.uk/([^/]+)/results/?")


@dataclass(frozen=True, order=True)
class Parkrun:
    name: str
    short_name: str

    @classmethod
    def from_url_title(cls, url, title):
        short_name = NAME_URL.fullmatch(url).group(1)
        return cls(title.replace(" parkrun", ""), short_name)

    @property
    def url(self):
        return f"https://www.parkrun.org.uk/{self.short_name}"

    def html(self):
        return a(self.name, href=self.url)


@dataclass(frozen=True)
class Date:
    date: date
    url: str

    @classmethod
    def from_link(cls, a):
        return cls(date(*(int(i) for i in a.contents[0].split("/")[::-1])), a["href"])

    def html(self):
        return a(self.date, href=self.url)
