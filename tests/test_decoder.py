import os
import json
import base64
import shutil
import unittest
from pathlib import Path
from dir2json.decoder import json_decode_dir

class TestDecodeJsonToDirectory(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_output'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_decode_text_file(self):
        json_data = json.dumps([
            {"name": "example.txt", "content": "Hello, world!", "type": "text"}
        ])
        json_decode_dir(json_data, self.test_dir)
        
        file_path = Path(self.test_dir) / 'example.txt'
        self.assertTrue(file_path.exists())
        with open(file_path, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), "Hello, world!")

    def test_decode_binary_file(self):
        content = base64.b64encode(b"binary data").decode('utf-8')
        json_data = json.dumps([
            {"name": "example.bin", "content": content, "type": "binary"}
        ])
        json_decode_dir(json_data, self.test_dir)
        
        file_path = Path(self.test_dir) / 'example.bin'
        self.assertTrue(file_path.exists())
        with open(file_path, 'rb') as f:
            self.assertEqual(f.read(), b"binary data")

if __name__ == '__main__':
    unittest.main()