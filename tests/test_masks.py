from typing import Any

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Основные тесты для строковых входных данных
@pytest.mark.parametrize(
    "value, expected",
    [
        # Корректные номера карт
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        # Неправильная длина
        ("70007922896061", "Неверный номер карты"),
        ("12345667765433345566776543345677", "Неверный номер карты"),
        ("", "Неверный номер карты"),
        # Не цифровые символы
        ("700079ffffffff", "Неверный номер карты"),
    ],
)
def test_get_mask_card_number(value: str, expected: str) -> None:
    assert get_mask_card_number(value) == expected


# Тесты для нестроковых входных данных
@pytest.mark.parametrize(
    "value, expected",
    [
        (1234, "Неверный тип данных"),
        (["lala", "lalal"], "Неверный тип данных"),
        ({"key": "value"}, "Неверный тип данных"),
        (None, "Неверный тип данных"),
    ],
)
def test_get_mask_card_number_invalid_types(value: Any, expected: str) -> None:
    assert get_mask_card_number(value) == expected


# Основные тесты для строковых входных данных
@pytest.mark.parametrize(
    "value, expected",
    [
        # Корректные номера счетов
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
        # Слишком короткие
        ("736", "Неверный номер счета"),
        ("", "Неверный номер счета"),
        # Не цифровые символы
        ("7365410843013587lala", "Неверный номер счета"),
        ("не ну а вдруг", "Неверный номер счета"),
    ],
)
def test_get_mask_account(value: str, expected: str) -> None:
    assert get_mask_account(value) == expected


# Тесты для нестроковых входных данных
@pytest.mark.parametrize(
    "value, expected",
    [
        (1234, "Неверный тип данных"),
        (["lala", "lalal"], "Неверный тип данных"),
        ({"key": "value"}, "Неверный тип данных"),
        (None, "Неверный тип данных"),
    ],
)
def test_get_mask_account_invalid_types(value: Any, expected: str) -> None:
    assert get_mask_account(value) == expected
