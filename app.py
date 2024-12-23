from pathlib import Path

from abstract_class import AbstractBookRepository, AbstractBookRepositoryExport
from book_manager import BookManager
from book_repository import BookRepository
from exceptions import BookRepositoryError, BookRepositoryExportException
from helper import clear_display, print_awaiting_message
from library_console import LibraryConsole
from repository_export import BookRepositoryExport


# LOGGER_FILENAME = "library.log"
# logger = get_logger('app', LOGGER_FILENAME, is_debug_mode=True)


class SimpleLibrary:
    REPOSITORY_FILENAME = "book_repository.json"

    def __init__(self):
        book_repository: AbstractBookRepository = BookRepository()
        repository_export: AbstractBookRepositoryExport = BookRepositoryExport(book_repository)
        book_repository.set_repository_export(repository_export)
        self._book_manager = BookManager(book_repository)
        self._library_console = LibraryConsole(self._book_manager)

    def run(self):
        """ Запуск работы приложения """
        self._load_data()
        self._library_console.start_console(self._quit_handler)

    def _load_data(self):
        """ Загружает из файла данные в хранилище """
        repository_file = Path(self.REPOSITORY_FILENAME)
        # Данные будут загружены, если файл для загрузки есть.
        if repository_file.exists():
            try:
                load_num = self._book_manager.load_data(self.REPOSITORY_FILENAME)
                print_awaiting_message(f'{load_num} books have been uploaded')
            except (BookRepositoryError, BookRepositoryExportException) as err:
                print("Probably not all books have been downloaded..")
                print_awaiting_message(err.message)

    def _save_data(self):
        """ Сохраняет данные из хранилища в файл. """
        save_num = self._book_manager.save_data(self.REPOSITORY_FILENAME)
        if save_num > 0:
            # Показывать сообщение, только если были данные для сохранения.
            print(f"{save_num} books have been saved")

    def _quit_handler(self):
        """ Обработка выхода из приложения. """
        clear_display()
        self._save_data()
        input("Thank you for using our library. Good luck.")


if __name__ == "__main__":
    SimpleLibrary().run()
