from pathlib import Path
import json

from book import Book, BookStatus
from exceptions import BookRepositoryError


class BookRepository:
    """ Хранилище книг """
    def __init__(self, repository_filename):
        self._filename = repository_filename
        self._last_id = 0
        self._books: dict[id, Book] = {}

    def save(self):
        """ Сохраняет книги в файл """
        with open(self._filename, 'w') as f:
            json.dump()

    def load(self):
        """ Загружает книги из файла """

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

    def find_book_by_author(self, author: str) -> tuple[Book]:
        """ Поиск книг по автору """
        return tuple(filter(lambda b: b.author == author, self._books.values()))

    def find_book_by_title(self, title: str) -> tuple[Book]:
        """ Поиск книг по заголовку """
        return tuple(filter(lambda b: title in b.title, self._books.values()))

    def find_book_by_year(self, year: int) -> tuple[Book]:
        """ Поиск книг по году издания """
        return tuple(filter(lambda b: b.year == year, self._books.values()))

    def _to_json(self):
        """ Преобразует список всех книг в json строку """
        return f"[{','.join(book.to_json() for book in self.all_books)}]"

    def _from_json(self, data: str):
        """ Заполняет хранилище по json строке """
        obj_list = json.loads(data)
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

    def _check_filename(self):
        """ Проверяет наличие файла репозитория и создаёт при отсутствии """
        if not self._filename.exists():
            self._filename.touch()
