# from app import SimpleLibrary
from helper import clear_display


class LibraryManager:
    """ Класс управления библиотекой """
    def __init__(self, library: 'SimpleLibrary'):
        self._library = library

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
        clear_display()
        self._print_result("Book is added")

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

    @classmethod
    def _input_id(cls, msg):
        """ Запрос ввода идентификатора книги """
        while True:
            try:
                num = input(msg)
                if num in ('c', 'cancel'):
                    raise InputStop()
                return int(num)
            except ValueError:
                clear_display()
                print("Error: The identifier must be a number. Try again, or press '(c)cancel' to cancel input.")

    def _input_status(self):
        """
        Запрос ввода статуса
        :return:
        :raises InputException: Неверный статус
        """
        while True:
            try:
                status_str = input("Enter status book (a)vailable or (g)iven_out: ").lower()
                if status_str in ('c', 'cancel'):
                    raise InputStop()
                return self._str_status_convert(status_str)
            except InputException:
                clear_display()
                print("Error: The status must be only a '(a)vailable' or '(g)iven_out'). "
                      "Try again, or press '(c)cancel' to cancel input.")

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


class InputException(Exception):
    """ Ошибка ввода данных с консоли """
    def __init__(self, msg):
        self._msg = msg

    @property
    def message(self):
        return self._msg


class InputStop(Exception):
    """ Перкращение ввода данных """
    pass