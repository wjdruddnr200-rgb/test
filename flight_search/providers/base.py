from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
import re

from flight_search.models import FlightOption, SearchCriteria


class FlightProvider(ABC):
    name: str

    @abstractmethod
    def build_search_url(self, criteria: SearchCriteria) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_results(self, html: str, url: str, criteria: SearchCriteria) -> list[FlightOption]:
        raise NotImplementedError

    def parse_price(self, text: str) -> int | None:
        numbers = re.sub(r"[^0-9]", "", text)
        if not numbers:
            return None
        return int(numbers)

    def parse_time(self, text: str):
        text = text.strip()
        for pattern in ("%H:%M", "%H%M"):
            try:
                return datetime.strptime(text, pattern).time()
            except ValueError:
                continue
        return None

    def soup(self, html: str):
        try:
            from bs4 import BeautifulSoup
        except ModuleNotFoundError:
            return None
        return BeautifulSoup(html, "html.parser")
