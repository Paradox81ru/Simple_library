from pathlib import Path
import json
from typing import Any

from abstract_book_repository import AbstractBookRepository
from book import Book, BookStatus
from exceptions import BookRepositoryError


class BookRepository(AbstractBookRepository):
    """ Хранилище книг """
    def __init__(self):
        self._last_id = 0
        self._books: dict[id, Book] = {}

    def save(self, filename: Path):
        """ Сохраняет книги в файл """
        with open(filename, 'w') as f:
            json.dump(self._to_obj(), f)

    def load(self, filename: Path):
        """ Загружает книги из файла """
        if not Path(filename).exists():
            raise BookRepositoryError(f"The file '{filename}' with the saved books was not found")
        with open(filename, 'r') as f:
            self._from_obj(json.load(f))

    @property
    def number_of_books(self) -> int:
        """ Количество книг в хранилище """
        return len(self._books)

    @property
    def all_books(self) -> tuple[Book, ...]:
        """ Возвращает всё книги из хранилища """
        return tuple(self._books.values())

    def add_book(self, book: Book):
        """ Добавляет книгу в репозиторий """
        self._last_id += 1
        book.id = self._last_id
        book.status = BookStatus.AVAILABLE
        self._books[self._last_id] = book

    def remove_book(self, _id: int):
        """
        Удаляет книгу из репозитория
        :param _id: идентификатор удаляемой книги
        :return: удалённая книга
        """
        if self.number_of_books == 0:
            raise BookRepositoryError("It is impossible to delete books because the repository is empty")
        try:
            return self._books.pop(_id)
        except KeyError:
            raise BookRepositoryError(f"The book with the ID {_id} is missing")

    def get_book_by_id(self, _id: int) -> Book | None:
        """
        Получение книги по её идентификатору
        :param _id: Идентификатор книги, которую требуется вернуть
        :return: Найденная по указанному идентификатору книга или None, если книги с таим идентификатором нет.
        """
        try:
            return self._books[_id]
        except KeyError:
            return None

    def find_book_by_author(self, author: str) -> tuple[Book]:
        """ Поиск книг по автору """
        return tuple(filter(lambda b: b.author == author, self._books.values()))

    def find_book_by_title(self, title: str) -> tuple[Book]:
        """ Поиск книг по заголовку """
        return tuple(filter(lambda b: title in b.title, self._books.values()))

    def find_book_by_year(self, year: int) -> tuple[Book]:
        """ Поиск книг по году издания """
        return tuple(filter(lambda b: b.year == year, self._books.values()))

    def _to_obj(self) -> list[dict[str: Any]]:
        """ Преобразует список всех книг в список простых объект """
        return [book.to_dict() for book in self.all_books]

    def _from_obj(self, obj_list):
        """ Заполняет хранилище из списка простых объектов """
        last_id = 0
        for obj in obj_list:
            book = Book(obj['_title'], obj['_author'], int(obj['_year']))
            book.id = int(obj['_id'])
            book.status = BookStatus.get_status(obj['_status'])
            self._books[book.id] = book
            # Сразу же ищется самый последний (он же самый большой) идентификатор.
            if book.id > last_id:
                last_id = book.id
        self._last_id = last_id

    def _to_json(self) -> str:
        """ Преобразует список всех книг в json строку """
        return json.dumps(self._to_obj())

    def _from_json(self, _json: str):
        """ Заполняет хранилище по json строке """
        self._from_obj(json.loads(_json))
