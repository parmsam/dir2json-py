import os
import json
import tempfile
import pytest
import base64
from dir2json.encoder import json_encode_dir

def test_json_encode_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample files
        file_path_1 = os.path.join(temp_dir, 'file1.txt')
        file_path_2 = os.path.join(temp_dir, 'file2.bin')

        with open(file_path_1, 'w') as f:
            f.write('Hello, World!')

        with open(file_path_2, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')

        # Encode directory
        result = json_encode_dir(temp_dir, file_types=('text', 'binary'), metadata=['file_size'])
        result_json = json.loads(result)

        # Sort the result by file name to ensure consistent order
        result_json = sorted(result_json, key=lambda x: x['name'])

        # Decode Base64 content for assertions
        result_json[0]['content'] = base64.b64decode(result_json[0]['content']).decode('utf-8')

        # Assertions
        assert len(result_json) == 2
        assert result_json[0]['name'] == 'file1.txt'
        assert result_json[0]['content'] == 'Hello, World!'
        assert 'file_size' in result_json[0]

        assert result_json[1]['name'] == 'file2.bin'
        assert result_json[1]['type'] == 'binary'
        assert 'file_size' in result_json[1]

def test_encode_directory_with_ignore():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample files
        file_path_1 = os.path.join(temp_dir, 'file1.txt')
        file_path_2 = os.path.join(temp_dir, 'file2.txt')

        with open(file_path_1, 'w') as f:
            f.write('File 1 content')

        with open(file_path_2, 'w') as f:
            f.write('File 2 content')

        # Encode directory with ignore
        result = json_encode_dir(temp_dir, ignore=['file2.txt'])
        result_json = json.loads(result)

        # Sort the result by file name to ensure consistent order
        result_json = sorted(result_json, key=lambda x: x['name'])

        # Assertions
        assert len(result_json) == 1
        assert result_json[0]['name'] == 'file1.txt'