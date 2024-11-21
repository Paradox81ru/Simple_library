
class SimpleLibraryException(Exception):
    """ Общее исключение библиотеки книг """
    def __init__(self, msg):
        self._msg = msg

    @property
    def message(self):
        return self._msg


class InputException(SimpleLibraryException):
    """ Исключение при вводе данных с консоли """
    pass


class BookRepositoryError(SimpleLibraryException):
    """ Класс ошибки репозитория книг """
    pass