from __future__ import annotations

import argparse
from datetime import datetime

from flight_search.models import SearchCriteria
from flight_search.providers.naver import NaverFlightsProvider
from flight_search.providers.skyscanner import SkyscannerProvider
from flight_search.search import FlightSearcher


def _parse_time(raw: str | None):
    if raw is None:
        return None
    return datetime.strptime(raw, "%H:%M").time()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="날짜/시간/가격 조건으로 항공권 메타 검색")
    parser.add_argument("--origin", required=True, help="출발지 IATA 코드 (예: ICN)")
    parser.add_argument("--destination", required=True, help="도착지 IATA 코드 (예: NRT)")
    parser.add_argument("--date", required=True, help="출발일 (YYYY-MM-DD)")
    parser.add_argument("--earliest", help="최소 출발 시간 (HH:MM)")
    parser.add_argument("--latest", help="최대 출발 시간 (HH:MM)")
    parser.add_argument("--max-price", type=int, help="최대 금액")
    parser.add_argument("--currency", default="KRW", help="통화 코드")
    return parser


def print_result_table(result):
    print(f"\n[{result.provider}] {result.url}")
    if result.error:
        print(f"  - 수집 실패: {result.error}")
        return
    if not result.options:
        print("  - 조건에 맞는 항공편이 없습니다.")
        return

    for option in result.options[:10]:
        arr = option.arrival_time.strftime("%H:%M") if option.arrival_time else "-"
        print(
            f"  - {option.airline:15} {option.departure_time.strftime('%H:%M')} -> {arr}  "
            f"{option.price:,} {option.currency}"
        )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    criteria = SearchCriteria(
        origin=args.origin,
        destination=args.destination,
        departure_date=datetime.strptime(args.date, "%Y-%m-%d").date(),
        earliest_departure=_parse_time(args.earliest),
        latest_departure=_parse_time(args.latest),
        max_price=args.max_price,
        currency=args.currency,
    )

    providers = [NaverFlightsProvider(), SkyscannerProvider()]
    searcher = FlightSearcher(providers=providers)
    results = searcher.run(criteria)

    print("=== 항공권 조건 검색 결과 ===")
    print(
        f"조건: {criteria.origin}->{criteria.destination}, {criteria.departure_date}, "
        f"시간 {args.earliest or '제한없음'}~{args.latest or '제한없음'}, "
        f"최대 금액 {criteria.max_price if criteria.max_price else '제한없음'} {criteria.currency}"
    )

    for result in results:
        print_result_table(result)

    print("\n참고: 일부 사이트는 동적 렌더링/봇 차단으로 인해 결과 수집이 제한될 수 있습니다.")


if __name__ == "__main__":
    main()
