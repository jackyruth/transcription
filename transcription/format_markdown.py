#!/usr/bin/env python3
"""
Script to organize markdown files by putting each sentence on its own line
with line breaks at column 80.
"""

import re
import sys
from typing import List


def split_sentences(text: str) -> List[str]:
    """Split text into sentences using common sentence boundaries."""
    # Split on sentence endings (.!?) followed by space and capital letter
    # or end of string, but avoid splitting on abbreviations like "Mr."
    pattern = r'(?<!\.\s)(?<!\.\d)(?<=[.!?])\s+(?=[A-Z])'
    sentences = re.split(pattern, text)
    return [s.strip() for s in sentences if s.strip()]


def wrap_line(text: str, width: int = 80) -> str:
    """Wrap text to specified width, preserving word boundaries."""
    if len(text) <= width:
        return text
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        # +1 for space between words
        if current_length + len(word) + (1 if current_line else 0) <= width:
            current_line.append(word)
            current_length += len(word) + (1 if current_line else 0)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)


def process_markdown_file(input_file: str, output_file: str = None) -> None:
    """Process markdown file to organize sentences."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Split into paragraphs (preserve empty lines)
    paragraphs = content.split('\n\n')
    processed_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip() == '':
            processed_paragraphs.append('')
            continue
        
        # Check if it's a markdown header or code block
        if paragraph.startswith('#') or paragraph.startswith('```'):
            processed_paragraphs.append(paragraph)
            continue
        
        # Process regular text paragraphs
        sentences = split_sentences(paragraph)
        processed_sentences = []
        
        for sentence in sentences:
            wrapped_sentence = wrap_line(sentence, 80)
            processed_sentences.append(wrapped_sentence)
        
        processed_paragraphs.append('\n'.join(processed_sentences))
    
    result = '\n\n'.join(processed_paragraphs)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Processed file saved to: {output_file}")
    else:
        print(result)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python format_markdown.py <input_file> [output_file]")
        print("If output_file is not provided, result is printed to stdout.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_markdown_file(input_file, output_file)


if __name__ == "__main__":
    main()