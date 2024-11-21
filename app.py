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
        print(f"Press (q)uit to exit")
        print("")

    def start(self):
        """ Запуск консоли """
        book_repository = BookRepository()
        book_manager = BookManager(book_repository)
        library_manager = LibraryManager(self, book_manager)
        while True:
            clear_display()
            print(f"{self.library_tile}\n")
            self.show_menu()
            action_num = input("Select a menu item: ")
            if action_num.lower() in ('q', 'quit'):
                break
            library_manager.actions_handle(action_num)


if __name__ == "__main__":
    SimpleLibrary().run()