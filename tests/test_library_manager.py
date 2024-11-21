import unittest

from app import SimpleLibrary
from library_manager import LibraryManager, InputException


class LibraryManagerTest(unittest.TestCase):
    """ Тестирование управление библиотекой """
    def setUp(self):
        self.manager = LibraryManager(SimpleLibrary())

    def test_str_status_convert_positive(self):
        """ Проверяет конвертацию вводимого параметра статуса книги """
        for status_str, result in (('a', True), ('available', True),
                                   ('g', False), ('given_out', False)):
            with self.subTest(status_str=status_str, result=result):
                self.assertEqual(self.manager._str_status_convert(status_str), result,
                              msg=f"'{status_str}' is not convert to {result}")

    def test_str_status_convert_negative(self):
        """ Проверяет вызов исключения при вводе неверного статуса книги """
        for status_str in ('b', 'availabl', 'gi', 'given'):
            with self.subTest(str_status=status_str):
                with self.assertRaises(InputException, msg=f"'{status_str}' is not raises exception") as cm:
                    self.manager._str_status_convert(status_str)
                self.assertEqual(cm.exception.message, f"Error: Status '{status_str}' is invalid")
