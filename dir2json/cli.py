# cli.py
import argparse
from dir2json.encoder import json_encode_dir

def main():
    parser = argparse.ArgumentParser(description="Encode a directory into JSON format.")
    parser.add_argument("directory", help="Path to the directory to encode.")
    parser.add_argument("--file-types", nargs="+", default=["text", "binary"], help="File types to include (e.g., text, binary). Defaults to both.")
    parser.add_argument("--metadata", nargs="+", help="Metadata to include (e.g., file_size, creation_time, last_modified_time).")
    parser.add_argument("--ignore", nargs="+", help="List of file names to exclude from encoding.")

    args = parser.parse_args()

    try:
        result = json_encode_dir(
            directory=args.directory,
            file_types=tuple(args.file_types),
            metadata=args.metadata,
            ignore=args.ignore
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()