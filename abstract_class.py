from abc import ABC, abstractmethod
from typing import Any

from book import Book, BookStatus


class AbstractBookRepositoryExport(ABC):
    """ Абстрактный класс экспорта и импорта данных """
    def __init__(self, book_repository: 'AbstractBookRepository'):
        """
        Конструктор класса
        :param book_repository: ХранилищеЮ, в которе производится импорт-экспорт.
        """
        self._book_repository = book_repository

    @abstractmethod
    def import_data(self) -> tuple[dict[int, dict[str: Any]], dict[int, bool]]:
        """
        Импортирует данные.
        :return: Возвращает кортеж, вначале список книг, а потом словарь статусов этих книг.
        """
        raise NotImplementedError()

    @abstractmethod
    def export_data(self, source_data: tuple[dict[int, dict[str: Any]], dict[int, bool]],
                    destination_data: tuple[dict[int, dict[str: Any]], dict[int, bool]]) -> int:
        """
        Заполняет хранилище из списка простых объектов.
        :param source_data: Данные для экспорта в виде кортежа: [book_list, status_dict].
        :param destination_data: Данные, куда данные экспортируются.
        :return: Последний номер идентификатора.
        :raises BookRepositoryExportException: Ошибка при экспорте данных
        """
        raise NotImplementedError()


class AbstractBookRepository(ABC):
    """ Абстрактный метод для хранилища книг. """
    def __init__(self):
        self._last_id = 0
        """"""
        self._books: dict[int, Book] = {}
        """ Книги. """
        self._books_status: dict[int, bool] = {}
        """ Статусы книги. """
        self._repository_export: AbstractBookRepository | None = None

    def set_repository_export(self, repository_export: AbstractBookRepositoryExport):
        """
        Устанавливает класс экспорта-импорта хранилища.
        :param repository_export: Класс экспорта импорта хранилища
        :return:
        """
        self._repository_export = repository_export

    @property
    @abstractmethod
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища. """
        raise NotImplementedError()

    @abstractmethod
    def save(self, filename) -> int:
        """
        Сохраняет книги в файл.
        :param filename:
        :return: Количество сохранённых книг.
        """
        raise NotImplementedError()

    @abstractmethod
    def load(self, filename) -> int:
        """
        Загружает книги из файла.
        :param filename:
        :return: Количество загруженных книг.
        :raises BookRepositoryError:
        :raises BookRepositoryExportException:
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def number_of_books(self) -> int:
        """ Количество книг в хранилище. """
        raise NotImplementedError()

    @abstractmethod
    def add_book(self, book: Book) -> int:
        """
        Добавляет книгу в хранилище.
        :param book: Добавляемая книга.
        :return: Идентификатор добавленной в хранилище книг книги.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_status_book(self, _id) -> BookStatus:
        """
        Возвращает статус книги
        :param _id:
        :return:
        :raises BookRepositoryError: Книга с указанным идентификатором отсутствует;
        """
        raise NotImplementedError()

    @abstractmethod
    def changing_status_book(self, _id: int, status: BookStatus) -> Book:
        """
        Изменяет статус книги.
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
        Удаляет книгу из хранилища.
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
        :param _id: Идентификатор книги, которую требуется вернуть.
        :return: Найденная по указанному идентификатору книга или None, если книги с таим идентификатором нет.
        :raises BookRepositoryError: Ошибка проверки корректности идентификатора.
        """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_author(self, author: str) -> tuple[Book]:
        """ Поиск книг по автору. """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_title(self, title: str) -> tuple[Book]:
        """ Поиск книг по заголовку. """
        raise NotImplementedError()

    @abstractmethod
    def find_book_by_year(self, year: int) -> tuple[Book]:
        """
        Поиск книг по году издания.
        :param year:
        :return:
        :raises BookRepositoryError: Ошибка при указании года выпуска книги.
        """
        raise NotImplementedError()
