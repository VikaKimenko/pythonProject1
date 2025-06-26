from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(type_and_number: [str]) -> [str]:
    """Функция определяет счет это или номер карты и возвращает замаскированный"""
    text_result = ""
    digit_result = ""
    digit_count = 0
    for el in type_and_number:
        if el.isalpha():
            text_result += el
        elif el.isdigit():
            digit_result += el
            digit_count += 1
    if digit_count > 16:
        return f"{text_result} {get_mask_account(digit_result)}"
    else:
        return f"{text_result} {get_mask_card_number(digit_result)}"


def get_date(data_number: str) -> str:
    """Вывести дату в формате "ДД.ММ.ГГГГ"."""
    correct = data_number[8:10] + "." + data_number[5:7] + "." + data_number[:4]
    return correct
