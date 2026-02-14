from __future__ import annotations

from dataclasses import dataclass
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flight_search.models import FlightOption, SearchCriteria
from flight_search.providers.base import FlightProvider


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ProviderResult:
    provider: str
    url: str
    options: list[FlightOption]
    error: str | None = None


class FlightSearcher:
    def __init__(self, providers: list[FlightProvider], timeout: int = 20):
        self.providers = providers
        self.timeout = timeout

    def run(self, criteria: SearchCriteria) -> list[ProviderResult]:
        results: list[ProviderResult] = []

        for provider in self.providers:
            url = provider.build_search_url(criteria)
            try:
                req = Request(url, headers={"User-Agent": USER_AGENT})
                with urlopen(req, timeout=self.timeout) as response:
                    html = response.read().decode("utf-8", errors="ignore")
                parsed = provider.parse_results(html, url, criteria)
                filtered = [option for option in parsed if option.matches(criteria)]
                filtered.sort(key=lambda o: o.price)
                results.append(ProviderResult(provider=provider.name, url=url, options=filtered))
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                logger.warning("provider_failed provider=%s error=%s", provider.name, exc)
                results.append(ProviderResult(provider=provider.name, url=url, options=[], error=str(exc)))

        return results
