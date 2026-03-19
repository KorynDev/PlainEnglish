#!/usr/bin/env python3
"""
PlainEnglish Interpreter — CLI Entry Point

Usage:
    python plainenglish.py <file.ple>

Reads a .ple source file and executes it.
"""

import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interpreter.lexer import lex
from interpreter.parser import parse
from interpreter.interpreter import Interpreter
from interpreter.errors import PlainEnglishError, file_not_found, empty_program


def main():
    if len(sys.argv) < 2:
        print("PlainEnglish Interpreter v1.0")
        print("Usage: python plainenglish.py <file.ple>")
        print()
        print("Example: python plainenglish.py examples/greeting.ple")
        sys.exit(0)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(str(file_not_found(filename)))
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except OSError as e:
        print(f"I had trouble reading the file: {e}")
        sys.exit(1)

    if not source.strip():
        print(str(empty_program(filename)))
        sys.exit(1)

    try:
        sentences = lex(source, filename)
        program = parse(sentences)
        interpreter = Interpreter()
        interpreter.run(program)
    except PlainEnglishError as e:
        print(f"\nOops! {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        sys.exit(0)


if __name__ == '__main__':
    main()
