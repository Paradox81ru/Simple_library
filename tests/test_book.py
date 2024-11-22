import unittest

from book import Book, BookStatus
from book_repository import BookRepository


class BookTest(unittest.TestCase):
    """ Тестирование книги """
    def test_book_create_and_stringing(self):
        """ Тестирует создание книги и её строковое отображение """
        # Новая книга
        book = Book("Толковый словарь", "В.И. Даль", 1982)
        self.assertEqual(str(book), f"Book titled 'Толковый словарь' of the author В.И. Даль 1982 edition, "
                                    f"status given out")
        self.assertEqual(repr(book), f"Book('Толковый словарь', 'В.И. Даль', 1982)")
        self.assertEqual(book.id, 0)
        self.assertFalse(book.is_available)
        self.assertEqual(book.status.to_str(), 'given out')

        # Назначение книге идентификатора и изменение статуса.
        book.id = 2
        book.status = True
        self.assertEqual(str(book), f"Book id 2, titled 'Толковый словарь' of the author "
                                    f"В.И. Даль 1982 edition, status available")

    def test_edit_book(self):
        """ Тестирует изменение книги позитивный """
        tutle = "Толковый словарь"
        author = "В.И. Даль"
        year = 1982
        book = Book(tutle, author, year)
        self.assertEqual(book.id, 0)
        self.assertEqual(book.title, tutle)
        self.assertEqual(book.author, author)
        self.assertEqual(book.year, year)
        self.assertFalse(book.is_available)
        self.assertEqual(book.status.to_str(), 'given out')

        book.id = 3
        book.title = "Большой толковый словарь"
        book.author = "Владимир Иванович Даль"
        book.year = 2001
        book.status = BookStatus.AVAILABLE

        self.assertEqual(book.id, 3)
        self.assertEqual(book.title, "Большой толковый словарь")
        self.assertEqual(book.author, "Владимир Иванович Даль")
        self.assertEqual(book.year, 2001)
        self.assertTrue(book.is_available)
        self.assertEqual(book.status.to_str(), 'available')
        self.assertEqual(str(book), f"Book id 3, titled 'Большой толковый словарь' of the author "
                                    f"Владимир Иванович Даль 2001 edition, status available")

        # Изменение статуса логическим значением.
        book.status = False
        self.assertEqual(book.status.to_str(), 'given out')

    def test_edit_book_negative(self):
        """ Тестирует изменение книги негативный тест """
        with self.assertRaises(ValueError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", 2100)
        self.assertEqual(cm.exception.args[0], "The year cannot be longer than the current year")

        with self.assertRaises(ValueError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", 'aaaa')
        self.assertEqual(cm.exception.args[0], "The year must be an integer")

        book = Book("Толковый словарь", "В.И. Даль", 1982)
        self.assertEqual(book.id, 0)

        with self.assertRaises(ValueError) as cm:
            book.id = 'a'
        self.assertEqual(cm.exception.args[0], "The identifier must be an integer")

        with self.assertRaises(ValueError) as cm:
            book.id = 0
        self.assertEqual(cm.exception.args[0], "The ID must be greater than zero")

        with self.assertRaises(ValueError) as cm:
            book.id = -1
        self.assertEqual(cm.exception.args[0], "The ID must be greater than zero")

        with self.assertRaises(ValueError) as cm:
            book.year = 'ddd'
        self.assertEqual(cm.exception.args[0], "The year must be an integer")

        with self.assertRaises(ValueError) as cm:
            book.year = 2100
        self.assertEqual(cm.exception.args[0], "The year cannot be longer than the current year")

        with self.assertRaises(ValueError) as cm:
            book.status = 2
        self.assertEqual(cm.exception.args[0], "The status must be a logical value")