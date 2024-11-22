from abc import ABC, abstractmethod
from pathlib import Path

from book import Book, BookStatus


class AbstractBookRepository(ABC):
    """ Абстрактный метод для хранилища книг """

    @property
    @abstractmethod
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища """
        raise NotImplementedError()

    @abstractmethod
    def save(self, filename) -> int:
        """
        Сохраняет книги в файл
        :param filename:
        :return: Количество сохранённых книг
        """
        raise NotImplementedError()

    @abstractmethod
    def load(self, filename) -> int:
        """
        Загружает книги из файла
        :param filename:
        :return: Количество загруженных книг
        """
        raise NotImplementedError()

    @abstractmethod
    def add_book(self, book: Book) -> int:
        """
        Добавляет книгу в репозиторий
        :param book: Добавляемая книга
        :return: идентификатор добавленной в репозиторий книги
        """
        raise NotImplementedError()

    @abstractmethod
    def changing_status_book(self, _id: int, status: BookStatus) -> Book:
        """
        Изменяет статус книги
        :param _id: Идентификатор книги, статус которой надо изменить.
        :param status: Новый статус книги.
        :return: Книга с изменённым статусом.
        :raises BookRepositoryError: Изменить статус книги невозможно, так как хранилище пустое;
                                     Книга с указанным идентификатором отсутствует;
                                     Статус должен быть логическим значением.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_book(self, _id: int) -> Book:
        """
        Удаляет книгу из репозитория
        :param _id: Идентификатор удаляемой книги.
        :return: Удалённая книга.
        :raises BookRepositoryError: Удалить книги невозможно, так как хранилище пустое;
                                     Книга с указанным идентификатором отсутствует.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_book_by_id(self, _id: int) -> Book | None:
        """
        Получение книги по её идентификатору
        :param _id: Идентификатор книги, которую требуется вернуть
        :return: Найденная по указанному идентификатору книга или None, если книги с таим идентификатором нет.
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
        """
        Поиск книг по году издания
        :param year:
        :return:
        :raises BookRepositoryError: Ошибка при указании года выпуска книги
        """
        raise NotImplementedError()
