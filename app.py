from helper import clear_display


class SimpleLibrary:
    library_tile = "*** SIMPLE LIBRARY ***"

    ADD_BOOK = '1'
    REMOVE_BOOK = '2'
    SEARCH_BOOK = '3'
    DISPLAY_ALL_BOOKS = '4'
    CHANGE_BOOK_STATUS = '5'
    QUIT = "q"

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
            self.actions_handle(action_num)

    def actions_handle(self, action_num: str):
        """ Обрабатывает выбранное действие """
        match action_num:
            case self.ADD_BOOK:
                print("Book is added")
            case self.REMOVE_BOOK:
                print("Book is removed")
            case self.SEARCH_BOOK:
                print("Book is search")
            case self.DISPLAY_ALL_BOOKS:
                print("Displaying books")
            case self.CHANGE_BOOK_STATUS:
                print("Changed book status")
            case _:
                print("There is no such menu")


if __name__ == "__main__":
    SimpleLibrary().run()