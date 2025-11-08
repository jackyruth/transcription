import re
import sys
from typing import List


class MarkdownFormatter:
    """
    Script to organize markdown files by putting each sentence on its own line
    with line breaks when the line is over a certain column.
    """

    def __init__(self, line_width: int = 80) -> None:
        """
        Initialize the MarkdownFormatter with configuration.

        Args:
            line_width: Maximum line width for text wrapping
        """
        self.line_width = line_width

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences using common sentence boundaries."""
        # Split on sentence endings (.!?) followed by space and capital letter
        # or end of string, but avoid splitting on abbreviations like "Mr."
        pattern = r"(?<!\.\s)(?<!\.\d)(?<=[.!?])\s+(?=[A-Z])"
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def _wrap_line(self, text: str) -> str:
        """Wrap text to specified width, preserving word boundaries."""
        if len(text) <= self.line_width:
            return text

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            # +1 for space between words
            if (
                current_length + len(word) + (1 if current_line else 0)
                <= self.line_width
            ):
                current_line.append(word)
                current_length += len(word) + (1 if current_line else 0)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)

    def process_content(self, content: str) -> str:
        """
        Process markdown content to organize sentences and wrap lines.

        Args:
            content: Raw markdown content to process

        Returns:
            Processed markdown content
        """
        # Split into paragraphs (preserve empty lines)
        paragraphs = content.split("\n\n")
        processed_paragraphs = []

        for paragraph in paragraphs:
            if paragraph.strip() == "":
                processed_paragraphs.append("")
                continue

            # Check if it's a markdown header or code block
            if paragraph.startswith("#") or paragraph.startswith("```"):
                processed_paragraphs.append(paragraph)
                continue

            # Process regular text paragraphs
            sentences = self._split_sentences(paragraph)
            processed_sentences = []

            for sentence in sentences:
                wrapped_sentence = self._wrap_line(sentence)
                processed_sentences.append(wrapped_sentence)

            processed_paragraphs.append("\n".join(processed_sentences))

        return "\n\n".join(processed_paragraphs)

    def process_file(self, input_file: str, output_file: str = None) -> None:
        """
        Process a markdown file and output to stdout or file.

        Args:
            input_file: Path to the input markdown file
            output_file: Optional path for output file (defaults to stdout)
        """
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.", file=sys.stderr)
            sys.exit(1)

        processed_content = self.process_content(content)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(processed_content)
            print(f"Processed file saved to: {output_file}", file=sys.stderr)
        else:
            # Output to stdout for piping
            print(processed_content)
