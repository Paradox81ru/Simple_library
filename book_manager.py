from abstract_book_repository import AbstractBookRepository
from book import Book
from enums import SearchCriteria
from exceptions import BookManagerError, BookRepositoryError


class BookManager:
    """ Класс управление хранилищем книг """
    def __init__(self, book_repository: AbstractBookRepository):
        self._book_repository = book_repository

    def load_data(self, filename):
        """ Загружает данные в репозиторий """
        self._book_repository.load(filename)

    def save_data(self, filename):
        """ Сохраняет данные из репозитория """
        self._book_repository.save(filename)

    def add_book(self, title: str, author: str, year: int) -> int:
        """
        Добавляет книгу в библиотеку
        :param title: название книги
        :param author: автор
        :param year: год издания
        :return: идентификатор добавленной книги
        :raises BookManagerError: Неправильно указан год издания книги
        """
        try:
            new_book = Book(title, author, year)
        except ValueError as err:
            raise BookManagerError(err.args[0])
        self._book_repository.add_book(new_book)
        return new_book.id

    def remove_book(self, _id: int) -> int:
        """
        Удаляет книгу из репозитория
        :param _id: Идентификатор удаляемой книги.
        :return: Идентификатор удалённой книги.
        :raises BookManagerError: Удалить книги невозможно, так как хранилище пусто;
                                     Книга с указанным идентификатором отсутствует.
        """
        try:
            return self._book_repository.remove_book(_id).id
        except BookRepositoryError as err:
            raise BookManagerError(err.message)

    def find_book(self, search_criteria: SearchCriteria, search_val: str | int):
        """
        Поиск книги
        :param search_criteria: Критерий поиска
        :param search_val: значение поиска
        :return: Строковый список описаний найденных книг
        :raises BookManagerError: Ошибка при указании года выпуска книги;
                                     Указан неверный критерий поиска
        """
        match search_criteria:
            case SearchCriteria.SEARCH_TITLE:
                books = self._book_repository.find_book_by_title(search_val)
            case SearchCriteria.SEARCH_AUTHOR:
                books = self._book_repository.find_book_by_author(search_val)
            case SearchCriteria.SEARCH_YEAR:
                try:
                    books = self._book_repository.find_book_by_year(search_val)
                except BookRepositoryError as err:
                    raise BookManagerError(err.args[0])
            case _:
                raise BookManagerError("Invalid search criteria specified")
        return "\n".join(str(book) for book in books) if len(books) > 0 else "Nothing was found for your query"

    def get_all_books(self):
        """ Возвращает список всех книг из хранилища """
        pass

