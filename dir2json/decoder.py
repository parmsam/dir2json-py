import os
import json
import base64
from pathlib import Path

def json_decode_dir(json_data, target_directory):
    """
    Decode a JSON string into a directory structure.

    :param json_data: JSON string representing the directory's contents.
    :param target_directory: Path to the target directory.
    :return: None. Creates files in the specified directory.
    """
    data = json.loads(json_data)

    os.makedirs(target_directory, exist_ok=True)

    for file in data:
        file_path = Path(target_directory) / file['name']
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file.get('type') == 'binary':
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(file['content']))
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file['content'])