#!/usr/bin/env python3
import requests
import re
import json
import sys
from typing import Any, Dict, List, Union

def download_json(url: str) -> Union[Dict, List]:
    """Download JSON from a URL and return as Python dict/list."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def search_json(data: Any, pattern: re.Pattern, path: str = "") -> List[str]:
    """
    Recursively search for pattern in JSON keys/values.
    Returns list of matches with their path and value.
    """
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)):
                results.extend(search_json(v, pattern, new_path))
            else:
                text = str(v)
                if pattern.search(text):
                    results.append(f"{new_path}: {text}")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_path = f"{path}[{idx}]"
            if isinstance(item, (dict, list)):
                results.extend(search_json(item, pattern, new_path))
            else:
                text = str(item)
                if pattern.search(text):
                    results.append(f"{new_path}: {text}")
    return results

if __name__ == "__main__":
    # Example: free JSON placeholder API
    url = "https://jsonplaceholder.typicode.com/posts"

    # Take pattern from CLI args or default to 'facilis'
    pattern_str = sys.argv[1] if len(sys.argv) > 1 else "facilis"
    regex = re.compile(pattern_str, re.IGNORECASE)

    print(f"Downloading JSON from {url} ...")
    data = download_json(url)

    print(f"Searching for pattern '{pattern_str}' ...\n")
    matches = search_json(data, regex)

    if matches:
        for m in matches:
            print(m)
    else:
        print("No matches found.")
# Uses
#python3 internet_download_json.py "sunt"
