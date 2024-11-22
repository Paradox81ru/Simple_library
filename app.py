from pathlib import Path

from book_manager import BookManager
from book_repository import BookRepository
from helper import clear_display
from library_manager import LibraryManager
import sys


class SimpleLibrary:
    library_tile = "*** SIMPLE LIBRARY ***"

    ADD_BOOK = '1'
    REMOVE_BOOK = '2'
    SEARCH_BOOK = '3'
    DISPLAY_ALL_BOOKS = '4'
    CHANGE_BOOK_STATUS = '5'

    REPOSITORY_FILENAME = "book_repository.json"

    def __init__(self):
        self._book_manager = BookManager(BookRepository())
        self._library_manager = LibraryManager(self, self._book_manager)

    def run(self):
        """ Запуск работы приложения """
        self._load_data()
        self._start_console()

    def _load_data(self):
        """ Загружает из файла данные в хранилище """
        repository_file = Path(self.REPOSITORY_FILENAME)
        # Данные будут загружены, если файл для загрузки есть.
        if repository_file.exists():
            self._book_manager.load_data(self.REPOSITORY_FILENAME)

    def _save_data(self):
        """ Сохраняет данные из хранилища в файл """
        self._book_manager.save_data(self.REPOSITORY_FILENAME)

    def _show_menu(self):
        """ Отображает меню действий """
        print(f"{self.ADD_BOOK}. Adding a book.")
        print(f"{self.REMOVE_BOOK}. Deleting a book.")
        print(f"{self.SEARCH_BOOK}. Book Search.")
        print(f"{self.DISPLAY_ALL_BOOKS}. Displaying all books.")
        print(f"{self.CHANGE_BOOK_STATUS}. Changing the status of a book.")
        print(f"Press (q)uit to exit")
        print("")

    def _start_console(self):
        """ Запуск консоли """
        # Запрос выбора действия, пока не будет произведён выход из приложения.
        while True:
            clear_display()
            print(f"{self.library_tile}\n")
            self._show_menu()
            action_num = input("Select a menu item: ").strip().lower()
            if action_num in ('q', 'quit'):
                self._quit_handler()
                break
            self._library_manager.actions_handle(action_num)

    def _quit_handler(self):
        """ Обработка выхода из приложения """
        self._save_data()
        clear_display()
        input("Thank you for using our library. Good luck.")


if __name__ == "__main__":
    SimpleLibrary().run()
