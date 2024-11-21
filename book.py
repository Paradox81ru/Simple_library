
class Book:
    """ Класс книги """
    def __init__(self, _id: int, title: str, author: str, year: int, status: bool):
        """
        Конструктор класса книги
        :param _id: идентификатор
        :param title: название книги
        :param author: автор
        :param year: год издания
        :param status: статус книги, если True, то 'в наличии', иначе 'выдана'
        """
        self._id = _id
        self._title = title
        self._author = author
        self._year = year
        self._status = status

    @property
    def id(self):
        """ Идентификатор """
        return self._id

    @property
    def title(self):
        """ Название книги """
        return self._title

    @property
    def author(self):
        """ Автор """
        return self._author

    @property
    def year(self):
        """ Год издания """
        return self._year

    @property
    def status(self):
        """ Статус книги """
        return self._status

    def __str__(self):
        return f"Book {self._id}."

    def __repr__(self):
        return f"Book({self._id}, {self._title}, {self._author}, {self._year}, {self._status})"