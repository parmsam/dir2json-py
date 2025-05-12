import os
import json
import base64
import time
from pathlib import Path

def json_encode_dir(
    directory, 
    file_types=('text', 'binary'), 
    metadata=None,
    ignore=None
    ):
    """
    Encode all files in a directory into a JSON format.

    Parameters
    ----------
    directory : str
        Path to the directory to encode.
    file_types : tuple of str, optional
        Tuple specifying file types to include ('text', 'binary'). Defaults to both.
    metadata : list of str, optional
        List of metadata to include ('file_size', 'creation_time', 'last_modified_time'). Defaults to None.
    ignore : list of str, optional
        List of file names to exclude from encoding. Defaults to None.

    Returns
    -------
    str
        JSON string representing the directory's contents.

    Raises
    ------
    ValueError
        If the specified directory does not exist.

    Examples
    --------
    >>> json_encode_dir('/path/to/dir', file_types=('text',), metadata=['file_size'])
    '{"name": "file1.txt", "content": "Hello, World!", "type": "text", "file_size": 123}'
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    files = [f for f in Path(directory).rglob('*') if f.is_file()]

    if ignore:
        ignore_set = set(ignore)  # Convert ignore list to set for faster lookup
        files = [f for f in files if f.name not in ignore_set]

    bundle = []

    for file in files:
        file_info = {
            'name': str(file.relative_to(directory)),
            'content': None,
            'type': None
        }
        normalized_suffix = file.suffix.lower().lstrip('.')  # Normalize suffix by stripping the leading dot
        try:
            if normalized_suffix in text_file_extensions():
                if 'text' in file_types:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        file_info['content'] = f.read()
                        file_info['type'] = 'text'
            elif 'binary' in file_types:
                with open(file, 'rb') as f:
                    file_info['content'] = base64.b64encode(f.read()).decode('utf-8')
                    file_info['type'] = 'binary'

            if metadata:
                if 'file_size' in metadata:
                    file_info['file_size'] = f"{file.stat().st_size} bytes"
                if 'creation_time' in metadata:
                    file_info['creation_time'] = time.ctime(file.stat().st_ctime)
                if 'last_modified_time' in metadata:
                    file_info['last_modified_time'] = time.ctime(file.stat().st_mtime)

        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        bundle.append(file_info)

    return json.dumps(bundle, separators=(',', ':'))

def text_file_extensions():
    """
    Return a list of common text file extensions.

    Returns
    -------
    set of str
        A set of common text file extensions.

    Examples
    --------
    >>> text_file_extensions()
    {'py', 'txt', 'md', 'html', 'json', ...}
    """
    return {
        "r", "rmd", "rnw", "rpres", "rhtml", "qmd",
        "py", "ipynb", "js", "ts", "jl", "sas",
        "html", "css", "scss", "less", "sass",
        "tex", "txt", "md", "markdown", "html", "htm",
        "json", "yml", "yaml", "xml", "svg", "yml",
        "sh", "bash", "zsh", "fish", "bat", "cmd",
        "sql", "csv", "tsv", "tab",
        "log", "dcf", "ini", "cfg", "conf", "properties", "env", "envrc",
        "gitignore", "gitattributes", "gitmodules", "gitconfig", "gitkeep",
        "htaccess", "htpasswd", "htgroups", "htdigest"
    }
