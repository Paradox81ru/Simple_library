import unittest
import json

from book import Book
from book_repository import BookRepository
from exceptions import BookRepositoryError


class BookRepositoryTest(unittest.TestCase):
    """ Тестирование хранилища книг """

    def setUp(self):
        self.books = (Book("Толковый словарь", "В.И. Даль", 1982),
                      Book("Ночной дозор", "Сергей Лукьяненко", 1998),
                      Book("Дневной дозор", "Сергей Лукьяненко", 2000),
                      Book("Звездные войны. Новая надежда", "Алан Дин Фостер. ", 1976),
                      Book("Звездные войны. Империя наносит ответный удар", "Дональд Ф", 1980),
                      Book("Звездные войны. Возвращение джедая", "Джеймс Кан", 1983))

    def test_add_book(self):
        """ Проверяет добавление книг в репозиторий """
        book_repository = BookRepository('filename.json')
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
        book_repository = BookRepository('filename.json')
        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Удаляется книга,
        book_repository.remove_book(6)
        number_of_books -= 1
        # и проверка, что в хранилище на одну книгу меньше
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Ещё одна книга удаляется,
        book_repository.remove_book(1)
        number_of_books -= 1
        # и снова проверка, что в хранилище на одну книгу меньше
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Из хранилища удаляются все книги
        for _id in range(2, 6):
            book_repository.remove_book(_id)
        self.assertEqual(book_repository.number_of_books, 0)

        # Проверка ошибки, при попытке удалить книгу из пустого репозитория
        with self.assertRaises(BookRepositoryError) as cm:
            book_repository.remove_book(9)
        self.assertEqual(cm.exception.message, "It is impossible to delete books because the repository is empty")

    def test_remove_book_negative(self):
        """ Проверяет удаление книг из репозитория негативный"""
        book_repository = BookRepository('filename.json')
        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
        number_of_books = len(self.books)
        # Проверка, что репозиторий заполнен книгами.
        self.assertEqual(book_repository.number_of_books, number_of_books)

        # Попытка удалить книгу, идентификатора которого нет.
        with self.assertRaises(BookRepositoryError) as cm:
            book_repository.remove_book(10)
        self.assertEqual(cm.exception.message, f"The book with the ID 10 is missing")

    def test_find_books(self):
        """ Проверяет поиск книг """
        book_repository = BookRepository('filename.json')
        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
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
        book_repository = BookRepository('filename.json')

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

    def test_get_all_books(self):
        """ Проверяет возвращение всех книг из репозитория """
        book_repository = BookRepository('filename.json')
        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
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

    def test_save_and_load_repository(self):
        """ Проверяет удаление книг из репозитория негативный"""
        # book = self.books[0]
        # book.id = 2
        # print(book.to_json())

        book_repository = BookRepository('filename.json')
        # Репозиторий заполняется книгами
        for i, book in enumerate(self.books, start=3):
            book_repository.add_book(book)
        repository_json = book_repository._to_json()

        new_book_repository = BookRepository('filename.json')
        new_book_repository._from_json(repository_json)
        self.assertEqual(new_book_repository.number_of_books, 6)