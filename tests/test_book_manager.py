import re
import unittest

from book import BookStatus
from book_manager import BookManager
from book_repository import BookRepository
from enums import SearchCriteria
from exceptions import BookManagerError


class BookRepositoryTest(unittest.TestCase):
    """ Тестирование управление хранилищем книг """
    def setUp(self):
        self.books_data = (("Толковый словарь", "В.И. Даль", 1982),
                           ("Ночной дозор", "Сергей Лукьяненко", 1998),
                           ("Дневной дозор", "Сергей Лукьяненко", 2000),
                           ("Звездные войны. Новая надежда", "Алан Дин Фостер", 1976),
                           ("Звездные войны. Империя наносит ответный удар", "Дональд Ф.", 1980),
                           ("Звездные войны. Возвращение джедая", "Джеймс Кан", 1983))

    def _get_repository_filled_with_books(self) -> tuple[BookManager, BookRepository]:
        """ Возвращает заполненное книгами хранилище и его менеджер книг """
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Хранилище заполняется книгами.
        for book_data in self.books_data:
            book_manager.add_book(*book_data)
        return book_manager, book_repository

    def test_add_book(self):
        """ Проверяет добавление книг в хранилище """
        book_manager = BookManager(BookRepository())

        # Добавляет книгу в хранилище,
        _id = book_manager.add_book(*self.books_data[0])
        # и проверяет, что вернулся идентификатор добавленной книги.
        self.assertEqual(_id, 1)

        # Добавляет ещё одну книгу в хранилище,
        _id = book_manager.add_book(*self.books_data[1])
        # и проверяет, что вернулся идентификатор новой добавленной книги.
        self.assertEqual(_id, 2)

    def test_add_book_negative(self):
        """ Проверяет добавление книг в хранилище негативный """
        book_manager = BookManager(BookRepository())

        # Попытка добавить книгу со слишком коротким заголовком.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("То", "В.И. Даль", 1982)
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The length of the book title should be from 3 to 50 characters.")

        # Попытка добавить книгу со слишком коротким автором.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В", 1982)
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The length of the book author should be from 2 to 25 characters.")

        # Попытка добавить книгу со слишком длинным автором.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "абвгдуёжзиклмнопрстуфхцчшщ", 1982)
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The length of the book author should be from 2 to 25 characters.")

        # Попытка добавить книгу с годом выпуска больше текущего.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", 2100)
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The year cannot be longer than the current year.")

        # Попытка добавить книгу с текстом вместо года издания.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", "aaaa")
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The year must be an integer.")

        # Попытка добавить книгу с дробными значением года издания, но в текстовом виде.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.add_book("Толковый словарь", "В.И. Даль", "2001.3")
        # Проверка текста возникшей при этом ошибки.
        self.assertEqual(cm.exception.message, "The year must be an integer.")

    def test_remove_book(self):
        """ Проверяет удаление книги из хранилища через менеджер книг """
        book_manager, book_repository = self._get_repository_filled_with_books()

        number_of_books = len(self.books_data)
        # Проверка, что хранилище заполнено книгами.
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
        """ Проверяет удаление книг из хранилища через менеджер книг негативный"""
        # Создаётся пустое хранилище.
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Проверка ошибки, при попытке удалить книгу из пустого хранилища.
        with self.assertRaises(BookManagerError) as cm:
            book_manager.remove_book(9)
        self.assertEqual(cm.exception.message, "It is impossible to delete books because the repository is empty.")

        # Далее хранилище заполняется книгами.
        for book_data in self.books_data:
            book_manager.add_book(*book_data)
        number_of_books = len(self.books_data)
        # Проверка, что хранилище заполнено книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Попытка удалить книгу, идентификатора которого нет.
        with self.assertRaises(BookManagerError) as cm:
            book_manager.remove_book(10)
        self.assertEqual(cm.exception.message, f"The book with the ID 10 is missing.")

    def test_find_books(self):
        """ Проверяет поиск книг """
        book_manager, book_repository = self._get_repository_filled_with_books()

        number_of_books = len(self.books_data)
        # Проверка, что хранилище заполнена книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Получение информации о книге по её идентификатору.
        result = book_manager.get_book_info_by_id(1)
        expected_result = "Book id 1, titled 'Толковый словарь' of the author В.И. Даль 1982 edition, status available"
        self.assertEqual(result, expected_result)

        # Поиск книг по автору.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_AUTHOR, 'Сергей Лукьяненко')
        expected_result = ("Book id 2, titled 'Ночной дозор' of the author Сергей Лукьяненко 1998 edition, "
                           "status available\n"
                           "Book id 3, titled 'Дневной дозор' of the author Сергей Лукьяненко 2000 edition, "
                           "status available")
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 2)

        # Поиск книг по заголовку.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_TITLE, "Звездные войны")
        expected_result = ("Book id 4, titled 'Звездные войны. Новая надежда' "
                           "of the author Алан Дин Фостер 1976 edition, status available\n"
                           "Book id 5, titled 'Звездные войны. Империя наносит ответный удар' "
                           "of the author Дональд Ф. 1980 edition, status available\n"
                           "Book id 6, titled 'Звездные войны. Возвращение джедая' "
                           "of the author Джеймс Кан 1983 edition, status available")
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 3)

        # Поиск книг по году выпуска.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 1982)
        expected_result = "Book id 1, titled 'Толковый словарь' of the author В.И. Даль 1982 edition, status available"
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 1)

        # Поиск книг по году выпуска указанному в текстовом виде.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, '1983')
        expected_result = "Book id 6, titled 'Звездные войны. Возвращение джедая' of the author Джеймс Кан 1983 edition, status available"
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 1)

        # Поиск книг по году выпуска указанному в дробном виде.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 1980.9)
        expected_result = "Book id 5, titled 'Звездные войны. Империя наносит ответный удар' of the author Дональд Ф. 1980 edition, status available"
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 1)

    def test_not_find_books(self):
        """ Проверяет ненахождения книг """
        # Создаётся пустое хранилище.
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # В пустом хранилище информация о книге по ID получена не будет, вернётся None.
        result = book_manager.get_book_info_by_id(1)
        self.assertIsNone(result)

        expected_result = "Nothing was found for your query"
        # Проверяется, что в пустом хранилище ничего не находится.
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_AUTHOR, 'Сергей Лукьяненко')
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)

        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_TITLE, 'Звездные войны')
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)

        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 1982)
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)

        # Далее создаётся заполненное книгами хранилище.
        book_manager, book_repository = self._get_repository_filled_with_books()
        # Проверка, что хранилище заполнено книгами.
        self.assertEqual(book_repository.number_of_books, len(self.books_data))

        # При попытке получить информацию по ID о несуществующую книге, вернётся None.
        result = book_manager.get_book_info_by_id(9)
        self.assertIsNone(result)

        # Проверяется, что несуществующие книги в хранилище не находятся.
        expected_result = "Nothing was found for your query"
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_AUTHOR, "Джон Р. Р. Толкин")
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_TITLE, "Властелин колец")
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)
        books_num, result = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 1955)
        self.assertEqual(result, expected_result)
        self.assertEqual(books_num, 0)



    def test_find_books_negative(self):
        """ Проверяет поиск книг негативный """
        book_manager, _ = self._get_repository_filled_with_books()

        # Проверяет исключение при попытке получить информацию о книге по-нулевому ID.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.get_book_info_by_id(0)
        self.assertEqual(cm.exception.message, "The identifier must be greater than zero.")

        # Проверяет исключение при попытке получить информацию о книге по-отрицательному ID.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.get_book_info_by_id(-1)
        self.assertEqual(cm.exception.message, "The identifier must be greater than zero.")

        # Проверяет исключение при попытке получить информацию о книге по ID строке
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.get_book_info_by_id('q')
        self.assertEqual(cm.exception.message, "The identifier must be an integer.")

        # Проверка исключения при неверно указанном критерии поиска
        with self.assertRaises(BookManagerError) as cm:
            _, _ = book_manager.find_book(8, "Звездные войны")
        self.assertEqual(cm.exception.message, "Invalid search criteria specified")

        # Проверка исключения при неверно указанном годе при поиске по году выпуска книги.
        with self.assertRaises(BookManagerError) as cm:
            _, _ = book_manager.find_book(SearchCriteria.SEARCH_YEAR, "dddd")
        self.assertEqual(cm.exception.message, "The year must be an integer.")

        # Проверка исключения при попытке поиска книги по году выпуска указанному в виде дроби, то в текстовом виде.
        with self.assertRaises(BookManagerError) as cm:
            _, _ = book_manager.find_book(SearchCriteria.SEARCH_YEAR, "1703.1")
        self.assertEqual(cm.exception.message, "The year must be an integer.")

        # Проверка исключения при неверно указанном годе при поиске по году выпуска книги.
        with self.assertRaises(BookManagerError) as cm:
            _, _ = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 2111)
        self.assertEqual(cm.exception.message, "The year cannot be longer than the current year.")

    def test_get_all_books(self):
        """ Проверяет отображение всех книг из хранилища """
        # Создаётся пустое хранилище
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Проверка сообщения при запросе всех книг из пустого хранилища,
        books_num, result = book_manager.get_all_books()
        self.assertEqual(result, "There are no books to display in the storage")
        # а также нулевое значение всех книг.
        self.assertEqual(books_num, 0)

        # Теперь создаётся заполненное хранилище книг.
        book_manager, book_repository = self._get_repository_filled_with_books()
        books_num, result = book_manager.get_all_books()
        expected_result = """Book id 1, titled 'Толковый словарь' of the author В.И. Даль 1982 edition, status available
Book id 2, titled 'Ночной дозор' of the author Сергей Лукьяненко 1998 edition, status available
Book id 3, titled 'Дневной дозор' of the author Сергей Лукьяненко 2000 edition, status available
Book id 4, titled 'Звездные войны. Новая надежда' of the author Алан Дин Фостер 1976 edition, status available
Book id 5, titled 'Звездные войны. Империя наносит ответный удар' of the author Дональд Ф. 1980 edition, status available
Book id 6, titled 'Звездные войны. Возвращение джедая' of the author Джеймс Кан 1983 edition, status available"""
        # Проверка строки всех книг,
        self.assertEqual(result, expected_result)
        # и значения общего количества книг в хранилище.
        self.assertEqual(books_num, 6)

    def test_changing_book_status(self):
        """ Проверяет изменение статуса книги """
        book_manager, _ = self._get_repository_filled_with_books()
        # Ищется книга по году 2000, для удобства такая в хранилище сейчас одна.
        books_str = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 2000)
        _id, status = self._get_id_and_status_from_book_str(books_str[1])
        # Запоминается её идентификатор, и фиксируется статус, сейчас она в наличии.
        self.assertEqual(_id, 3)
        self.assertEqual(status, 'available')

        # Изменяется статус книги по запомненному идентификатору.
        book_manager.changing_status_book(_id, BookStatus.GIVEN_OUT)
        # Снова поиск той же книги по году 2000.
        books_str = book_manager.find_book(SearchCriteria.SEARCH_YEAR, 2000)
        _id, status = self._get_id_and_status_from_book_str(books_str[1])
        # Сверяется её идентификатор, и проверяется, что её статус изменился.
        self.assertEqual(_id, 3)
        self.assertEqual(status, 'given out')

    def test_changing_book_status_negative(self):
        """ Проверяет изменение статуса книги """
        # Создаётся пустое хранилище.
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)

        # Проверка исключения при попытке изменить статус в пустом хранилище
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.changing_status_book(2, BookStatus.GIVEN_OUT)
        self.assertEqual(cm.exception.message,
                         "It is impossible to changing status books because the repository is empty.")

        # Далее создаётся хранилище заполненное книгами.
        book_manager, _ = self._get_repository_filled_with_books()
        # Проверка исключения при попытке изменить статус несуществующей книге.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.changing_status_book(10, BookStatus.GIVEN_OUT)
        self.assertEqual(cm.exception.message, "The book with the ID 10 is missing.")

        # Проверка исключения при попытке изменить статус на неправильный.
        with self.assertRaises(BookManagerError) as cm:
            _ = book_manager.changing_status_book(2, 3)
        self.assertEqual(cm.exception.message, "The status must be a logical value.")

    # noinspection PyMethodMayBeStatic
    def _get_id_and_status_from_book_str(self, book_str):
        """
        Выделяет из строкового обозначения книги её идентификатор и статус
        :param book_str:
        :return: Кортеж в формате (Идентификатор, статус)
        """
        pattern = r".*id\s(\d+).*status\s([\w\s]+)"
        match = re.findall(pattern, book_str)
        result = match[0]
        return int(result[0]), result[1]
