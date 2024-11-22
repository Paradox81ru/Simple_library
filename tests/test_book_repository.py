import unittest
import json
from pathlib import Path

from book import Book, BookStatus
from book_repository import BookRepository
from exceptions import BookRepositoryError
import tempfile


class BookRepositoryTest(unittest.TestCase):
    """ Тестирование хранилища книг """

    def setUp(self):
        self.books = (Book("Толковый словарь", "В.И. Даль", 1982),
                      Book("Ночной дозор", "Сергей Лукьяненко", 1998),
                      Book("Дневной дозор", "Сергей Лукьяненко", 2000),
                      Book("Звездные войны. Новая надежда", "Алан Дин Фостер.", 1976),
                      Book("Звездные войны. Империя наносит ответный удар", "Дональд Ф", 1980),
                      Book("Звездные войны. Возвращение джедая", "Джеймс Кан", 1983))

    def _get_repository_filled_with_books(self) -> BookRepository:
        """ Возвращает заполненное книгами хранилище """
        book_repository = BookRepository()
        # Репозиторий заполняется книгами
        for book in self.books:
            book_repository.add_book(book)
        return book_repository

    def test_add_book(self):
        """ Проверяет добавление книг в репозиторий """
        book_repository = BookRepository()
        self.assertEqual(book_repository.number_of_books, 0)
        book_1 = self.books[0]

        # В репозиторий добавляется книга,
        book_repository.add_book(book_1)
        # и проверяется, что она действительно была добавлена
        self.assertEqual(book_repository.number_of_books, 1)
        self.assertGreater(book_1.id, 0)
        self.assertTrue(book_1.status.value)

        book_2 = self.books[1]

        # В репозиторий добавляется вторая книга,
        book_repository.add_book(book_2)
        # и проверяется, что она действительно была добавлена
        self.assertEqual(book_repository.number_of_books, 2)

        for i, book in enumerate(self.books[2:], start=3):
            book_repository.add_book(book)
            self.subTest(f"{book.author} - {book.title}")
            self.assertEqual(book_repository.number_of_books, i)

    def test_remove_book(self):
        """ Проверяет удаление книг из репозитория """
        book_repository = self._get_repository_filled_with_books()
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Проверка, что книга с идентификатором 6 есть в хранилище.
        self.assertEqual(book_repository.get_book_by_id(6).id, 6)
        # Удаляется книга с идентификатором 6,
        remove_book = book_repository.remove_book(6)
        # и проверка, что вернулась именно удалённая книга.
        self.assertEqual(remove_book.id, 6)
        number_of_books -= 1
        # Далее проверка, что в хранилище на одну книгу меньше,
        self.assertEqual(book_repository.number_of_books, number_of_books)
        # и что книги с идентификатором 6 в хранилище нет.
        self.assertIsNone(book_repository.get_book_by_id(6))

        # Проверка, что книга с идентификатором 1 есть в хранилище.
        self.assertEqual(book_repository.get_book_by_id(1).id, 1)
        # Ещё одна книга удаляется, на этот раз с ID 1,
        remove_book = book_repository.remove_book(1)
        # и проверка, что вернулась именно удалённая книга.
        self.assertEqual(remove_book.id, 1)
        number_of_books -= 1
        # М снова проверка, что в хранилище на одну книгу меньше,
        self.assertEqual(book_repository.number_of_books, number_of_books)
        # и что на этот раз в хранилище уже нет книги с идентификатором 1.
        self.assertIsNone(book_repository.get_book_by_id(1))

        # Из хранилища удаляются все книги,
        for _id in range(2, 6):
            book_repository.remove_book(_id)
        # и проверка, что в хранилище действительно книг нет.
        self.assertEqual(book_repository.number_of_books, 0)

    def test_remove_book_negative(self):
        """ Проверяет удаление книг из репозитория негативный"""
        # Создаётся пустое хранилище.
        book_repository = BookRepository()
        # Проверка ошибки, при попытке удалить книгу из пустого хранилища.
        with self.assertRaises(BookRepositoryError) as cm:
            book_repository.remove_book(9)
        self.assertEqual(cm.exception.message, "It is impossible to delete books because the repository is empty")

        # Далее хранилище заполняется книгами.
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
        number_of_books = len(self.books)
        # Проверка, что хранилище заполнено книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Попытка удалить книгу, идентификатора которого нет.
        with self.assertRaises(BookRepositoryError) as cm:
            book_repository.remove_book(10)
        self.assertEqual(cm.exception.message, f"The book with the ID 10 is missing")

    def test_find_books(self):
        """ Проверяет поиск книг """
        book_repository = self._get_repository_filled_with_books()
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Поиск книг по автору.
        books = book_repository.find_book_by_author("Сергей Лукьяненко")
        # Проверка, что найдено две книги
        self.assertEqual(len(books), 2)
        self.assertEqual(tuple(book.author for book in books), ("Сергей Лукьяненко", "Сергей Лукьяненко"))

        # Поиск книг по заголовку.
        books = book_repository.find_book_by_title("Звездные войны")
        # Проверка, что найдено три книги
        self.assertEqual(len(books), 3)
        expected_book_list = ("Звездные войны. Новая надежда",
                              "Звездные войны. Империя наносит ответный удар",
                              "Звездные войны. Возвращение джедая")
        self.assertEqual(tuple(book.title for book in books), expected_book_list)

        # Поиск книг по году издания.
        books = book_repository.find_book_by_year(1982)
        # Проверка, что найдена одна книга.
        self.assertEqual(len(books), 1)
        self.assertEqual("Толковый словарь", books[0].title)

    def test_not_find_books(self):
        """ Проверяет ненахождения книг """
        book_repository = BookRepository()

        # Проверка, что репозиторий пустой
        self.assertEqual(book_repository.number_of_books, 0)

        # Проверяется, что в пустом репозитории ничего не находится.
        books = book_repository.find_book_by_author("Сергей Лукьяненко")
        self.assertEqual(books, ())
        books = book_repository.find_book_by_title("Звездные войны")
        self.assertEqual(books, ())
        books = book_repository.find_book_by_year(1982)
        self.assertEqual(books, ())

        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Проверяется, что несуществующие книги в репозитории не находится.
        books = book_repository.find_book_by_author("Джон Р. Р. Толкин")
        self.assertEqual(books, ())
        books = book_repository.find_book_by_title("Властелин колец")
        self.assertEqual(books, ())
        books = book_repository.find_book_by_year(1955)
        self.assertEqual(books, ())

    def test_find_books_negative(self):
        """ Проверяет поиск книг негативный """
        book_repository = BookRepository()

        # Проверяет исключение при попытке поиска книги по неправильно введённому году выпуска
        with self.assertRaises(BookRepositoryError) as cm:
            _ = book_repository.find_book_by_year('dddd')
        self.assertEqual(cm.exception.message, "The year must be an integer")

    def test_get_all_books(self):
        """ Проверяет возвращение всех книг из репозитория """
        book_repository = self._get_repository_filled_with_books()
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами
        self.assertEqual(book_repository.number_of_books, number_of_books)

        books = book_repository.all_books
        self.assertEqual(len(books), 6)
        expected_book_list = (
            "Толковый словарь",
            "Ночной дозор",
            "Дневной дозор",
            "Звездные войны. Новая надежда",
            "Звездные войны. Империя наносит ответный удар",
            "Звездные войны. Возвращение джедая")
        self.assertSequenceEqual(tuple(book.title for book in books), expected_book_list)

    def test_changing_book_status(self):
        """ Проверяет изменение статуса книги """
        book_repository = self._get_repository_filled_with_books()

        book = book_repository.get_book_by_id(2)
        # Проверка, что книга доступна
        self.assertEqual(book.status, BookStatus.AVAILABLE)

        # Изменяется статус книги.
        changed_book = book_repository.changing_status_book(2, BookStatus.GIVEN_OUT)
        self.assertEqual(changed_book.status, BookStatus.GIVEN_OUT)
        # и проверка, что статус книги изменился.
        find_book = book_repository.get_book_by_id(2)
        self.assertEqual(find_book.status, BookStatus.GIVEN_OUT)

        # Возвращение статуса книги.
        changed_book = book_repository.changing_status_book(2, BookStatus.AVAILABLE)
        self.assertEqual(changed_book.status, BookStatus.AVAILABLE)
        # и проверка, что статус книги вернулся к доступной..
        find_book = book_repository.get_book_by_id(2)
        self.assertEqual(find_book.status, BookStatus.AVAILABLE)

    def test_changing_book_status_negative(self):
        """ Проверяет изменение статуса книги негативный """
        book_repository = BookRepository()
        # Проверка исключения при попытке изменить статус в пустом хранилище
        with self.assertRaises(BookRepositoryError) as cm:
            _ = book_repository.changing_status_book(2, BookStatus.GIVEN_OUT)
        self.assertEqual(cm.exception.message,
                         "It is impossible to changing status books because the repository is empty")

        # Далее хранилище заполняется книгами.
        book_repository = self._get_repository_filled_with_books()
        # Проверка исключения при попытке изменить статус несуществующей книге.
        with self.assertRaises(BookRepositoryError) as cm:
            _ = book_repository.changing_status_book(10, BookStatus.GIVEN_OUT)
        self.assertEqual(cm.exception.message, "The book with the ID 10 is missing")

        # Проверка исключения при попытке изменить статус на неправильный.
        with self.assertRaises(BookRepositoryError) as cm:
            _ = book_repository.changing_status_book(2, 3)
        self.assertEqual(cm.exception.message, "The status must be a logical value")

    def test_import_and_export_repository(self):
        """ Проверяет импорт и экспорт данных репозитория """
        book_repository = self._get_repository_filled_with_books()

        # Все книги в список простых объектов.
        repository_obj = book_repository._import()
        # Создание нового хранилища.
        book_repository_1 = BookRepository()
        self.assertEqual(book_repository_1.number_of_books, 0)
        # Заполнение нового хранилища из списка простых объектов.
        book_repository_1._export(repository_obj)
        self.assertEqual(book_repository_1.number_of_books, 6)

        # Все книги в JSON строку
        repository_json = book_repository._to_json()

        book_repository_2 = BookRepository()
        self.assertEqual(book_repository_2.number_of_books, 0)
        # Заполнение нового хранилища из json_строки
        book_repository_2._from_json(repository_json)
        self.assertEqual(book_repository_2.number_of_books, 6)

    def test_save_and_load_repository(self):
        """ Проверяет удаление книг из репозитория негативный"""
        filename = 'book_repository.json'
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = Path(tmpdir, filename)
            # Проверяется, что файла с сохранёнными книгами ещё нет.
            self.assertFalse(filename.exists())

            # Создаётся пустое хранилище
            book_repository = BookRepository()
            save_num = book_repository.save(filename)
            # Проверка, что при пустом хранилище количество сохранённых данных равно нулю,
            self.assertEqual(save_num, 0)
            # а так же, что при этом не создаётся файл с сохранениями.
            self.assertFalse(filename.exists())

            # Далее создаётся заполненное хранилище книг.
            book_repository = self._get_repository_filled_with_books()
            number_of_books = len(self.books)
            # Проверка, что хранилище заполнено книгами.
            self.assertEqual(book_repository.number_of_books, number_of_books)
            save_num = book_repository.save(filename)
            # После сохранения должен появиться файл с сохранёнными книгами.
            self.assertTrue(filename.exists())
            # Так же проверяется возвращаемое значение количества сохранённых книг.
            self.assertEqual(save_num, 6)

            # Теперь создаётся другое хранилище книг,
            other_book_repository = BookRepository()
            # и туда загружаются книги.
            load_num = other_book_repository.load(filename)
            # Проверка возвращаемого значение количества загруженных книг.
            self.assertEqual(load_num, 6)
            # Так же проверка, что в хранилище действительно столько книг, сколько и должно быть.
            self.assertEqual(other_book_repository.number_of_books, number_of_books)
            self.assertSequenceEqual(
                tuple(book.title for book in self.books),
                tuple(book.title for book in other_book_repository.all_books))
            last_id = number_of_books
            # Проверяется, что последний идентификатор хранилища верный.
            self.assertEqual(other_book_repository._last_id, number_of_books)
            # Пробуется найти книги из другого хранилища
            books = other_book_repository.find_book_by_author('Сергей Лукьяненко')
            self.assertEqual(books[0].title, "Ночной дозор")
            self.assertEqual(books[1].title, "Дневной дозор")

            # Поиск книги по идентификатору, которого нет.
            non_existent_book = other_book_repository.get_book_by_id(last_id + 1)
            # Проверка, что ничего не найдено.
            self.assertIsNone(non_existent_book)

            # Теперь добавляется новая книга,
            new_book = Book("Новая книга", "Неизвестный автор", 2000)
            other_book_repository.add_book(new_book)
            # а потом ищется по новому идентификатору.
            find_new_book = other_book_repository.get_book_by_id(last_id + 1)
            # Проверка, что книга найдена,
            self.assertIsNotNone(find_new_book)
            # и имеет новый идентификатор.
            self.assertEqual(find_new_book.id, last_id + 1)