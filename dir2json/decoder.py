import os
import json
import base64
from pathlib import Path

def json_decode_dir(json_data, target_directory):
    """
    Decode a JSON representation of a directory back into its original structure.

    Parameters
    ----------
    json_data : str
        JSON string representing the directory's contents.
    target_directory : str
        Path to the directory where the decoded files will be saved.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the JSON data is invalid or the output directory cannot be created.

    Examples
    --------
    >>> json_decode_dir('{"name": "file1.txt", "content": "Hello, World!", "type": "text"}', '/path/to/output')
    # Decodes the JSON and creates the file `file1.txt` in the specified output directory.
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