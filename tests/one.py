import unittest

from app import SimpleLibrary


class SimpleLibraryTest(unittest.TestCase):
    def setUp(self):
        self.simple_library = SimpleLibrary()
