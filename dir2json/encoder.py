import os
import json
import base64
from pathlib import Path

def json_encode_dir(
    directory, 
    file_types=('text', 'binary'), 
    metadata=None,
    ignore=None
    ):
    """
    Encode all files in a directory into a JSON format.

    :param directory: Path to the directory to encode.
    :param file_types: Tuple specifying file types to include ('text', 'binary'). Defaults to both.
    :param metadata: List of metadata to include ('file_size', 'creation_time', 'last_modified_time'). Defaults to None.
    :param ignore: List of file names to exclude from encoding. Defaults to None.
    :return: JSON string representing the directory's contents.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    files = [f for f in Path(directory).rglob('*') if f.is_file()]

    if ignore:
        files = [f for f in files if f.name not in ignore]

    bundle = []

    for file in files:
        file_info = {
            'name': str(file.relative_to(directory)),
            'content': None,
            'type': 'binary' if 'binary' in file_types else 'text'
        }

        if 'binary' in file_types and file.suffix.lower() not in text_file_extensions():
            with open(file, 'rb') as f:
                file_info['content'] = base64.b64encode(f.read()).decode('utf-8')
                file_info['type'] = 'binary'
        elif 'text' in file_types:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                file_info['content'] = f.read()
                file_info['type'] = 'text'

        if metadata:
            if 'file_size' in metadata:
                file_info['file_size'] = file.stat().st_size
            if 'creation_time' in metadata:
                file_info['creation_time'] = file.stat().st_ctime
            if 'last_modified_time' in metadata:
                file_info['last_modified_time'] = file.stat().st_mtime

        bundle.append(file_info)

    return json.dumps(bundle, indent=4)

def text_file_extensions():
    """Return a list of common text file extensions."""
    return [
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
    ]