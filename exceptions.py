
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

class BookRepositoryExportException(SimpleLibraryException):
    """ Исключение в случае проблем с загрузкой данных из файла """
    pass


class BookManagerError(SimpleLibraryException):
    """ Класс ошибки менеджера книг """
    pass

class ValidationError(SimpleLibraryException):
    """ Класс ошибки валидации """
    pass