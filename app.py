from helper import clear_display
from manager import Manager
import sys


class SimpleLibrary:
    library_tile = "*** SIMPLE LIBRARY ***"

    ADD_BOOK = '1'
    REMOVE_BOOK = '2'
    SEARCH_BOOK = '3'
    DISPLAY_ALL_BOOKS = '4'
    CHANGE_BOOK_STATUS = '5'
    QUIT = "q"

    def __init__(self):
        self._manager = Manager(self)

    @classmethod
    def run(cls):
        cls().start()

    @classmethod
    def show_menu(cls):
        """ Отображает меню действий """
        print(f"{cls.ADD_BOOK}. Adding a book")
        print(f"{cls.REMOVE_BOOK}. Deleting a book")
        print(f"{cls.SEARCH_BOOK}. Book Search")
        print(f"{cls.DISPLAY_ALL_BOOKS}. Displaying all books")
        print(f"{cls.CHANGE_BOOK_STATUS}. Changing the status of a book")

    def start(self):
        """ Запуск консоли """
        while True:
            clear_display()
            print(f"{self.library_tile}\n")
            self.show_menu()
            action_num = input("Select a menu item: ")
            if action_num.lower() == self.QUIT:
                break
            self._manager.actions_handle(action_num)


if __name__ == "__main__":
    SimpleLibrary().run()