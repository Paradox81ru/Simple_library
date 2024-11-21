import json
import datetime
from enum import Enum


class BookStatus(Enum):
    """ Статус книги в библиотеке """
    AVAILABLE = True
    GIVEN_OUT = False

    def to_str(self):
        return 'available' if self.value else 'given out'

    @classmethod
    def get_status(cls, status: bool):
        """ Возвращает статус по логическому значению """
        return cls.AVAILABLE if status else cls.GIVEN_OUT


class Book:
    """ Класс книги """
    def __init__(self, title: str, author: str, year: int):
        """
        Конструктор класса книги
        :param title: название книги
        :param author: автор
        :param year: год издания
        """
        self._id = 0
        self._title = title
        self._author = author
        self._year = year
        self._status: bool = False

    @property
    def id(self) -> int:
        """ Идентификатор книги """
        return self._id

    @id.setter
    def id(self, val: int):
        """ Идентификатор книги """
        try:
            val = int(val)
        except ValueError:
            raise ValueError("The identifier must be an integer")
        if val < 1:
            raise ValueError("The ID must be greater than zero")
        self._id = val

    @property
    def title(self) -> str:
        """ Название книги """
        return self._title

    @title.setter
    def title(self, val: str):
        """ Название книги """
        self._title = val

    @property
    def author(self) -> str:
        """ Автор """
        return self._author

    @author.setter
    def author(self, val: str):
        """ Автор """
        self._author = val

    @property
    def year(self) -> int:
        """ Год издания """
        return self._year

    @year.setter
    def year(self, val: int):
        """ Год издания """
        try:
            val = int(val)
        except ValueError:
            raise ValueError("The year must be an integer")
        now_year = datetime.datetime.now().year
        if val > now_year:
            raise ValueError("The year cannot be longer than the current year")
        self._year = val

    @property
    def status(self) -> BookStatus:
        """
        Статус книги
        :return: если True, то 'в наличии', иначе 'выдана'
        """
        return BookStatus.get_status(self._status)

    @status.setter
    def status(self, val: BookStatus | bool):
        """
        Статус книги
        :param val: если True, то 'в наличии', иначе 'выдана'
        """
        if isinstance(val, BookStatus):
            val = val.value
        self._status = val

    @property
    def is_available(self):
        """ Доступна ли книга """
        return self._status

    def to_dict(self):
        """ Преобразование данных в словарь """
        return self.__dict__

    def to_json(self):
        """ Сериализация данных в JSON """
        return json.dumps(self.__dict__)

    def __str__(self):
        _id = f"id {self._id}, " if self._id > 0 else ""
        return (f"Book {_id}titled '{self._title}' of the author {self._author} {self._year} edition, "
                f"{self.status.to_str()}")

    def __repr__(self):
        return f"Book('{self._title}', '{self._author}', {self._year})"
