from abc import ABC, abstractmethod

from book import Book


class AbstractBookRepository(ABC):
    """ Абстрактный метод для хранилища книг """

    @property
    @abstractmethod
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища """
        raise NotImplementedError()

    @abstractmethod
    def add_book(self, book: Book):
        """ Добавляет книгу в репозиторий """
        raise NotImplementedError()

    @abstractmethod
    def remove_book(self, _id: int):
        """
        Удаляет книгу из репозитория
        :param _id: идентификатор удаляемой книги
        :return: удалённая книга
        """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_author(self, author: str) -> tuple[Book]:
        """ Поиск книг по автору """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_title(self, title: str) -> tuple[Book]:
        """ Поиск книг по заголовку """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_year(self, year: int) -> tuple[Book]:
        """ Поиск книг по году издания """
        raise NotImplementedError()
