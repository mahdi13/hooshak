import unittest


class BaseHooshakTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def setup_mockup(cls):
        pass
