from __future__ import annotations

from urllib.parse import quote

from flight_search.models import FlightOption, SearchCriteria
from flight_search.providers.base import FlightProvider


class SkyscannerProvider(FlightProvider):
    name = "Skyscanner"

    def build_search_url(self, criteria: SearchCriteria) -> str:
        origin = quote(criteria.origin.upper())
        destination = quote(criteria.destination.upper())
        date_text = criteria.departure_date.strftime("%y%m%d")
        return f"https://www.skyscanner.co.kr/transport/flights/{origin}/{destination}/{date_text}/"

    def parse_results(self, html: str, url: str, criteria: SearchCriteria) -> list[FlightOption]:
        soup = self.soup(html)
        options: list[FlightOption] = []
        if soup is None:
            return options

        cards = soup.select("div[data-testid='itinerary-card'], li[class*='DayViewCard'], div[class*='FlightsTicket']")
        for card in cards:
            airline_node = card.select_one("span[class*='name'], div[class*='LegInfo_routePartialCarrier']")
            airline = airline_node.get_text(strip=True) if airline_node else "Unknown"

            time_nodes = card.select("span[class*='Time'], div[class*='LegInfo_routePartialTime']")
            dep = self.parse_time(time_nodes[0].get_text(strip=True)) if len(time_nodes) > 0 else None
            arr = self.parse_time(time_nodes[1].get_text(strip=True)) if len(time_nodes) > 1 else None

            price_node = card.select_one("span[data-testid='price'], div[class*='Price_mainPrice']")
            price = self.parse_price(price_node.get_text(" ", strip=True)) if price_node else None

            if dep is None or price is None:
                continue

            options.append(
                FlightOption(
                    provider=self.name,
                    airline=airline,
                    departure_time=dep,
                    arrival_time=arr,
                    price=price,
                    currency=criteria.currency,
                    deep_link=url,
                )
            )

        return options
