"""Unittest for DataProcessor"""
import unittest
from typing import List

from src.db.processed_manager import ProcessedManager
from src.db.processed_structure import ProcessedStructure


class TestDataProcessor(unittest.TestCase):
    """Class for Unittest of DataProcessor."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_0(self):
        """Unittest for clear_table function."""
        result = ProcessedManager.clear_table()
        self.assertTrue(result)

    def test_1(self):
        """Unittest for insert_data function"""
        data = ProcessedStructure(
            path="/mnt/c/LOCAL_DATA",
            old_filename="example.jpg",
            tags=["tag1", "tag 2"],
            text=["text1", "text2"],
            bboxes=[[0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 1, 1, 2, 2, 3, 3]]
        )
        result = ProcessedManager.insert_data(data)
        self.assertIsInstance(result, int)

    def test_2(self):
        """Another unittest for insert_data function"""
        data = ProcessedStructure(
            path="/mnt/c/LOCAL_DATA",
            old_filename="another_example.jpg",
            new_filename="ama_new_here.jpg",
            tags=None,
            text=["text1", "text2", "text2", "", "", "1909"],
            bboxes=[[0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 1, 1, 2, 2, 3, 3]]
        )
        result = ProcessedManager.insert_data(data)
        self.assertIsInstance(result, int)

    def test_3(self):
        """Unittest for get_data_by_id function."""
        result = ProcessedManager.get_data_by_id(uid=1)
        print(result)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ProcessedStructure)

    def test_4(self):
        """Unittest for insert_new_filename function."""
        new_filename = "amma_new_here.jpg"
        result = ProcessedManager.insert_new_filename(new_filename, uid=1)
        self.assertTrue(result)

    def test_5(self):
        """Unittest for get_text function."""
        uid = None
        result = ProcessedManager.get_text(uid)
        self.assertIsNotNone(result)

    def test_6(self):
        """Unittest for get_all_data function."""
        result = ProcessedManager.get_all_data()
        self.assertIsInstance(result, List)


class TestSuit(unittest.TestSuite):
    """Test Suit to achieve running tests in the specific order."""
    def __init__(self):
        super().__init__()
        self.addTest(TestDataProcessor("test_0"))  # Clear table
        self.addTest(TestDataProcessor("test_1"))  # Insert data
        self.addTest(TestDataProcessor("test_2"))
        self.addTest(TestDataProcessor("test_3"))  # Get element by ID
        self.addTest(TestDataProcessor("test_4"))  # Insert new_filename by its ID
        self.addTest(TestDataProcessor("test_5"))  # Get text


if __name__ == "__main__":
    suite = TestSuit()
    runner = unittest.TextTestRunner()
    runner.run(suite)
