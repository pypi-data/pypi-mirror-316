# -----------------------------------------------------------------------------
# Copyright (c) 2024 Damien Pageot.
#
# This file is part of Your Project Name.
#
# Licensed under the MIT License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
# -----------------------------------------------------------------------------

"""
Markdown Code Block Parser

This module provides functions to parse Markdown files and extract code blocks based on specific
patterns. It focuses on identifying code blocks with associated metadata such as language, name,
and tag.

Functions:
    - compile_pattern: Compile a regular expression pattern to match code blocks in Markdown files.
    - parse_markdown: Parse a Markdown file to extract code blocks and their metadata.

The parsing functionality relies on regular expressions to identify and extract code blocks that
include specified languages and metadata. The extracted code blocks are returned as a list of
dictionaries containing relevant information.

Usage:
    - Use `compile_pattern` to create a regular expression pattern for matching code blocks.
    - Use `parse_markdown` to read a Markdown file and extract code blocks based on the compiled
      pattern and provided languages.
"""

import re


def compile_pattern(languages: list) -> re.Pattern:
    """
    Compile the regular expression pattern for matching code blocks.

    Args:
        languages (List[str]): List of valid languages.

    Returns:
        re.Pattern: Compiled regex pattern for parsing code blocks.
    """
    return re.compile(
        rf"```({('|').join(languages)}) \{{name=(.*?)(?:,\s*tag=(.*?))?\}}\s*([\s\S]*?)\s*```",
        re.DOTALL,
    )


def detect_shebang(content: str) -> str:
    """
    Detect the shebang used in the code block.

    Args:
        content (str): The content of the code block.

    Returns:
        str: The shebang used in the code block.
    """
    shebang_pattern = r"^#!\s*(\/usr\/bin\/env\s+)?(\S+)"
    match = re.search(shebang_pattern, content, re.MULTILINE)

    if match:
        return f"{match.group(1)}{match.group(2)}" if match.group(1) else match.group(2)

    return None


def parse_markdown(file_path: str, languages: list) -> list:
    """
    Parse the Markdown file to extract code blocks with names.

    Args:
        file_path (str): Path to the Markdown file.
        languages (list): List of valid languages.

    Returns:
        list: List of dictionaries containing code block information
            or an empty List if file not found.
    """
    pattern = compile_pattern(languages)
    try:
        with open(file_path, "r") as file:
            content = file.read()

        matches = pattern.findall(content)
        shebang = detect_shebang(content)

        blocklist = [
            {
                "name": shebang if (shebang is not None) else name.strip(),
                "tag": tag,
                "file": file_path,
                "lang": lang,
                "code": code.strip(),
                "exec": lang in languages,
            }
            for lang, name, tag, code in matches
        ]

        return blocklist

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return []
