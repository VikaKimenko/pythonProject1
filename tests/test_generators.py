from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура с тестовыми данными транзакций
@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# Тесты для filter_by_currency
@pytest.mark.parametrize(
    "currency, expected_count, expected_ids",
    [
        ("USD", 3, [939719570, 142264268, 895315941]),
        ("RUB", 2, [873106923, 594226727]),
        ("EUR", 0, []),
        ("GBP", 0, []),
    ],
)
def test_filter_by_currency(
    transactions: List[Dict[str, Any]],
    currency: str,
    expected_count: int,
    expected_ids: List[int],
) -> None:
    """Тестирование фильтрации транзакций по валюте."""
    filtered = list(filter_by_currency(transactions, currency))
    assert len(filtered) == expected_count
    assert [t["id"] for t in filtered] == expected_ids
    for transaction in filtered:
        assert transaction["operationAmount"]["currency"]["code"] == currency


def test_filter_by_currency_empty_input() -> None:
    """Тестирование с пустым списком транзакций."""
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_missing_fields() -> None:
    """Тестирование обработки транзакций с отсутствующими полями."""
    test_data: List[Dict[str, Any]] = [
        {"id": 1},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"currency": {}}},
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    filtered = list(filter_by_currency(test_data, "USD"))
    assert len(filtered) == 1
    assert filtered[0]["id"] == 4


# Тесты для transaction_descriptions
def test_transaction_descriptions_all(transactions: List[Dict[str, Any]]) -> None:
    """Тестирование генератора описаний для всех транзакций."""
    gen = transaction_descriptions(transactions)
    descriptions = list(gen)
    assert len(descriptions) == 5
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


@pytest.mark.parametrize("count", [0, 1, 3, 5])
def test_transaction_descriptions_partial(
    transactions: List[Dict[str, Any]],
    count: int,
) -> None:
    """Тестирование генератора описаний для части транзакций."""
    gen = transaction_descriptions(transactions)
    descriptions = [next(gen) for _ in range(count)] if count > 0 else []
    assert len(descriptions) == count
    if count > 0:
        assert descriptions[0] == "Перевод организации"


def test_transaction_descriptions_empty_input() -> None:
    """Тестирование с пустым списком транзакций."""
    with pytest.raises(StopIteration):
        next(transaction_descriptions([]))


def test_transaction_descriptions_missing_field() -> None:
    """Тестирование обработки транзакции без описания."""
    test_data: List[Dict[str, Any]] = [
        {"id": 1},
        {"id": 2, "description": "Test"},
    ]
    gen = transaction_descriptions(test_data)
    assert next(gen) == "Test"
    with pytest.raises(StopIteration):
        next(gen)


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9998, 10000, ["0000 0000 0000 9998", "0000 0000 0000 9999", "0000 0000 0001 0000"]),
        (9999_9999_9999_9998, 9999_9999_9999_9999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    """Тестирование генератора номеров карт в диапазоне."""
    generated = list(card_number_generator(start, end))
    assert generated == expected
    for number in generated:
        parts = number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)


def test_card_number_generator_single_value() -> None:
    """Тестирование генератора для одного номера."""
    assert next(card_number_generator(42, 42)) == "0000 0000 0000 0042"


def test_card_number_generator_invalid_range() -> None:
    """Тестирование неверного диапазона (start > end)."""
    with pytest.raises(StopIteration):
        next(card_number_generator(10, 5))


def test_card_number_generator_edge_cases() -> None:
    """Тестирование крайних случаев."""
    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"
    assert next(card_number_generator(9999_9999_9999_9999, 9999_9999_9999_9999)) == "9999 9999 9999 9999"
