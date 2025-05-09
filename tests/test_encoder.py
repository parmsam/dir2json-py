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

        # Assertions for text file
        assert result_json[0]['name'] == 'file1.txt'
        assert result_json[0]['content'] == 'Hello, World!'
        assert result_json[0]['type'] == 'text'
        assert 'file_size' in result_json[0]

        # Assertions for binary file
        assert result_json[1]['name'] == 'file2.bin'
        assert result_json[1]['type'] == 'binary'
        assert 'file_size' in result_json[1]
        decoded_binary_content = base64.b64decode(result_json[1]['content'])
        assert decoded_binary_content == b'\x00\x01\x02\x03'

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

def test_json_encode_multiple_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple sample files
        file_paths = [
            os.path.join(temp_dir, f'file{i}.txt') for i in range(1, 6)
        ]

        for i, file_path in enumerate(file_paths):
            with open(file_path, 'w') as f:
                f.write(f'Content of file {i + 1}')

        # Encode directory
        result = json_encode_dir(temp_dir, file_types=('text',))
        result_json = json.loads(result)

        # Sort the result by file name to ensure consistent order
        result_json = sorted(result_json, key=lambda x: x['name'])

        # Assertions
        assert len(result_json) == len(file_paths)
        for i, file_info in enumerate(result_json):
            assert file_info['name'] == f'file{i + 1}.txt'
            assert file_info['content'] == f'Content of file {i + 1}'
            assert file_info['type'] == 'text'

def test_json_encode_with_metadata():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample file
        file_path = os.path.join(temp_dir, 'sample.txt')
        with open(file_path, 'w') as f:
            f.write('Sample content')

        # Encode directory with metadata
        result = json_encode_dir(temp_dir, metadata=['file_size', 'creation_time', 'last_modified_time'])
        result_json = json.loads(result)

        # Assertions
        assert len(result_json) == 1
        assert result_json[0]['name'] == 'sample.txt'
        assert 'file_size' in result_json[0]
        assert 'creation_time' in result_json[0]
        assert 'last_modified_time' in result_json[0]

def test_json_encode_various_file_types():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample files of various types
        file_path_py = os.path.join(temp_dir, 'script.py')
        file_path_r = os.path.join(temp_dir, 'analysis.R')
        file_path_log = os.path.join(temp_dir, 'output.log')

        with open(file_path_py, 'w') as f:
            f.write('print("Hello, Python!")')

        with open(file_path_r, 'w') as f:
            f.write('print("Hello, R!")')

        with open(file_path_log, 'w') as f:
            f.write('Log entry: Process started.')

        # Encode directory
        result = json_encode_dir(temp_dir, file_types=('text',))
        result_json = json.loads(result)

        # Sort the result by file name to ensure consistent order
        result_json = sorted(result_json, key=lambda x: x['name'])

        # Assertions
        assert len(result_json) == 3
        assert result_json[0]['name'] == 'analysis.R'
        assert result_json[0]['content'] == 'print("Hello, R!")'
        assert result_json[0]['type'] == 'text'

        assert result_json[1]['name'] == 'output.log'
        assert result_json[1]['content'] == 'Log entry: Process started.'
        assert result_json[1]['type'] == 'text'

        assert result_json[2]['name'] == 'script.py'
        assert result_json[2]['content'] == 'print("Hello, Python!")'
        assert result_json[2]['type'] == 'text'

def test_json_encode_file_types_correctness():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample files
        text_file = os.path.join(temp_dir, 'example.txt')
        binary_file = os.path.join(temp_dir, 'example.bin')

        with open(text_file, 'w') as f:
            f.write('This is a text file.')

        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')

        # Encode directory
        result = json_encode_dir(temp_dir, file_types=('text', 'binary'))
        result_json = json.loads(result)

        # Sort the result by file name to ensure consistent order
        result_json = sorted(result_json, key=lambda x: x['name'])

        # Assertions
        assert len(result_json) == 2
        assert result_json[0]['name'] == 'example.bin'
        assert result_json[0]['type'] == 'binary'

        assert result_json[1]['name'] == 'example.txt'
        assert result_json[1]['type'] == 'text'