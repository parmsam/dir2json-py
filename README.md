# dir2json


dir2json is a Python library for encoding and decoding directory
structures to and from JSON format.

## Features

-   Encode a directory structure into a JSON string.
-   Decode a JSON string back into a directory structure.

## Installation

<!-- To install the package, run the following command:

```bash
pip install .
``` -->

You can install it directly from Github using:

``` bash
pip install git+https://github.com/parmsam/dir2json-py.git
```

## Usage

### Encoding a Directory

``` python
import tempfile
import os
from dir2json.encoder import json_encode_dir

# Let's create temp directory for this example
temp_dir = tempfile.mkdtemp()
# Create a sample file in the temp directory
with open(os.path.join(temp_dir, 'example1.py'), 'w') as f:
    f.write('print("Hello, World!")')
# Create another sample file
with open(os.path.join(temp_dir, 'example2.py'), 'w') as f:
    f.write('print("Hello, again!")')
# Provide the directory path to the function
json_data = json_encode_dir(temp_dir, file_types=['text'])

print(json_data)
```

    [{"name":"example1.py","content":"print(\"Hello, World!\")","type":"text"},{"name":"example2.py","content":"print(\"Hello, again!\")","type":"text"}]

### Decoding a JSON String

``` python
from dir2json.decoder import json_decode_dir

# Provide the JSON string and the target directory path
json_data = '{"name": "example.txt", "content": "Hello world", "type": "text"}'
json_decode_dir(json_data, '/path/to/target')
```

## CLI Usage

`dir2json` also provides a command-line interface (CLI) for encoding
directories into JSON format.

### Encoding a Directory via CLI

To encode a directory, run the following command:

``` bash
python -m dir2json.cli /path/to/directory --file-types text binary --metadata file_size creation_time --ignore .DS_Store
```

#### Arguments:

-   `directory`: Path to the directory to encode.
-   `--file-types`: (Optional) Specify file types to include (e.g.,
    `text`, `binary`). Defaults to both.
-   `--metadata`: (Optional) Specify metadata to include (e.g.,
    `file_size`, `creation_time`, `last_modified_time`).
-   `--ignore`: (Optional) List of file names to exclude from encoding.

The encoded JSON will be printed to the console.

## License

This project is licensed under the MIT License.
