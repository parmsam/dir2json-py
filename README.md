# dir2json

dir2json is a Python library for encoding and decoding directory structures to and from JSON format.

## Features
- Encode a directory structure into a JSON string.
- Decode a JSON string back into a directory structure.

## Installation

<!-- To install the package, run the following command:

```bash
pip install .
``` -->

You can install it directly from Github using:

```bash
pip install git+https://github.com/yourusername/dir2json.git
```

## Usage

### Encoding a Directory

```python
from dir2json.encoder import encode_directory_to_json

# Provide the path to the directory you want to encode
json_data = encode_directory_to_json('/path/to/directory')
print(json_data)
```

### Decoding a JSON String

```python
from dir2json.decoder import decode_json_to_directory

# Provide the JSON string and the target directory path
json_data = '{"name": "example.txt", "content": "SGVsbG8gd29ybGQ=", "type": "binary"}'
decode_json_to_directory(json_data, '/path/to/target')
```

## License

This project is licensed under the MIT License.