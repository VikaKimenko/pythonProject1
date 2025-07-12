from datetime import datetime
from typing import Dict, List


def filter_by_state(operations: List[Dict[str, object]], state: str = "EXECUTED") -> list[dict[str, object]]:
    """
    Фильтрует список транзакций по указанному статусу.
    """
    filtered_list = []
    for entry in operations:
        if entry.get("state") == state:
            filtered_list.append(entry)
        else:
            continue
    return filtered_list


def sort_by_date(operations: list[dict[str, object]], reverse: bool = True) -> list[dict[str, object]]:
    """
    Сортирует список транзакций по дате.
    """
    sorted_operations = operations.copy()
    sorted_operations.sort(key=lambda x: datetime.fromisoformat(str(x["date"])), reverse=reverse)

    return sorted_operations
