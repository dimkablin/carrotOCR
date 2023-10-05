"""Unittest for DataProcessor"""
import unittest
from src.db.database_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Class for Unittest of DataProcessor."""

    def test_insert_data(self):
        """Unittest for insert_data function"""
        filepath = "example.jpg"
        tags = ["Исследование 1", "Исследование 2"]
        text = ["Татнефть геофизика", "Шевцов"]
        bboxes = [[0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 1, 1, 2, 2, 3, 3]]
        result = DataProcessor.insert_data(filepath, tags, text, bboxes)
        self.assertIsInstance(result, int)

    def test_get_data_by_id(self):
        """Unittest for get_data_by_id function."""
        uid = 1
        result = DataProcessor.get_data_by_id(uid)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_insert_new_filename(self):
        """Unittest for insert_new_filename function."""
        new_filename = "amma_new_here.jpg"
        uid = 1
        result = DataProcessor.insert_new_filename(new_filename, uid)
        self.assertTrue(result)


class TestSuit(unittest.TestSuite):
    """Test Suit to achieve running tests in the specific order."""
    def __init__(self):
        super().__init__()
        self.addTest(TestDataProcessor("test_insert_data"))
        self.addTest(TestDataProcessor("test_insert_new_filename"))
        self.addTest(TestDataProcessor("test_get_data_by_id"))


if __name__ == "__main__":
    suite = TestSuit()
    runner = unittest.TextTestRunner()
    runner.run(suite)
