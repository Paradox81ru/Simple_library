# from app import SimpleLibrary
from helper import clear_display


class Manager:
    """ Класс управления библиотекой """
    def __init__(self, library: 'SimpleLibrary'):
        self._library = library

    def actions_handle(self, action_num: str):
        """ Обрабатывает выбранное действие """
        match action_num:
            case self._library.ADD_BOOK:
                self._add_book()
            case self._library.REMOVE_BOOK:
                self._remove_book()
            case self._library.SEARCH_BOOK:
                print("Book is search")
            case self._library.DISPLAY_ALL_BOOKS:
                print("Displaying books")
            case self._library.CHANGE_BOOK_STATUS:
                print("Changed book status")
            case _:
                print("There is no such menu")

    def _add_book(self):
        """ Добавляет книгу в библиотеку """
        clear_display()
        self._print_result("Book is added")

    def _remove_book(self):
        """ Удаляет книгу из библиотеки """
        clear_display()
        try:
            _id = self._input_id("Enter the ID of the book you want to delete: ")
        except InputException as err:
            self._print_result(err.message)
            return
        self._print_result(f"Book {_id} is removed")

    def _search_book(self):
        """ ПОиск книши """
        print("Search is book")

    def _display_all_books(self):
        """ Отображает все книги из библиотеки """
        clear_display()
        self._print_result("Display all books")

    def _changed_book_status(self):
        """ Изменяет статус книги """
        clear_display()
        try:
            _id = self._input_id("Enter the ID of the book you want to delete: ")
            status = self._input_status()
        except InputException as err:
            self._print_result(err.message)
            return
        self._print_result("Display all books")
        print(f"The book {id} changed status {status} ")

    @classmethod
    def _input_id(cls, msg):
        """ Запрос ввода идентификатора книги """
        try:
            return int(input(msg))
        except ValueError:
            raise InputException("Error: The identifier must be a number")

    def _input_status(self):
        """
        Запрос ввода статуса
        :return:
        :raises InputException: Неверный статус
        """
        status_str = input("Enter status (a)vailable or (g)iven_out").lower()
        return self._str_status_convert(status_str)

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

    def _print_result(self, msg):
        print(msg)
        input("press any key...")


class InputException(Exception):
    """ Ошибка ввода данных с консоли """
    def __init__(self, msg):
        self._msg = msg

    @property
    def message(self):
        return self._msg