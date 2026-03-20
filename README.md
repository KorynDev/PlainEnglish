# PlainEnglish

> A programming language you can read like a book.

PlainEnglish is a beginner-friendly, imperative programming language where every statement reads as a natural English sentence. Source files use the `.ple` extension and contain **only** English words, spaces, commas, and periods — no brackets, braces, operators, or special characters.

---

## Quick Start

### 1. Write a Program

Create a file called `hello.ple`:

```
Let name be "World".
Display "Hello,", name.
```

### 2. Run It

```bash
python plainenglish.py hello.ple
```

**Output:**
```
Hello, World
```

### Requirements

- Python 3.10 or later
- No external dependencies

---

## What Can You Do?

| Feature | Example |
|---|---|
| **Variables** | `Let score be 0.` |
| **Math** | `Set total to price times quantity.` |
| **Conditions** | `If score is greater than 50, then.` |
| **Counted loops** | `Repeat 10 times.` |
| **While loops** | `While running is true, repeat.` |
| **For-each loops** | `For each item in list.` |
| **Input** | `Ask "What is your name?" and store it in name.` |
| **Output** | `Display "Hello,", name.` |
| **Functions** | `Define a function called greet that takes person.` |
| **Lists** | `Let colours be a list containing "red", "green", "blue".` |
| **Libraries** | `Use math.` |

---

## Example Programs

### Greeting (`examples/greeting.ple`)
Asks for your name and age, prints a personalised message.

### Even Numbers (`examples/even_numbers.ple`)
Prints every even number from 1 to 100.

### Factorial (`examples/factorial.ple`)
Defines a recursive factorial function and prints the factorial of 5.

### Full Demo (`examples/demo.ple`)
Exercises every feature of the language in one file.

---

## Project Structure

```
PlainEnglish/
  plainenglish.py          CLI entry point
  interpreter/
    __init__.py
    lexer.py               Splits source into sentences
    parser.py              Builds an Abstract Syntax Tree
    ast_nodes.py           AST node definitions
    interpreter.py         Tree-walking evaluator
    errors.py              Beginner-friendly error messages
  examples/
    greeting.ple
    even_numbers.ple
    factorial.ple
    demo.ple
    math_demo.ple
    graphics_demo.ple
  libs/                    Standard libraries
    __init__.py
    math_lib.py
    graphics_lib.py
    input_lib.py
    random_lib.py
    time_lib.py
    text_lib.py
    file_lib.py
    system_lib.py
    dictionary_lib.py
    network_lib.py
    json_lib.py
    type_lib.py
    regex_lib.py
    csv_lib.py
    base64_lib.py
    crypto_lib.py
    dialog_lib.py
    database_lib.py
  spec/
    SPECIFICATION.md       Full language specification
  docs/
    cheatsheet.md          One-page quick reference
  vscode-extension/        VSCode syntax highlighting
    package.json
    language-configuration.json
    syntaxes/
      plainenglish.tmLanguage.json
```

---

## VSCode Extension

To get syntax highlighting for `.ple` files:

1. Copy the `vscode-extension` folder into your VSCode extensions directory:
   - **Windows:** `%USERPROFILE%\.vscode\extensions\plainenglish`
   - **macOS/Linux:** `~/.vscode/extensions/plainenglish`
2. Restart VSCode.
3. Open any `.ple` file — keywords, numbers, and comments will be highlighted.

---

## Language Rules

1. Only `,` and `.` are allowed — no other symbols.
2. Every statement ends with a period.
3. Commas separate items in lists and parameters.
4. Blocks use English keywords (`End if`, `End repeat`, etc.), not indentation.
5. Everything is case-insensitive.
6. Error messages are written in plain English.

---

## License

MIT
