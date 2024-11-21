import unittest

from book_manager import BookManager
from book_repository import BookRepository


class BookRepositoryTest(unittest.TestCase):
    """ Тестирование управление хранилищем книг """
    def test_add_book(self):
        """ Проверяет добавление книг в репозиторий """
        book_manager = BookManager(BookRepository())
        _id = book_manager.add_book("Толковый словарь", "В.И. Даль", 1982)
        self.assertEqual(_id, 1)

        _id = book_manager.add_book("Ночной дозор", "Сергей Лукьяненко", 1998)
        self.assertEqual(_id, 2)

    def test_add_book_negative(self):
        """ Проверяет добавление книг в репозиторий негативный """
        book_manager = BookManager(BookRepository())
        with self.assertRaises(ValueError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", 2100)
        self.assertEqual(cm.exception.args[0], "The year cannot be longer than the current year")

        with self.assertRaises(ValueError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", "aaaa")
        self.assertEqual(cm.exception.args[0], "The year must be an integer")
