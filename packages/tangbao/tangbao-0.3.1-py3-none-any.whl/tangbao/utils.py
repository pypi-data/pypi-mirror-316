from contextlib import contextmanager
from io import StringIO
import sys
import pandas as pd
import os
from typing import Dict, Any

def extract_code_from_log(file_path):
    """
    Extracts code snippets from a log file.

    Args:
        file_path (str): The path to the log file.

    Returns:
        str: The extracted code snippet.

    Example:
        code_snippet = extract_code_from_log('path/to/log.txt')
        print(code_snippet)
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    indices_code_running = [i for i, line in enumerate(lines) if "Code running:" in line]
    if len(indices_code_running) < 1:
        return "No code in the log"
    start_index = indices_code_running[-1]

    indices_triple_backtick = [i for i, line in enumerate(lines) if "```" in line]
    if not indices_triple_backtick:
        raise ValueError("The phrase '```' does not occur in the file.")
    end_index = indices_triple_backtick[-1]

    extracted_lines = lines[start_index+2:end_index]

    return ''.join(extracted_lines)

def get_file_ext(x):
    """
    Returns the file extension of a given filename.

    Args:
        x (str): The filename.

    Returns:
        str: The file extension.

    Example:
        ext = get_file_ext("example.png")
        print(ext)  # Output: .png
    """
    assert isinstance(x, str)
    return os.path.splitext(x)[1].lower()

def extract_source(rag_output: Dict[str, Any]) -> str:
    text = ""
    titles = []
    for i, context in enumerate(rag_output["docs"], start=1):
        titles.append(context['metadata']['Source'])
        text += (
            f"<b>Chunk {i}:</b>"
            f"<br>"
            f"<u>Document name</u>: {context['metadata']['Source']}"
            f"<br>"
            f"<u>Page</u>: {context['metadata']['Page']}"
            f"<br>"
            f"<u>Content</u>: <em>{context['text']}</em>"
            f"<br><br>"
        )
    return text, titles