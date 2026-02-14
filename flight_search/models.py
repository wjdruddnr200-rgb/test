from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time


@dataclass(slots=True)
class SearchCriteria:
    origin: str
    destination: str
    departure_date: date
    earliest_departure: time | None = None
    latest_departure: time | None = None
    max_price: int | None = None
    currency: str = "KRW"


@dataclass(slots=True)
class FlightOption:
    provider: str
    airline: str
    departure_time: time
    arrival_time: time | None
    price: int
    currency: str
    deep_link: str

    def matches(self, criteria: SearchCriteria) -> bool:
        if criteria.max_price is not None and self.price > criteria.max_price:
            return False

        if criteria.earliest_departure and self.departure_time < criteria.earliest_departure:
            return False

        if criteria.latest_departure and self.departure_time > criteria.latest_departure:
            return False

        return True
