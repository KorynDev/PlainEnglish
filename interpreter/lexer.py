"""
Lexer for PlainEnglish.

Splits a .ple source file into a list of (line_number, raw_sentence) tuples.
Each sentence is everything between two periods (the period is consumed).
Comments (sentences beginning with "Note") are discarded here.
"""

from __future__ import annotations
from typing import List, Tuple
from .errors import missing_period


def lex(source: str, filename: str = "<stdin>") -> List[Tuple[int, str]]:
    """Return a list of (line_number, sentence_text) pairs.

    The *line_number* is the line on which the sentence **starts** (1-based).
    Decimal numbers like ``3.5`` are preserved — the period inside a number
    is NOT treated as a statement terminator.
    """
    sentences: List[Tuple[int, str]] = []
    current_chars: list[str] = []
    start_line = 1
    current_line = 1

    i = 0
    length = len(source)

    while i < length:
        ch = source[i]

        if ch == '\n':
            current_line += 1
            current_chars.append(' ')
            i += 1
            continue

        if ch == '.':
            # Check if this period is part of a decimal number.
            # Decimal: digit(s) before AND digit(s) after the period.
            if i > 0 and i + 1 < length and source[i - 1].isdigit() and source[i + 1].isdigit():
                current_chars.append(ch)
                i += 1
                continue

            # Otherwise, this period terminates a statement.
            sentence = ''.join(current_chars).strip()
            if sentence:
                # Skip comments
                if not sentence.lower().startswith("note ") and sentence.lower() != "note":
                    sentences.append((start_line, sentence))
            current_chars = []
            start_line = current_line
            i += 1
            # Advance start_line past any immediate newline
            continue

        if not current_chars or all(c == ' ' for c in current_chars):
            # We are about to start a new sentence — record its line.
            start_line = current_line

        current_chars.append(ch)
        i += 1

    # If there is trailing text with no period, that's an error.
    leftover = ''.join(current_chars).strip()
    if leftover:
        raise missing_period(current_line)

    return sentences
