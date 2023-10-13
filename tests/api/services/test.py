"""Unittest for src/db/api"""
import unittest

from src.api.models.get_f import GetFRequest
from src.api.services.check_text_in_db import check_text_in_db
from src.api.services.get_folders import get_folders_service
from src.db.database_processor import DataProcessor
from src.utils.utils import get_abspath


class TestAPI(unittest.TestCase):
    """Class for Unittest of src/db/api."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_1(self):
        """unittest for check_file_has_processed."""
        with open(get_abspath("notebooks/data/similar_texts.txt"), 'r', encoding='utf-8') as file:
            text1 = file.readline()
            text2 = file.readline()

        # Firstly we should insert simular text into the DB
        data = ("another_example.jpg", [], text1.split(" "),
                [[0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 1, 1, 2, 2, 3, 3]])

        result = DataProcessor.insert_data(*data)
        self.assertIsNotNone(result)

        # And now we can check this function out
        result = check_text_in_db(text2)
        print(result)

    async def test_2(self):
        """unittest for get_folders_service."""
        req = GetFRequest(path='/mnt/c/')
        result = await get_folders_service(req)
        self.assertIsNotNone(result)


class TestSuit(unittest.TestSuite):
    """Test Suit to achieve running tests in the specific order."""
    def __init__(self):
        super().__init__()
        self.addTest(TestAPI("test_1"))  # check_text_in_db


if __name__ == "__main__":
    suite = TestSuit()
    runner = unittest.TextTestRunner()
    runner.run(suite)
