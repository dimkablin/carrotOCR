"""Unittest for src/db/api"""
import unittest

from src.api.models.get_f import GetFRequest
from src.api.services.find_duplicate import find_duplicate_service
from src.api.services.get_folders import get_folders_service
from src.db.processed_manager import ProcessedManager
from src.db.processed_structure import ProcessedStructure
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
        data = ProcessedStructure(
            directory="/mnt/c/LOCAL_DATA",
            old_filename="example.jpg",
            text=text1.split(" ")
        )

        result = ProcessedManager.insert_data(data)
        self.assertIsNotNone(result)

        # And now we can check this function out
        result = find_duplicate_service(text2)
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
