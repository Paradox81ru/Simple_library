# from app import SimpleLibrary
from datetime import datetime

from book_manager import BookManager
from exceptions import InputException
from helper import clear_display
from typing import final


class LibraryManager:
    """ Класс управления библиотекой """
    TRY_AGAIN: final = "Try again, or press '(c)cancel' to cancel input."

    def __init__(self, library: 'SimpleLibrary', book_manager: BookManager):
        self._library = library
        self._book_manager = book_manager

    def actions_handle(self, action_num: str):
        """ Обрабатывает выбранное действие """
        match action_num.strip():
            case '':
                return
            case self._library.ADD_BOOK:
                self._add_book()
            case self._library.REMOVE_BOOK:
                self._remove_book()
            case self._library.SEARCH_BOOK:
                self._search_book()
            case self._library.DISPLAY_ALL_BOOKS:
                self._display_all_books()
            case self._library.CHANGE_BOOK_STATUS:
                self._changed_book_status()
            case _:
                self._invalid_menu()

    def _add_book(self):
        """ Добавляет книгу в библиотеку """
        # Запрашивает данные для добавления книги.
        clear_display()
        title = input("Enter the title of the book: ")
        clear_display()
        author = input("Enter the author of the book: ")
        clear_display()
        try:
            year = self._input_year()
        except InputStop:
            return

        try:
            # Добавляет книгу, и получает её идентификатор.
            book_id = self._book_manager.add_book(title, author, year)
            self._print_result(f"Book ID {book_id} is added")
        except ValueError as err:
            self._print_result(err.args[0])

    def _remove_book(self):
        """ Удаляет книгу из библиотеки """
        clear_display()
        try:
            _id = self._input_id("Enter the ID of the book you want to delete: ")
        except InputStop:
            return
        self._print_result(f"Book {_id} is removed")

    def _search_book(self):
        """ Поиск книги """
        clear_display()
        self._print_result("Search is book")

    def _display_all_books(self):
        """ Отображает все книги из библиотеки """
        clear_display()
        self._print_result("Display all books")

    def _changed_book_status(self):
        """ Изменяет статус книги """
        clear_display()
        try:
            _id = self._input_id("Enter the ID of the book whose status you want to change: ")
            clear_display()
            status = self._input_status()
        except InputStop:
            return
        self._print_result(f"The status of the book with ID {_id} changed to {status} ")

    def _invalid_menu(self):
        """ Сообщение при неверно выбранном меню """
        clear_display()
        self._print_result("There is no such menu")

    def _input_id(self, msg):
        """ Запрос ввода идентификатора книги """
        while True:
            try:
                num = input(msg)
                if num in ('c', 'cancel'):
                    raise InputStop()
                return int(num)
            except ValueError:
                clear_display()
                print(f"Error: The identifier must be a number. {self.TRY_AGAIN}")

    def _input_status(self):
        """
        Запрос ввода статуса
        :return: статус
        :raises InputStop: Отменить ввод
        """
        while True:
            try:
                status_str = input("Enter status book (a)vailable or (g)iven_out: ").lower()
                if status_str in ('c', 'cancel'):
                    raise InputStop()
                return self._str_status_convert(status_str)
            except InputException:
                clear_display()
                print(f"Error: The status must be only a '(a)vailable' or '(g)iven_out'). {self.TRY_AGAIN}")

    def _input_year(self):
        """
        Запрос ввода года издания
        """
        while True:
            try:
                year = input("Enter the year of publication of the book: ")
                if year in ('c', 'cancel'):
                    raise InputStop()
                year = int(year)
                now_year = datetime.now().year
                # Проверка, что год выпуска не больше текущего года.
                if year > now_year:
                    clear_display()
                    print(f"Error: The year cannot be longer than the current year. {self.TRY_AGAIN}")
                    continue
                return year
            except ValueError:
                clear_display()
                print(f"Error: The year must be a number. {self.TRY_AGAIN}")

    @classmethod
    def _str_status_convert(cls, status_str) -> bool | None:
        """
        Конвертирует статус из строки в логический тип.
        :param status_str: статус в виде строки
        :return:
        :raises InputException: Неверный статус
        """
        if status_str in ('a', 'available'):
            return True
        elif status_str in ('g', 'given_out'):
            return False
        raise InputException(f"Error: Status '{status_str}' is invalid")

    @classmethod
    def _print_result(cls, msg):
        print(msg)
        input("press any key...")


class InputStop(Exception):
    """ Окончание ввода данных """
    pass
