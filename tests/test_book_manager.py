import unittest

from book_manager import BookManager
from book_repository import BookRepository
from enums import SearchCriteria
from exceptions import BookRepositoryError, BookManagerError


class BookRepositoryTest(unittest.TestCase):
    """ Тестирование управление хранилищем книг """
    def setUp(self):
        self.books_data = (("Толковый словарь", "В.И. Даль", 1982),
                      ("Ночной дозор", "Сергей Лукьяненко", 1998),
                      ("Дневной дозор", "Сергей Лукьяненко", 2000),
                      ("Звездные войны. Новая надежда", "Алан Дин Фостер.", 1976),
                      ("Звездные войны. Империя наносит ответный удар", "Дональд Ф", 1980),
                      ("Звездные войны. Возвращение джедая", "Джеймс Кан", 1983))

    def _get_repository_filled_with_books(self) -> tuple[BookManager, BookRepository]:
        """ Возвращает заполненное книгами хранилище и его менеджер книг """
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Репозиторий заполняется книгами.
        for book_data in self.books_data:
            book_manager.add_book(*book_data)
        return book_manager, book_repository

    def test_add_book(self):
        """ Проверяет добавление книг в репозиторий """
        book_manager = BookManager(BookRepository())

        # Добавляет книгу в репозиторий,
        _id = book_manager.add_book(*self.books_data[0])
        # и проверяет, что вернулся идентификатор добавленной книги.
        self.assertEqual(_id, 1)

        # Добавляет ещё одну книгу в репозиторий,
        _id = book_manager.add_book(*self.books_data[1])
        # и проверяет, что вернулся идентификатор новой добавленной книги.
        self.assertEqual(_id, 2)

    def test_add_book_negative(self):
        """ Проверяет добавление книг в репозиторий негативный """
        book_manager = BookManager(BookRepository())

        # Попытка добавить книгу с годом выпуска больше текущего.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", 2100)
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.args[0], "The year cannot be longer than the current year")

        # Попытка добавить книгу с годом выпуска в виде текста..
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", "aaaa")
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.args[0], "The year must be an integer")

    def test_remove_book(self):
        """ Проверяет удаление книги из репозитория через менеджер книг """
        book_manager, book_repository = self._get_repository_filled_with_books()

        number_of_books = len(self.books_data)
        # Проверка, что репозиторий заполнен книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Проверка, что книга с идентификатором 6 есть в хранилище.
        self.assertEqual(book_repository.get_book_by_id(6).id, 6)
        # Удаляется книга с идентификатором 6,
        _id = book_manager.remove_book(6)
        # и проверяется, что вернулся идентификатор удалённой книги.
        self.assertEqual(_id, 6)
        number_of_books -= 1
        # Далее проверка, что в хранилище на одну книгу меньше,
        self.assertEqual(book_repository.number_of_books, number_of_books)
        # и что книги с идентификатором 6 в хранилище нет.
        self.assertIsNone(book_repository.get_book_by_id(6))

        # Проверка, что книга с идентификатором 1 есть в хранилище.
        self.assertEqual(book_repository.get_book_by_id(1).id, 1)
        # Удаляется книга с идентификатором 1,
        _id = book_manager.remove_book(1)
        # и проверяется, что вернулся идентификатор удалённой книги.
        self.assertEqual(_id, 1)
        number_of_books -= 1
        # М снова проверка, что в хранилище на одну книгу меньше,
        self.assertEqual(book_repository.number_of_books, number_of_books)
        # и что книги с идентификатором 1 в хранилище нет.
        self.assertIsNone(book_repository.get_book_by_id(1))

        # Из хранилища удаляются все книги,
        for _id in range(2, 6):
            book_manager.remove_book(_id)
        # и проверка, что в хранилище действительно книг нет.
        self.assertEqual(book_repository.number_of_books, 0)

    def test_remove_book_negative(self):
        """ Проверяет удаление книг из репозитория через менеджер книг негативный"""
        # Создаётся пустое хранилище.
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Проверка ошибки, при попытке удалить книгу из пустого репозитория
        with self.assertRaises(BookManagerError) as cm:
            book_manager.remove_book(9)
        self.assertEqual(cm.exception.message, "It is impossible to delete books because the repository is empty")

        # Далее репозиторий заполняется книгами.
        for book_data in self.books_data:
            book_manager.add_book(*book_data)
        number_of_books = len(self.books_data)
        # Проверка, что репозиторий заполнен книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Попытка удалить книгу, идентификатора которого нет.
        with self.assertRaises(BookManagerError) as cm:
            book_manager.remove_book(10)
        self.assertEqual(cm.exception.message, f"The book with the ID 10 is missing")

    def test_find_books(self):
        """ Проверяет поиск книг """
        book_manager, book_repository = self._get_repository_filled_with_books()

        number_of_books = len(self.books_data)
        # Проверка, что репозиторий заполнен книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Поиск книг по автору.
        result = book_manager.find_book(SearchCriteria.SEARCH_AUTHOR, 'Сергей Лукьяненко')
        expected_result = ("Book id 2, titled 'Ночной дозор' of the author Сергей Лукьяненко 1998 edition, available\n"
                           "Book id 3, titled 'Дневной дозор' of the author Сергей Лукьяненко 2000 edition, available")
        self.assertEqual(result, expected_result)

        # Поиск книг по заголовку.
        result = book_manager.find_book(SearchCriteria.SEARCH_TITLE, "Звездные войны")
        expected_result = ("Book id 4, titled 'Звездные войны. Новая надежда' "
                           "of the author Алан Дин Фостер. 1976 edition, available\n"
                           "Book id 5, titled 'Звездные войны. Империя наносит ответный удар' "
                           "of the author Дональд Ф 1980 edition, available\n"
                           "Book id 6, titled 'Звездные войны. Возвращение джедая' "
                           "of the author Джеймс Кан 1983 edition, available")
        self.assertEqual(result, expected_result)

        # Поиск книг по году выпуска.
        result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 1982)
        expected_result = "Book id 1, titled 'Толковый словарь' of the author В.И. Даль 1982 edition, available"
        self.assertEqual(result, expected_result)

    def test_find_books_negative(self):
        """ Проверяет поиск книг негативный """
        book_manager, _ = self._get_repository_filled_with_books()

        # Проверка исключения при неверно указанном критерии поиска
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.find_book(8, "Звездные войны")
        self.assertEqual(cm.exception.message, "Invalid search criteria specified")

        # Проверка исключения при неверно указанном годе при поиске по году выпуска книги.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.find_book(SearchCriteria.SEARCH_YEAR, "dddd")
        self.assertEqual(cm.exception.message, "The year must be an integer")
