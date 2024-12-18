from copy import copy
from pathlib import Path
import json
from typing import Any

from abstract_book_repository import AbstractBookRepository
from book import Book, BookStatus
from exceptions import BookRepositoryError, ValidationError, BookRepositoryExportException
from validation import validation_year, validation_id


class BookRepository(AbstractBookRepository):
    """ Хранилище книг """
    def __init__(self):
        self._last_id = 0
        self._books: dict[id, Book] = {}

    def save(self, filename) -> int:
        """
        Сохраняет книги в файл.
        Файл создаётся, только если хранилище не пустое.
        :param filename:
        :return: Количество сохранённых книг
        """
        # Сохранять книги надо только, если хранилище не пустое.
        if self.number_of_books == 0:
            return 0
        filename = Path(filename)
        with open(filename, 'w') as f:
            json.dump(self._import(), f)
        return self.number_of_books

    def load(self, filename) -> int:
        """
        Загружает книги из файла
        :param filename:
        :return: Количество загруженных книг
        :raises BookRepositoryError:
        :raises BookRepositoryExportException:
        """
        filename = Path(filename)
        if not filename.exists():
            raise BookRepositoryError(f"The file '{filename}' with the saved books was not found")
        with open(filename, 'r') as f:
            self._export(json.load(f))
        return self.number_of_books

    @property
    def number_of_books(self) -> int:
        """ Количество книг в хранилище """
        return len(self._books)

    @property
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища """
        return tuple(self._books.values())

    def add_book(self, book: Book) -> int:
        """
        Добавляет книгу в хранилище
        :param book: Добавляемая книга
        :return: Идентификатор добавленной в хранилище книги
        """
        self._last_id += 1
        book.id = self._last_id
        book.status = BookStatus.AVAILABLE
        self._books[self._last_id] = book
        return book.id

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
        self._is_repository_empty('changing status')
        try:
            book = self._books[_id]
            book.status = status
            return book
        except KeyError:
            raise BookRepositoryError(f"The book with the ID {_id} is missing.")
        except ValidationError as err:
            raise BookRepositoryError(err.message)

    def remove_book(self, _id: int) -> Book:
        """
        Удаляет книгу из хранилища
        :param _id: Идентификатор удаляемой книги.
        :return: Удалённая книга.
        :raises BookRepositoryError: Удалить книги невозможно, так как хранилище пустое;
                                     Книга с указанным идентификатором отсутствует.
        """
        self._is_repository_empty('delete')
        try:
            return self._books.pop(_id)
        except KeyError:
            raise BookRepositoryError(f"The book with the ID {_id} is missing.")

    def get_book_by_id(self, _id: int) -> Book | None:
        """
        Получение книги по её идентификатору
        :param _id: Идентификатор книги, которую требуется вернуть
        :return: Найденная по указанному идентификатору книга или None, если книги с таим идентификатором нет.
        :raises BookRepositoryError: Ошибка проверки корректности идентификатора
        """
        try:
            return self._books[validation_id(_id)]
        except ValidationError as err:
            raise BookRepositoryError(err.message)
        except KeyError:
            return None

    def find_book_by_author(self, author: str) -> tuple[Book, ...]:
        """ Поиск книг по автору """
        author = author.strip()
        return tuple(filter(lambda b: b.author == author, self._books.values()))

    def find_book_by_title(self, title: str) -> tuple[Book, ...]:
        """ Поиск книг по заголовку """
        title = title.strip().lower()
        # При пустом запросе должен вернуться пустой кортеж
        if title == "":
            return ()
        return tuple(filter(lambda b: title in b.title.lower(), self._books.values()))

    def find_book_by_year(self, year: int) -> tuple[Book, ...]:
        """
        Поиск книг по году издания
        :param year:
        :return:
        :raises BookRepositoryError: Ошибка при указании года выпуска книги
        """
        try:
            year = validation_year(year)
        except ValidationError as err:
            raise BookRepositoryError(err.message)
        return tuple(filter(lambda b: b.year == year, self._books.values()))

    def _import(self) -> list[dict[str: Any]]:
        """ Преобразует список всех книг в список простых объект """
        return [copy(book.to_dict()) for book in self.all_books]

    def _export(self, obj_list):
        """
        Заполняет хранилище из списка простых объектов
        :param obj_list:
        :raises BookRepositoryExportException: Ошибка при экспорте данных
        """
        last_id = 0
        i = 1
        try:
            for obj in obj_list:
                book = Book(obj['_title'], obj['_author'], obj['_year'])
                book.id = obj['_id']
                book.status = obj['_status']
                self._books[book.id] = book
                # Сразу же ищется самый последний (он же самый большой) идентификатор.
                if book.id > last_id:
                    last_id = book.id
                i += 1
        except ValidationError as err:
            self._books = {}
            raise BookRepositoryExportException(f"Error when exporting books number {i}. "
                                                f"{err.message}: {err.var_name} = {err.value}")
        except KeyError as err:
            raise BookRepositoryExportException(f"Error when exporting books number {i}. The {err.args[0][1:]} data is missing")
        self._last_id = last_id


    def _to_json(self) -> str:
        """ Преобразует список всех книг в json строку """
        return json.dumps(self._import())

    def _from_json(self, _json: str):
        """
        Заполняет хранилище по json строке
        :param _json:
        :raises BookRepositoryExportException: Ошибка при экспорте данных
        """
        self._export(json.loads(_json))

    def _is_repository_empty(self, action: str):
        """
        Проверка на пустое хранилище.
        :raises BookRepositoryError: Удалить книги невозможно, так как хранилище пустое
        """
        if self.number_of_books == 0:
            raise BookRepositoryError(f"It is impossible to {action} books because the repository is empty.")