
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
    """ Класс ошибки хранилища книг """
    pass

class BookRepositoryExportException(SimpleLibraryException):
    """ Исключение в случае проблем с загрузкой данных из файла """
    pass


class BookManagerError(SimpleLibraryException):
    """ Класс ошибки менеджера книг """
    pass

class ValidationError(SimpleLibraryException):
    """ Класс ошибки валидации """
    def __init__(self, msg: str, var_name: str, value):
        super().__init__(msg)
        self._var_name = var_name
        self._value = value

    @property
    def var_name(self):
        return self._var_name

    @property
    def value(self):
        return self._value