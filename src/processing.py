from typing import List, Dict
from datetime import datetime

def filter_by_state(transactions: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    """
        Фильтрует список транзакций по указанному статусу.
        """
    filtered_list = []
    for dict in transactions:
        if dict.get('state') == state:
            filtered_list.append(dict)
        else:
            continue
    return filtered_list


def sort_by_date(operations: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """
     Сортирует список транзакций по дате.
     """
    sorted_operations = operations.copy()
    sorted_operations.sort(key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)

    return sorted_operations


# Пример использования
if __name__ == "__main__":
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    # Фильтрация по статусу
    executed_transactions = filter_by_state(transactions)
    print("EXECUTED транзакции:")
    print(executed_transactions)

    # Сортировка по дате (по умолчанию - новые сначала)
    sorted_transactions = sort_by_date(transactions)
    print("\nОтсортированные транзакции (новые сначала):")
    print(sorted_transactions)

    # Сортировка по дате (старые сначала)
    sorted_asc_transactions = sort_by_date(transactions, reverse=False)
    print("\nОтсортированные транзакции (старые сначала):")
    print(sorted_asc_transactions)