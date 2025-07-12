def get_mask_card_number(card_number: str) -> str:
    """Маскирует 6 цифр номера карты и разбивает на 4 блока."""
    if not isinstance(card_number, str):
        return "Неверный тип данных"

    if not card_number.isdigit():
        return "Неверный номер карты"

    if len(card_number) != 16:
        return "Неверный номер карты"

    masked_card_show = card_number[:4] + " " + card_number[4:6] + "**" + " **** " + card_number[-4:]
    return masked_card_show


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    if not isinstance(account_number, str):
        return "Неверный тип данных"

    if not account_number.isdigit():
        return "Неверный номер счета"

    if len(account_number) < 4:
        return "Неверный номер счета"

    account_can_be_show = "**" + account_number[-4:]
    return account_can_be_show
