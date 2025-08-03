from typing import Dict, Iterator, List, Any


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.
    """
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        curr = op_amount.get("currency", {})
        if curr.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор описаний транзакций.
    """
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    for number in range(start, end + 1):
        card_num = f"{number:016d}"
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
