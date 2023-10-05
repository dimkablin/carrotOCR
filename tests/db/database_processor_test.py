"""Unittest for DataProcessor"""
import unittest
from src.db.database_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Class for Unittest of DataProcessor."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_0(self):
        """Unittest for clear_table function."""
        result = DataProcessor.clear_table()
        self.assertTrue(result)

    def test_1(self):
        """Unittest for insert_data function"""
        filepath = "example.jpg"
        tags = ["tag1", "tag 2"]
        text = ["text1", "text2"]
        bboxes = [[0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 1, 1, 2, 2, 3, 3]]
        result = DataProcessor.insert_data(filepath, tags, text, bboxes)
        self.assertIsInstance(result, int)

    def test_2(self):
        """Unittest for get_data_by_id function."""
        result = DataProcessor.get_data_by_id(uid=1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_3(self):
        """Unittest for insert_new_filename function."""
        new_filename = "amma_new_here.jpg"
        result = DataProcessor.insert_new_filename(new_filename, uid=1)
        self.assertTrue(result)


class TestSuit(unittest.TestSuite):
    """Test Suit to achieve running tests in the specific order."""
    def __init__(self):
        super().__init__()
        self.addTest(TestDataProcessor("test_0"))
        self.addTest(TestDataProcessor("test_1"))
        self.addTest(TestDataProcessor("test_2"))
        self.addTest(TestDataProcessor("test_3"))


if __name__ == "__main__":
    suite = TestSuit()
    runner = unittest.TextTestRunner()
    runner.run(suite)
