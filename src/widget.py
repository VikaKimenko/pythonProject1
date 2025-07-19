from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(type_and_number: str) -> str:
    """Функция определяет счет это или номер карты и возвращает замаскированный"""
    if not isinstance(type_and_number, str):
        return "Неверный тип данных"

    text_result = ""
    digit_result = ""

    for el in type_and_number:
        if el.isalpha() or el == " ":
            text_result += el
        elif el.isdigit():
            digit_result += el

    if not digit_result:
        return "Не найдены цифры в номере"

    # Для счетов должна быть ровно 20 цифр
    if len(digit_result) > 16:
        if len(digit_result) != 20:  # Изменено условие
            return "Некорректная длина номера"
        return f"{text_result.strip()} {get_mask_account(digit_result)}"
    elif len(digit_result) == 16:
        return f"{text_result.strip()} {get_mask_card_number(digit_result)}"
    else:
        return "Некорректная длина номера"


def get_date(data_number: str) -> str:
    """Вывести дату в формате "ДД.ММ.ГГГГ"."""
    if not isinstance(data_number, str):
        return "Неверный формат входных данных"

    if len(data_number) >= 10 and data_number[4] == '-' and data_number[7] == '-':
        return f"{data_number[8:10]}.{data_number[5:7]}.{data_number[:4]}"
    return "Неверный формат входных данных"