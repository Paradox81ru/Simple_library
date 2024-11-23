from datetime import datetime
from typing import final

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
        raise ValidationError("The identifier must be an integer.", 'id', val)

    if _id < 1:
        raise ValidationError("The identifier must be greater than zero.", 'id', val)

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
        raise ValidationError("The year must be an integer.", 'year', val)

    now_year = datetime.now().year
    if year > now_year:
        raise ValidationError("The year cannot be longer than the current year.", 'year', val)
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
        raise ValidationError("The status must be a logical value.", 'status', val)
    else:
        status = val
    return status

def validation_title(val: str):
    """
    Проверяет переданное значение заголовка
    :param val: Заголовок книги
    :return:
    :raises ValidationError: Ошибка проверки заголовка
    """
    _min: final = 3
    _max: final = 50
    title = val.strip()
    if len(title) < _min or len(title) > _max:
        raise ValidationError(f"The length of the book title should be from {_min} to {_max} characters.", 'title', title)
    return title

def validation_author(val: str):
    """
    Проверяет переданное значение автора
    :param val: Автор книги
    :return:
    :raises ValidationError: Ошибка проверки автора
    """
    _min: final = 2
    _max: final = 25
    author = val.strip()
    if len(author) < _min or len(author) > _max:
        raise ValidationError(f"The length of the book author should be from {_min} to {_max} characters.", 'author', author)
    return author