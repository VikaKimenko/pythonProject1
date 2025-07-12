from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("PENDING", []),  # Несуществующий статус
        (None, [41428829, 939719570]),  # По умолчанию EXECUTED
    ],
)
def test_filter_by_state(sample_transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    if state is None:
        result = filter_by_state(sample_transactions)
    else:
        result = filter_by_state(sample_transactions, state)

    assert [t["id"] for t in result] == expected_ids


# Параметризованные тесты для sort_by_date
@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [41428829, 615064591, 594226727, 939719570]),  # По убыванию
        (False, [939719570, 594226727, 615064591, 41428829]),  # По возрастанию
    ],
)
def test_sort_by_date(sample_transactions: List[Dict[str, Any]], reverse: bool, expected_order: List[int]) -> None:
    result = sort_by_date(sample_transactions, reverse=reverse)
    assert [t["id"] for t in result] == expected_order


# Дополнительные тесты для edge cases
def test_filter_empty_list() -> None:
    assert filter_by_state([]) == []


def test_sort_empty_list() -> None:
    assert sort_by_date([]) == []


def test_sort_invalid_date_format() -> None:
    with pytest.raises(ValueError):
        sort_by_date([{"date": "invalid-date"}])
