from typing import final

from book import BookStatus
from book_manager import BookManager
from enums import SearchCriteria
from exceptions import InputException, BookManagerError, ValidationError
from helper import clear_display, print_awaiting_message
from validation import validation_id, validation_year, validation_title, validation_author


class LibraryConsole:
    """ Класс управления библиотекой """
    PRESS_CANCEL = ", or press '(c)cancel' to cancel input"
    TRY_AGAIN: final = f"Try again."

    library_tile = "*** SIMPLE LIBRARY ***"

    ADD_BOOK = '1'
    REMOVE_BOOK = '2'
    SEARCH_BOOK = '3'
    DISPLAY_ALL_BOOKS = '4'
    CHANGE_BOOK_STATUS = '5'

    def __init__(self, library: 'SimpleLibrary', book_manager: BookManager):
        self._library = library
        self._book_manager = book_manager

    def _show_menu(self):
        """ Отображает меню действий """
        print(f"{self.ADD_BOOK}. Adding a book.")
        print(f"{self.REMOVE_BOOK}. Deleting a book.")
        print(f"{self.SEARCH_BOOK}. Book search.")
        print(f"{self.DISPLAY_ALL_BOOKS}. Displaying all books.")
        print(f"{self.CHANGE_BOOK_STATUS}. Changing the status of a book.")
        print(f"Press (q)uit to exit")
        print("")

    def start_console(self, quit_handler: callable):
        """
        Запуск консоли
        :param quit_handler: Обработчик выхода из библиотеки
        """
        # Запрос выбора действия, пока не будет произведён выход из приложения.
        while True:
            clear_display()
            print(f"{self.library_tile}\n")
            self._show_menu()
            action_num = input("Select a menu item: ").strip(' .').lower()
            if action_num in ('q', 'quit'):
                quit_handler()
                break
            self._actions_handle(action_num)

    def _actions_handle(self, action_num: str):
        """ Обрабатывает выбранное действие """
        match action_num.strip():
            case '':
                return
            case self.ADD_BOOK:
                self._add_book()
            case self.REMOVE_BOOK:
                self._remove_book()
            case self.SEARCH_BOOK:
                self._search_book()
            case self.DISPLAY_ALL_BOOKS:
                self._display_all_books()
            case self.CHANGE_BOOK_STATUS:
                self._changed_book_status()
            case _:
                self._invalid_menu()

    def _add_book(self):
        """ Добавляет книгу в библиотеку """
        # Запрашивает данные для добавления книги.
        try:
            clear_display()
            title = self._input_validation(self._input_title)
            # title = self._input_title()
            clear_display()
            author = self._input_validation(self._input_author)
            # author = self._input_author()
            clear_display()
            year = self._input_validation(self._input_year)
            # year = self._input_year()
        except InputStop:
            return

        try:
            # Добавляет книгу, и получает её идентификатор.
            book_id = self._book_manager.add_book(title, author, year)
            print_awaiting_message(f"Book ID {book_id} is added")
        except BookManagerError as err:
            print_awaiting_message(err.message)

    def _remove_book(self):
        """ Удаляет книгу из библиотеки """
        clear_display()
        try:
            _id = self._input_validation(
                self._input_id(f"Enter the ID of the book you want to delete{self.PRESS_CANCEL}: "))
        except InputStop:
            return

        try:
            # Перед удалением надо найти информацию об удаляемой книге.
            book_info = self._book_manager.get_book_info_by_id(_id)
            if book_info is None:
                # И если книги с таким идентификатором нет, то нечего дальше и делать.
                print_awaiting_message(f"The book with ID {_id} was not found.")
                return

            try:
                # Иначе запрашивается подтверждение на удаление книги.
                confirm = self._input_confirm("Are you sure you want to delete the next book?\n" + book_info)
            except InputStop:
                # Если отменил подтверждение, то сообщение, что книга удалена не будет.
                print_awaiting_message(f"The book with ID {_id} will not be deleted.")
                return
            if confirm in  ('y', 'yes'):
                # Если подтвердил, значит книга удаляется.
                book_id = self._book_manager.remove_book(_id)
                print_awaiting_message(f"The book with ID {book_id} has been deleted.")
            else:
                # Если не подтвердил, соответствующее сообщение.
                print_awaiting_message(f"The book with ID {_id} will not be deleted.")
        except BookManagerError as err:
            print_awaiting_message(err.message)

    def _search_book(self):
        """ Поиск книги """
        try:
            search_num = self._select_search_criterion()
        except InputStop:
            return

        search_str = ""
        # Вообще код выше гарантирует правильное значение выбора критерия.
        match search_num:
            case SearchCriteria.SEARCH_TITLE:
                clear_display()
                search_str = input("Enter the title or part of the title of the book: ").strip()
            case SearchCriteria.SEARCH_AUTHOR:
                clear_display()
                search_str = input("Enter the author of the book: ").strip()
            case SearchCriteria.SEARCH_YEAR:
                try:
                    clear_display()
                    search_str = self._input_validation(self._input_year)
                except InputStop:
                    return
        try:
            search_num = SearchCriteria.get_criteria(search_num)
            books_num, result = self._book_manager.find_book(search_num, search_str)
            clear_display()
            print(f"{books_num} books found:")
            print_awaiting_message(result)
        except BookManagerError as err:
            print_awaiting_message(err.message)
        except ValueError as err:
            # 'get_criteria' может вызвать это исключение при неверном выборе критерия поиска.
            # Вообще код выше гарантирует правильное значение выбора критерия,
            # но все таки для гарантии ещё одна проверка.
            print_awaiting_message(err.args[0])

    def _select_search_criterion(self) -> str:
        """
        Выбор критерия поиска
        :return: Пункт выбранного критерия поиска.
        :raises InputStop: Отменить ввод.
        """
        # Запрос номера критерия поиска пока не будет правильный ввод или произведена отмена ввода.
        while True:
            clear_display()
            print(f"By what criteria do you want to perform a search{self.PRESS_CANCEL}?")
            print(f"{SearchCriteria.SEARCH_TITLE}. Title.")
            print(f"{SearchCriteria.SEARCH_AUTHOR}. Author.")
            print(f"{SearchCriteria.SEARCH_YEAR}. Year.")

            search_num = input("Select a search num: ").strip().lower()
            self._check_cancel_input(search_num)
            if search_num == "":
                continue
            # Если указан неверный пункт поиска, то заново запрашивается ввода пункта поиска.
            if search_num not in (SearchCriteria.SEARCH_TITLE, SearchCriteria.SEARCH_AUTHOR, SearchCriteria.SEARCH_YEAR):
                print_awaiting_message(f"There is no such search criterion. {self.TRY_AGAIN}")
                continue
            # Если ввод верный, то возвращается значение ввода.
            return search_num

    def _display_all_books(self):
        """ Отображает все книги из библиотеки """
        clear_display()
        count_num, all_books = self._book_manager.get_all_books()
        print(f"There are {count_num} books in the library in total:")
        print_awaiting_message(all_books)

    def _changed_book_status(self):
        """ Изменяет статус книги """
        clear_display()
        try:
            _id = self._input_validation(
                self._input_id(f"Enter the ID of the book whose status you want to change{self.PRESS_CANCEL}: "))
            clear_display()
            input_status = self._input_status()
        except InputStop:
            return

        try:
            book_id, status = self._book_manager.changing_status_book(_id, input_status)
            print_awaiting_message(f"The book with ID {book_id} now has the status '{status}'")
        except BookManagerError as err:
            print_awaiting_message(err.message)

    # noinspection PyMethodMayBeStatic
    def _invalid_menu(self):
        """ Сообщение при неверно выбранном меню """
        clear_display()
        print_awaiting_message("There is no such menu")

    def _input_id(self, msg):
        """
        Запрос ввода идентификатора книги
        :param msg: Сообщение при вводе идентификатора
        :return: Введённый идентификатор.
        :raises InputStop: Отменить ввод.
        """
        def wrap():
            num = input(msg).strip().lower()
            self._check_cancel_input(num)
            return validation_id(num)
        return wrap

    # def _input_id(self, msg):
    #     """
    #     Запрос ввода идентификатора книги
    #     :param msg: Сообщение при вводе идентификатора
    #     :return: Введённый идентификатор.
    #     :raises InputStop: Отменить ввод.
    #     """
    #     while True:
    #         try:
    #             num = input(msg).strip().lower()
    #             self._check_cancel_input(num)
    #             return validation_id(num)
    #         except ValidationError as err:
    #             clear_display()
    #             print(f"Error: {err.message} {self.TRY_AGAIN}")

    def _input_title(self):
        """
        Запрос ввода наименования книги
        :return: Наименование книги.
        :raises InputStop: Отменить ввод
        """
        title = input(f"Enter the title of the book{self.PRESS_CANCEL}: ").strip()
        self._check_cancel_input(title)
        return validation_title(title)

    def _input_author(self):
        """
        Запрос ввода автора книги
        :return: Автор книги.
        :raises InputStop: Отменить ввод
        """
        author = input(f"Enter the author of the book:{self.PRESS_CANCEL}: ").strip()
        self._check_cancel_input(author)
        return validation_author(author)

    def _input_year(self):
        """
        Запрос ввода года издания
        :return: Год издания.
        :raises InputStop: Отменить ввод
        """
        year = input(f"Enter the year of publication of the book{self.PRESS_CANCEL}: ").strip().lower()
        self._check_cancel_input(year)
        return validation_year(year)

    def _input_validation(self, func: callable):
        """
        Запрос ввода корректных данных
        :param func:
        :return: Корректные запрашиваемые данные.
        :raises InputStop: Отменить ввод
        """
        while True:
            try:
                return func()
            except ValidationError as err:
                clear_display()
                # Предупреждение о неверно введённых данных.
                print(f"Error: {err.message} {self.TRY_AGAIN}")

    def _input_status(self):
        """
        Запрос ввода статуса
        :return: Статус.
        :raises InputStop: Отменить ввод
        """
        while True:
            try:
                status_str = input(f"Enter status book (a)vailable or (g)iven_out{self.PRESS_CANCEL}: ").strip().lower()
                self._check_cancel_input(status_str)
                return self._str_status_convert(status_str)
            except InputException as err:
                clear_display()
                # Предупреждение о неверно введённом статусе книги.
                print(f"Error: {err.message} {self.TRY_AGAIN}")

    def _input_confirm(self, msg):
        """
        Запрос подтверждения Да или Нет
        :param msg: Сообщение при подтверждении
        :return: Подтверждение.
        :raises InputStop: Отменить ввод
        """
        while True:
            clear_display()
            print(msg)
            confirm = input(f"Select Yes/No{self.PRESS_CANCEL}: ").strip().lower()
            self._check_cancel_input(confirm)
            if confirm in ('y', 'yes', 'n', 'no'):
                return confirm
            else:
                print_awaiting_message(f"You have to return 'Yes' or 'No'. {self.TRY_AGAIN}")

    @classmethod
    def _str_status_convert(cls, status_str) -> BookStatus:
        """
        Конвертирует статус из строки в логический тип.
        :param status_str: Статус в виде строки.
        :return: Статус книги в логическом виде.
        :raises InputException: Неверный статус
        """
        if status_str in ('a', 'available'):
            return BookStatus.AVAILABLE
        elif status_str in ('g', 'given_out'):
            return BookStatus.GIVEN_OUT
        raise InputException(f"The status must be only a '(a)vailable' or '(g)iven_out'.")

    # noinspection PyMethodMayBeStatic
    def _check_cancel_input(self, _input):
        """
        Проверят введенное значение на отмену ввода
        :param _input: значение ввода
        :raises InputStop: исключение для прерывания ввода.
        """
        if _input in ('c', 'cancel'):
            raise InputStop()

class InputStop(Exception):
    """ Отмена ввода данных """
    pass
