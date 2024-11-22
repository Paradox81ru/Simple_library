from enum import StrEnum


class SearchCriteria(StrEnum):
    """ Перечисление критериев поиска """
    SEARCH_TITLE = '1'
    SEARCH_AUTHOR = '2'
    SEARCH_YEAR = '3'

    @classmethod
    def get_criteria(cls, val: str):
        """
        Получение нужного значения из перечислений критериев поиска
        :param val: Значение критерия
        :return: Критерий поиска.
        :raises ValueError: Неверное значение критерия поиска
        """
        match val:
            case cls.SEARCH_TITLE:
                return cls.SEARCH_TITLE
            case cls.SEARCH_AUTHOR:
                return cls.SEARCH_AUTHOR
            case cls.SEARCH_YEAR:
                return cls.SEARCH_YEAR
            case _:
                raise ValueError("Invalid value of the search criteria")