from abc import ABC, abstractmethod

from book import Book


class AbstractBookRepository(ABC):
    """ Абстрактный метод для хранилища книг """

    @property
    @abstractmethod
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища """
        raise NotImplementedError()

