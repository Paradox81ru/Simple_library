from abstract_book_repository import AbstractBookRepository
from book import Book


class BookManager:
    """ Класс управление хранилищем книг """
    def __init__(self, book_repository: AbstractBookRepository):
        self._book_repository = book_repository

    def add_book(self, title: str, author: str, year: int) -> int:
        """
        Добавляет книгу в библиотеку
        :param title: название книги
        :param author: автор
        :param year: год издания
        :return: идентификатор книги
        :raises ValueError: Неправильно указан год издания книги
        """
        new_book = Book(title, author, year)
        self._book_repository.add_book(new_book)
        return new_book.id