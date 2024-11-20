from functools import partial
import unittest

from app import SimpleLibrary
from manager import Manager, InputException


class ManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager(SimpleLibrary())

    def test_str_status_convert_positive(self):
        """ Проверяет конвертацию вводимого параметра статуса книги """
        for str_status, result in (('a', True), ('available', True),
                                   ('g', False), ('given_out', False)):

            self.assertEquals(self.manager._str_status_convert(str_status), result)

    def test_str_status_convert_negative(self):
        """ Проверяет вызов исключения при вводе неверного статуса """
        for status_str in ('b', 'availabl', 'gi', 'given'):
            with self.assertRaises(InputException, msg=f"'{status_str}' is not raises exception") as cm:
                self.manager._str_status_convert(status_str)
            self.assertEquals(cm.exception.message, f"Status '{status_str}' is invalid")
