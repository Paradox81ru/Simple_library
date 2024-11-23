from datetime import datetime

from book import BookStatus
from exceptions import ValidationError


def validation_id(val: int | str) -> int:
    """
    Проверяет переданный идентификатор.
    Корректный идентификатор это целое положительное число
    :param val: Идентификатор для проверки
    :return: Корректный идентификатор
    :raises ValidationError: Ошибка проверки корректности идентификатора
    """
    try:
        _id = int(val)
    except ValueError:
        raise ValidationError("The identifier must be an integer.")

    if _id < 1:
        raise ValidationError("The identifier must be greater than zero.")

    return _id

def validation_year(val: int | str) -> int:
    """
    Проверяет переданный год.
    Корректный год, это целое число не больше текущего года.
    Год может быть меньше нуля, что означает год до нашей эры.
    :param val: Год для проверки
    :return: Корректный год
    :raises ValidationError: Ошибка проверки корректности года
    """
    try:
        year = int(val)
    except ValueError:
        raise ValidationError("The year must be an integer.")

    now_year = datetime.now().year
    if year > now_year:
        raise ValidationError("The year cannot be longer than the current year.")
    return year

def validation_status(val: bool | BookStatus) -> bool:
    """
    Проверяет переданный статус книги
    :param val: Статус книги
    :return: Корректный статус
    :raises ValidationError: Ошибка проверки статуса
    """
    if isinstance(val, BookStatus):
        status = val.value
    elif not isinstance(val, bool):
        raise ValidationError("The status must be a logical value.")
    else:
        status = val
    return status