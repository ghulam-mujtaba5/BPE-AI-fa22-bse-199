#!/usr/bin/env python3
"""
Extract text labels from draw.io (diagrams.net) shapes in file.xml where the text contains at least one space.

Usage:
  python3 extract_shapes_with_space.py [input_xml] [output_txt]

Defaults:
  input_xml: file.xml (in current directory)
  output_txt: extracted_text_with_space.txt
"""

from __future__ import annotations

import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def html_to_text(s: str) -> str:
    """Convert draw.io's HTML-ish value attribute into plain text.

    - Unescapes XML/HTML entities (including &amp;nbsp; -> space)
    - Converts <br> to newlines (then normalizes whitespace)
    - Strips any remaining HTML tags
    - Collapses horizontal whitespace and trims
    """
    if s is None:
        return ""
    # Unescape twice to handle things like &amp;nbsp; (first &amp; -> &, then &nbsp; -> NBSP)
    s = html.unescape(html.unescape(s))
    # Convert explicit <br> tags into newlines before stripping tags
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    # Remove any remaining HTML tags
    s = re.sub(r"<[^>]+>", "", s)
    # Normalize non-breaking spaces to regular spaces
    s = s.replace("\xa0", " ")
    # Collapse consecutive spaces/tabs to a single space (preserve newlines)
    s = re.sub(r"[ \t]+", " ", s)
    # Replace runs of newlines with a single space (labels are usually single-line)
    s = re.sub(r"\s*\n\s*", " ", s)
    return s.strip()


def extract_labels_with_space(input_path: Path) -> list[str]:
    """Parse the XML and return unique shape labels that contain at least one space."""
    tree = ET.parse(input_path)
    root = tree.getroot()

    results: list[str] = []
    seen: set[str] = set()

    # Iterate through all mxCell elements; consider only vertex shapes (vertex="1")
    for cell in root.iter("mxCell"):
        if cell.get("vertex") != "1":
            continue
        raw_val = cell.get("value")
        if not raw_val:
            continue
        text = html_to_text(raw_val)
        if not text:
            continue
        # Keep only labels that contain at least one space character
        if " " in text and text not in seen:
            results.append(text)
            seen.add(text)

    return results


def main(argv: list[str]) -> int:
    """Command-line interface for label extraction."""
    in_path = Path(argv[1]) if len(argv) > 1 else Path("file.xml")

    if not in_path.exists():
        print(f"Input XML not found: {in_path}")
        return 1

    labels = extract_labels_with_space(in_path)
    print(f"Extracted {len(labels)} label(s) with spaces")
    
    if labels:
        print("\n".join(labels))
    
    return 0 if labels else 1


def get_labels(input_file: str) -> list[str]:
    """Extract labels from XML file.
    
    Args:
        input_file (str): Path to XML file
        
    Returns:
        list[str]: List of extracted labels containing spaces
    """
    in_path = Path(input_file)

    if not in_path.exists():
        raise FileNotFoundError(f"Input XML not found: {in_path}")

    try:
        labels = extract_labels_with_space(in_path)
        return labels
    except Exception as e:
        print(f"Error extracting labels: {e}")
        raise
