import unittest

from book import Book, BookStatus
from exceptions import ValidationError


class BookTest(unittest.TestCase):
    """ Тестирование книги """
    def test_book_create_and_stringing(self):
        """ Тестирует создание книги и её строковое отображение. """
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
        """ Тестирует изменение книги позитивный. """
        title = "Толковый словарь"
        author = "В.И. Даль"
        year = 1982
        book = Book(title, author, year)
        self.assertEqual(book.id, 0)
        self.assertEqual(book.title, title)
        self.assertEqual(book.author, author)
        self.assertEqual(book.year, year)
        self.assertFalse(book.is_available)
        self.assertEqual(book.status.to_str(), 'given out')

        # Создание книги с годом в виде дробного значения.
        book = Book(title, author, 1801.3)
        self.assertEqual(book.id, 0)
        self.assertEqual(book.title, title)
        self.assertEqual(book.author, author)
        # Дробное значение книги преобразовалось в целое число.
        self.assertEqual(book.year, 1801)
        self.assertFalse(book.is_available)
        self.assertEqual(book.status.to_str(), 'given out')

        # Создание книги с годом в виде числа, но в текстовом виде.
        book = Book(title, author, '1801')
        self.assertEqual(book.id, 0)
        self.assertEqual(book.title, title)
        self.assertEqual(book.author, author)
        # Дробное значение книги преобразовалось в целое число.
        self.assertEqual(book.year, 1801)
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

        # Дробное значение идентификатора преобразуется в целое число.
        book.id = 5.9
        self.assertEqual(book.id, 5)

        # Текстовое значение числа идентификатора преобразуется в целое число.
        book.id ='8'
        self.assertEqual(book.id, 8)

        # Дробное значение года преобразуется в целое число.
        book.year = 1999.7
        self.assertEqual(book.year, 1999)

        # Текстовое значение числа года преобразуется в целое число.
        book.year = '1800'
        self.assertEqual(book.year, 1800)

        # Изменение статуса логическим значением.
        book.status = False
        self.assertEqual(book.status.to_str(), 'given out')

    def test_edit_book_negative(self):
        """ Тестирует изменение книги негативный тест. """
        # Попытка создание книги со слишком коротким заголовком.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("То", "В.И. Даль", 1988)
        self.assertEqual(cm.exception.message,
                         "The length of the book title should be from 3 to 50 characters.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('title', 'То'))

        # Попытка создание книги со слишком коротким автором.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "В", 1988)
        self.assertEqual(cm.exception.message,
                         "The length of the book author should be from 2 to 25 characters.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('author', 'В'))

        # Попытка создание книги со слишком длинным автором.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "абвгдуёжзиклмнопрстуфхцчшщ", 1988)
        self.assertEqual(cm.exception.message,
                         "The length of the book author should be from 2 to 25 characters.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('author', 'абвгдуёжзиклмнопрстуфхцчшщ'))

        # Попытка создание книги с пустым годом издания.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", '')
        self.assertEqual(cm.exception.message, "The year must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', ''))

        # Попытка создание книги с годом больше текущего.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", 2100)
        self.assertEqual(cm.exception.message, "The year cannot be longer than the current year.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', 2100))

        # Попытка создание книги с текстом вместо года издания.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", 'aaaa')
        self.assertEqual(cm.exception.message, "The year must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', 'aaaa'))

        # Попытка создание книги с дробными значением года в текстовом виде.
        with self.assertRaises(ValidationError) as cm:
            _ = Book("Толковый словарь", "В.И. Даль", '1988.8')
        self.assertEqual(cm.exception.message, "The year must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', '1988.8'))

        # Создаётся корректная книга для дальнейшей проверки.
        book = Book("Толковый словарь", "В.И. Даль", 1982)
        self.assertEqual(book.id, 0)

        # Попытка изменение книге идентификатор на текстовое значение.
        with self.assertRaises(ValidationError) as cm:
            book.id = 'a'
        self.assertEqual(cm.exception.message, "The identifier must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('id', 'a'))

        # Попытка изменения книге идентификатор на дробное значение, но в текстовом виде.
        with self.assertRaises(ValidationError) as cm:
            book.id = '8.1'
        self.assertEqual(cm.exception.message, "The identifier must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('id', '8.1'))

        # Попытка изменение книге идентификатор на ноль.
        with self.assertRaises(ValidationError) as cm:
            book.id = 0
        self.assertEqual(cm.exception.message, "The identifier must be greater than zero.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('id', 0))

        # Попытка изменение книге идентификатор на дробное значение между нулём и единицей.
        with self.assertRaises(ValidationError) as cm:
            book.id = 0.9
        self.assertEqual(cm.exception.message, "The identifier must be greater than zero.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('id', 0.9))

        # Попытка изменение книге идентификатор на отрицательное значение.
        with self.assertRaises(ValidationError) as cm:
            book.id = -1
        self.assertEqual(cm.exception.message, "The identifier must be greater than zero.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('id', -1))

        # Попытка изменение книге года на текстовое значение.
        with self.assertRaises(ValidationError) as cm:
            book.year = 'ddd'
        self.assertEqual(cm.exception.message, "The year must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', 'ddd'))

        # Попытка установить год в виде текстового дробного числа.
        with self.assertRaises(ValidationError) as cm:
            book.year = '1988.5'
        self.assertEqual(cm.exception.message, "The year must be an integer.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', '1988.5'))

        # Попытка установить год больше текущего года.
        with self.assertRaises(ValidationError) as cm:
            book.year = 2100
        self.assertEqual(cm.exception.message, "The year cannot be longer than the current year.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('year', 2100))

        # Попытка установить неправильное значение статуса.
        with self.assertRaises(ValidationError) as cm:
            book.status = 2
        self.assertEqual(cm.exception.message, "The status must be a logical value.")
        self.assertEqual((cm.exception.var_name, cm.exception.value), ('status', 2))