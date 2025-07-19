import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("", "Не найдены цифры в номере"),
        ("12345", "Некорректная длина номера"),
        ("Счет 123", "Некорректная длина номера"),
        ("Карта без номера", "Не найдены цифры в номере"),
        ("Счет 7365410843013587430", "Некорректная длина номера"),
        ("Visa Platinum 700079228960636", "Некорректная длина номера"),
    ],
)
def test_mask_account_card(input_str: str, expected: str) -> None:
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("", "Неверный формат входных данных"),
        ("20240311", "Неверный формат входных данных"),
        ("123456789", "Неверный формат входных данных"),  # Изменено на строку
        ("2024-03-11T02:26:18.6714071234567890", "11.03.2024"),
        ("2024-03-11T02:26:18", "11.03.2024"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected
