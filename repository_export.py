import json
from copy import copy
from typing import Any

from abstract_class import AbstractBookRepositoryExport
from book import Book
from exceptions import ValidationError, BookRepositoryExportException
from validation import validation_id, validation_status


class BookRepositoryExport(AbstractBookRepositoryExport):
    """ Конкретный класс экспорта и импорта книг в хранилище. """
    def __init__(self, book_repository: 'AbstractBookRepository'):
        super().__init__(book_repository)
        self._last_id = 0

    def import_data(self) -> tuple[list[dict[str: Any]], dict[int, bool]]:
        """
        Импортирует данные.
        :return: Возвращает кортеж, словаря книг, и словаря статусов этих книг.
        """
        # books: dict[int, dict[str: Any]] = {}
        books: list[dict[str: Any]] = []
        books_status: dict[int, bool] = {}
        for book in self._book_repository.all_books:
            # books[book.id] = copy(book.to_dict())
            books.append(copy(book.to_dict()))
            books_status[book.id] = self._book_repository.get_status_book(book.id).value
        return books, books_status

    def export_data(self, source_data: tuple[list[dict[str: Any]], dict[int, bool]],
                    destination_data: tuple[list[dict[str: Any]], dict[int, bool]]) -> int:
        """
        Заполняет хранилище из списка простых объектов.
        :param source_data: Данные для экспорта в виде кортежа: [book_list, status_dict].
        :param destination_data: Данные, куда данные экспортируются.
        :return: Последний номер идентификатора.
        :raises BookRepositoryExportException: Ошибка при экспорте данных
        """
        source_book_dict, source_status_dict = source_data
        destination_book_dict, destination_status_dict = destination_data
        row_num = []
        try:
            # logger.debug(status_dict)
            row_num = [1]
            # После экспорта книг, сразу же устанавливается самый последний идентификатор.
            self._last_id = self._export_book(row_num, source_book_dict, destination_book_dict)
            row_num = [1]
            self._export_statuses(row_num, source_status_dict, destination_status_dict)
        except ValidationError as err:
            self._book_repository._books_status = {}
            self._book_repository._books = {}
            raise BookRepositoryExportException(f"Error when exporting books number {row_num[0]}. "
                                                f"{err.message}: {err.var_name} = {err.value}")
        except KeyError as err:
            self._book_repository._books_status = {}
            self._book_repository._books = {}
            raise BookRepositoryExportException(f"Error when exporting books number {row_num[0]}. "
                                                f"The {err.args[0][1:]} data is missing")

        return self._last_id

    def _export_book(self, row_num, source_book_list: list[dict[str: Any]],
                     destination_book_list: dict[int, dict[str: Any]]) -> int:
        """
        Экспортирует книги
        :param row_num: Счётчик экспортируемых строк.
        :param source_book_list: Словарь с данными для экспорта.
        :param destination_book_list: Словарь с данными, куда производиться экспорт.
        :return Самый последний (он же самый большой) идентификатор.
        :raises ValidationError: Ошибка валидации данных.
        :raises KeyError: Данные экспорта отсутствуют.
        """
        last_id = 0

        for _book in source_book_list:
            book = Book(_book['_title'], _book['_author'], _book['_year'])
            book.set_id(_book['_id'])
            destination_book_list[validation_id(book.id)] = book
            # Сразу же ищется самый последний (он же самый большой) идентификатор.
            if book.id > last_id:
                last_id = book.id
            row_num[0] = row_num[0] + 1

        return last_id

    def _export_statuses(self, row_num, source_status_dict: dict[int, bool], destination_status_dict: dict[int, bool]):
        """
        Экспортирует статусы книг.
        :param row_num: Счётчик экспортируемых строк.
        :param source_status_dict: Словарь с данными для экспорта.
        :param destination_status_dict: Словарь с данными, куда производиться экспорт.
        :raises ValidationError: Ошибка валидации данных.
        """
        for _id, status in source_status_dict.items():
            _id = validation_id(_id)
            # При экспорте проверятся, чтобы такой идентифкатор не превышал самый большой идентификатор в хранилище.
            if _id > self._last_id:
                ValidationError(f'The identifier does not exist in the book store.', 'status', _id)
            destination_status_dict[validation_id(_id)] = validation_status(status)
            row_num[0] = row_num[0] + 1

    def _to_json(self) -> str:
        """ Преобразует список всех книг в json строку. """
        return json.dumps(self.import_data())

    def _from_json(self, _json: str):
        """
        Заполняет хранилище по json строке.
        :param _json:
        :raises BookRepositoryExportException: Ошибка при экспорте данных.
        """
        self.export_data(json.loads(_json))