# pylint: disable=W
"""Tests fro the API"""
import unittest
import requests

BASE_URL = "http://localhost:8000/api"


class APITestCaseFiles(unittest.TestCase):
    """Test cases for API """
    def test_get_files(self):
        """ /api/get-files/ """
        url = BASE_URL+'/get-files/'
        body = {
            "count": -1,
            "path": "/"
        }
        response = requests.post(url, json=body)
        self.assertEqual(response.status_code, 200)

    def test_get_file(self):
        """ /api/get-file/?uid=1 """
        file_uid = 1
        url = BASE_URL+f'/get-file/?uid={file_uid}'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_folders(self):
        """ /api/get-folders/?uid=1 """
        url = BASE_URL+'/get-folders/'
        body = {
            "count": -1,
            "path": "/"
        }
        response = requests.post(url, json=body)
        self.assertEqual(response.status_code, 200)


class APITestCasePipeline(unittest.TestCase):
    """ Tests the APITest pipeline"""

    def test_get_chunk_id(self):
        """ /api/get-chunk-id/ """
        url = BASE_URL+'/get-chunk-id'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_upload_files(self):
        """ /api/upload-files/ """
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_process_chunk(self):
        """ /api/process-chunk/ """
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_process_image(self):
        """/api/process-image/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_processed(self):
        """/api/get-processed/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delte_data_by_id(self):
        """/api/delte-data-by-id/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_filename(self):
        """/api/add-filename/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_archive_chunk(self):
        """/api/archive-chunk/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)


class APITestCaseOCR(unittest.TestCase):
    """ Tests the APITest OCR"""
    def test_get_ocr_models(self):
        """/api/get-ocr-models/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_current_ocr_model(self):
        """/api/get-current-ocr-model/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_change_ocr_model(self):
        """/api/change-ocr-model/"""
        url = BASE_URL
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
