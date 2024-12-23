import json
from dataclasses import dataclass

from enums import BookStatus
from validation import validation_id, validation_year, validation_status, validation_title, validation_author


class Book:
    """ Класс книги. """
    def __init__(self, title: str, author: str, year: int):
        """
        Конструктор класса книги.
        :param title: Название книги.
        :param author: Автор.
        :param year: Год издания.
        :raises ValidationError: Ошибка при указании заголовка, автора или года выпуска книги.
        """
        self._id = 0
        self._title = validation_title(title)
        self._author = validation_author(author)
        self._year = validation_year(year)

    @property
    def id(self) -> int:
        """ Идентификатор книги. """
        return self._id

    def set_id(self, val: int):
        """
        Устанавливает идентификатор книги.
        :param val:
        :raises ValidationError: Ошибка проверки корректности идентификатора.
        """
        self._id = validation_id(val)

    @property
    def title(self) -> str:
        """ Название книги. """
        return self._title

    @property
    def author(self) -> str:
        """ Автор """
        return self._author

    @property
    def year(self) -> int:
        """ Год издания. """
        return self._year

    def to_dict(self):
        """ Преобразование данных в словарь. """
        return self.__dict__

    def to_json(self):
        """ Сериализация данных в JSON. """
        return json.dumps(self.__dict__)

    def __str__(self):
        _id = f"id {self._id}, " if self._id > 0 else ""
        return (f"Book {_id}titled '{self._title}' of the author {self._author} {self._year} edition")

    def __repr__(self):
        return f"Book('{self._title}', '{self._author}', {self._year})"
