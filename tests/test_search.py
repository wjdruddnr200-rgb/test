from datetime import date, time

from flight_search.models import FlightOption, SearchCriteria


def test_option_matches_by_price_and_time():
    criteria = SearchCriteria(
        origin="ICN",
        destination="NRT",
        departure_date=date(2026, 3, 1),
        earliest_departure=time(9, 0),
        latest_departure=time(14, 0),
        max_price=200000,
    )

    option = FlightOption(
        provider="Skyscanner",
        airline="TestAir",
        departure_time=time(11, 30),
        arrival_time=time(13, 45),
        price=180000,
        currency="KRW",
        deep_link="https://example.com",
    )

    assert option.matches(criteria)


def test_option_does_not_match_for_time_or_price():
    criteria = SearchCriteria(
        origin="ICN",
        destination="NRT",
        departure_date=date(2026, 3, 1),
        earliest_departure=time(9, 0),
        latest_departure=time(14, 0),
        max_price=200000,
    )

    expensive = FlightOption(
        provider="Skyscanner",
        airline="TestAir",
        departure_time=time(10, 0),
        arrival_time=None,
        price=250000,
        currency="KRW",
        deep_link="https://example.com",
    )

    late = FlightOption(
        provider="Skyscanner",
        airline="TestAir",
        departure_time=time(15, 0),
        arrival_time=None,
        price=180000,
        currency="KRW",
        deep_link="https://example.com",
    )

    assert not expensive.matches(criteria)
    assert not late.matches(criteria)
