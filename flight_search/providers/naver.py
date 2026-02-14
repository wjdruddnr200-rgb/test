from __future__ import annotations

from urllib.parse import quote

from flight_search.models import FlightOption, SearchCriteria
from flight_search.providers.base import FlightProvider


class NaverFlightsProvider(FlightProvider):
    name = "Naver 항공권"

    def build_search_url(self, criteria: SearchCriteria) -> str:
        # 네이버는 공식 공개 API가 없어서 딥링크 URL + HTML 파싱 방식으로 구성합니다.
        route = quote(f"{criteria.origin}-{criteria.destination}")
        date_text = criteria.departure_date.isoformat()
        return f"https://m-flight.naver.com/flights/international/{route}/{date_text}?adult=1"

    def parse_results(self, html: str, url: str, criteria: SearchCriteria) -> list[FlightOption]:
        soup = self.soup(html)
        options: list[FlightOption] = []
        if soup is None:
            return options

        cards = soup.select("div[class*='item_result'], li[class*='item_result'], div[class*='result']")
        for card in cards:
            airline_node = card.select_one("strong, span[class*='airline']")
            airline = airline_node.get_text(strip=True) if airline_node else "Unknown"
            time_nodes = card.select("span[class*='time'], strong[class*='time']")
            dep = self.parse_time(time_nodes[0].get_text(strip=True)) if len(time_nodes) > 0 else None
            arr = self.parse_time(time_nodes[1].get_text(strip=True)) if len(time_nodes) > 1 else None
            price_node = card.select_one("strong[class*='price'], span[class*='price']")
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
