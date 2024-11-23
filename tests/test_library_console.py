# import io
import unittest
# import unittest.mock

from app import SimpleLibrary
from book_manager import BookManager
from book_repository import BookRepository
from library_console import LibraryConsole, InputException


class LibraryConsoleTest(unittest.TestCase):
    """ Тестирование библиотечной консоли """
    def setUp(self):
        book_manager = BookManager(BookRepository())
        self.library_manager = LibraryConsole(SimpleLibrary(), book_manager)

    # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    # def assert_stdout(self, expected_output, mock_stdout):
    #     self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_str_status_convert_positive(self):
        """ Проверяет конвертацию вводимого параметра статуса книги """
        for status_str, result in (('a', True), ('available', True),
                                   ('g', False), ('given_out', False)):
            with self.subTest(status_str=status_str, result=result):
                self.assertEqual(self.library_manager._str_status_convert(status_str), result,
                                 msg=f"'{status_str}' is not convert to {result}")

    def test_str_status_convert_negative(self):
        """ Проверяет вызов исключения при вводе неверного статуса книги """
        for status_str in ('b', 'availabl', 'gi', 'given'):
            with self.subTest(str_status=status_str):
                with self.assertRaises(InputException, msg=f"'{status_str}' is not raises exception") as cm:
                    self.library_manager._str_status_convert(status_str)
                self.assertEqual(cm.exception.message, f"Error: Status '{status_str}' is invalid")
