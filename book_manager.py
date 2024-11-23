from abstract_book_repository import AbstractBookRepository
from book import Book, BookStatus
from enums import SearchCriteria
from exceptions import BookManagerError, BookRepositoryError, ValidationError


class BookManager:
    """ Класс управление хранилищем книг """
    def __init__(self, book_repository: AbstractBookRepository):
        self._book_repository = book_repository

    def load_data(self, filename):
        """
        Загружает данные в репозиторий
        :param filename: наименование файла для загрузки
        :return: Количество загруженных книг
        """
        return self._book_repository.load(filename)

    def save_data(self, filename) -> int:
        """
        Сохраняет данные из репозитория в файл.
        Файл создаётся, только если хранилище не пустое.
        :param filename: Наименование файла для сохранения.
        :return: Количество сохранённых книг
        """
        return self._book_repository.save(filename)

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
        except ValidationError as err:
            raise BookManagerError(err.message)
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

    def get_book_info_by_id(self, _id) -> str | None:
        """
        Возвращает информацию о книге по её идентификатору, или None, если книга не найдена.
        :param _id:
        :return:
        :raises BookManagerError: Удалить книги невозможно, так как хранилище пусто;
                                     Книга с указанным идентификатором отсутствует.
        """
        try:
            book = self._book_repository.get_book_by_id(_id)
            if book is None:
                return None
            else:
                return str(self._book_repository.get_book_by_id(_id))
        except BookRepositoryError as err:
            raise BookManagerError(err.message)

    def find_book(self, search_criteria: SearchCriteria, search_val: str | int) -> tuple[int, str]:
        """
        Поиск книги
        :param search_criteria: Критерий поиска
        :param search_val: значение поиска
        :return: Кортеж в формате (Кол-во найденных книг, Строковый список найденных книг)
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
        count_books = len(books)
        return (count_books, self._book_list_to_str(books)) if len(books) > 0 \
            else (0, "Nothing was found for your query")

    def get_all_books(self) -> tuple[int, str]:
        """
        Возвращает общее кол-во книг и список всех книг из хранилища
        :return: Кортеж в формате (Общее кол-во книг, строковый список всех книг)
        """
        books = self._book_repository.all_books
        count_books = len(books)
        return (count_books, self._book_list_to_str(books)) if len(books) > 0 \
            else (0, "There are no books to display in the storage")

    def changing_status_book(self, _id: int, status: BookStatus) -> tuple[int, str]:
        """
        Изменяет статус книги.
        :param _id: Идентификатор книги, статус которой надо изменить.
        :param status: Новый статус книги.
        :return: Идентификатор книги и её новый статус.
        :raises BookManagerError: Изменить статус книги невозможно, так как хранилище пустое;
                                  Книга с указанным идентификатором отсутствует;
                                  Статус должен быть логическим значением.
        """
        try:
            book = self._book_repository.changing_status_book(_id, status)
            return book.id, book.status.to_str()
        except BookRepositoryError as err:
            raise BookManagerError(err.message)

    # noinspection PyMethodMayBeStatic
    def _book_list_to_str(self, book_list: tuple[Book, ...]):
        """ Преобразует список книг в строку """
        return "\n".join(str(book) for book in book_list)
