# PlainEnglish Language Specification

**Version:** 1.0  
**File extension:** `.ple`  
**Permitted symbols:** Comma `,` and Period `.` only  
**Paradigm:** Imperative, beginner-friendly, human-readable  

---

## 1. General Rules

1. A PlainEnglish source file is a sequence of **statements**.
2. Every statement ends with a **period** `.`.
3. A **comma** `,` separates items within a statement (list items, parameters).
4. No other punctuation, brackets, braces, operators, sigils, or special characters may appear.
5. Statements are **case-insensitive** for keywords. Variable and function names are case-insensitive.
6. **Comments** begin with the word `Note` and end with a period. They are ignored by the interpreter.
7. Blank lines are ignored.
8. Block structures use explicit English opening and closing keywords, never indentation.

---

## 2. Variables

### 2.1 Declaration

**Syntax rule:** A variable is declared with the sentence `Let <name> be <value>.` where `<name>` is one or more English words and `<value>` is a literal value.

**Supported types** (inferred automatically):
- **Whole number:** `0`, `1`, `42`, `100` (written as English words or digits — digits are sequences of the characters zero through nine, which are letters in spirit and permitted)
- **Decimal number:** `3.5`, `0.75` (the period here is part of the number when preceded and followed by digits)
- **Boolean:** `true` or `false`
- **Text:** a sequence of words (any remaining words after `be` that are not a number or boolean are treated as text)

**Examples:**
```
Let name be Alice.
Let score be 0.
Let temperature be 98.6.
Let is ready be true.
Let greeting be Hello there friend.
```

### 2.2 Re-assignment

**Syntax rule:** A variable is updated with the sentence `Set <name> to <expression>.`

**Examples:**
```
Set score to 10.
Set score to score plus 5.
Set name to Bob.
Set is ready to false.
```

### 2.3 Arithmetic Expressions

Arithmetic is written using English words:
- `plus` — addition
- `minus` — subtraction
- `times` — multiplication
- `divided by` — division
- `modulo` — remainder

Expressions are evaluated **left to right** (no operator precedence — use intermediate variables for complex math).

**Examples:**
```
Set total to price times quantity.
Set remainder to count modulo 2.
Set average to sum divided by count.
```

---

## 3. Conditions

### 3.1 If, Otherwise if, Otherwise, End if

**Syntax rule:** An if-block begins with `If <condition>, then.` and ends with `End if.` Optional branches use `Otherwise if <condition>, then.` and `Otherwise.`

**Comparison operators (written as phrases):**
- `is equal to`
- `is not equal to`
- `is greater than`
- `is less than`
- `is greater than or equal to`
- `is less than or equal to`

**Boolean checks:**
- `<variable> is true`
- `<variable> is false`

**Compound conditions:**
- `and` — both conditions must hold
- `or` — at least one condition must hold

**Examples:**

```
If score is greater than 50, then.
  Display You passed.
End if.
```

```
If age is less than 13, then.
  Display You are a child.
Otherwise if age is less than 18, then.
  Display You are a teenager.
Otherwise.
  Display You are an adult.
End if.
```

```
If score is greater than 50 and is ready is true, then.
  Display Go ahead.
End if.
```

---

## 4. Loops

### 4.1 Counted Loop

**Syntax rule:** `Repeat <number or variable> times.` ... `End repeat.`

**Examples:**
```
Repeat 5 times.
  Display Hello.
End repeat.
```

```
Let count be 3.
Repeat count times.
  Display Looping.
End repeat.
```

### 4.2 While Loop

**Syntax rule:** `While <condition>, repeat.` ... `End while.`

**Examples:**
```
Let counter be 0.
While counter is less than 10, repeat.
  Display counter.
  Set counter to counter plus 1.
End while.
```

```
Let running be true.
While running is true, repeat.
  Display Still going.
  Set running to false.
End while.
```

### 4.3 For-Each Loop

**Syntax rule:** `For each <item name> in <list name>.` ... `End for each.`

**Examples:**
```
Let colours be a list containing red, green, blue.
For each colour in colours.
  Display colour.
End for each.
```

---

## 5. Input and Output

### 5.1 Display (Output)

**Syntax rule:** `Display <expression or text>.` prints a value or message to the screen followed by a newline.

When the displayed text contains a variable name, the variable's value is interpolated in place.

**Examples:**
```
Display Hello world.
Display score.
Display Your score is score out of 100.
```

### 5.2 Ask (Input)

**Syntax rule:** `Ask <prompt text> and store it in <variable name>.` reads one line of input from the user and saves it into the named variable. If the input looks like a number it is stored as a number.

**Examples:**
```
Ask What is your name and store it in name.
Ask Enter your age and store it in age.
```

---

## 6. Functions

### 6.1 Definition

**Syntax rule:** `Define a function called <name> that takes <param1>, <param2>.` ... `End function.`

A function with no parameters: `Define a function called <name>.` ... `End function.`

### 6.2 Return Value

**Syntax rule:** Inside a function body, `Give back <expression>.` returns a value to the caller.

### 6.3 Calling a Function

**Syntax rule (no return capture):** `Call <name>.` or `Call <name> with <arg1>, <arg2>.`

**Syntax rule (capture return):** `Set <variable> to the result of calling <name> with <arg1>, <arg2>.`

**Examples:**

```
Define a function called greet that takes person.
  Display Hello, person.
End function.

Call greet with Alice.
```

```
Define a function called add that takes a, b.
  Let total be a plus b.
  Give back total.
End function.

Set result to the result of calling add with 3, 5.
Display result.
```

```
Define a function called factorial that takes n.
  If n is less than or equal to 1, then.
    Give back 1.
  End if.
  Set result to the result of calling factorial with n minus 1.
  Set result to result times n.
  Give back result.
End function.
```

---

## 7. Lists

### 7.1 Creating a List

**Syntax rule:** `Let <name> be a list containing <item1>, <item2>, <item3>.`

An empty list: `Let <name> be an empty list.`

### 7.2 Adding to a List

**Syntax rule:** `Add <value> to <list name>.`

### 7.3 Removing from a List

**Syntax rule:** `Remove <value> from <list name>.`

### 7.4 List Length

**Syntax rule:** `Set <variable> to the length of <list name>.`

### 7.5 Accessing by Position

**Syntax rule:** `Set <variable> to item <number> of <list name>.`

**Examples:**

```
Let fruits be a list containing apple, banana, cherry.
Add grape to fruits.
Remove banana from fruits.
Set count to the length of fruits.
Display count.
```

```
Let numbers be an empty list.
Add 1 to numbers.
Add 2 to numbers.
Add 3 to numbers.
For each num in numbers.
  Display num.
End for each.
```

---

## 8. Comments

**Syntax rule:** `Note <any text>.`

Comments are ignored entirely by the interpreter.

**Examples:**
```
Note This program greets the user.
Note The variable below stores the users age.
Let age be 25.
```

---

## 9. Formal Grammar (Prose Rules)

1. A **program** is a sequence of zero or more statements.
2. A **statement** is a sequence of words and commas terminated by a period.
3. A **comment statement** begins with the word `Note` and ends with a period. It is discarded.
4. A **let statement** begins with `Let`, followed by a variable name (one or more words), followed by `be`, followed by a value expression, and ends with a period.
5. A **set statement** begins with `Set`, followed by a variable name, followed by `to`, followed by an expression, and ends with a period.
6. A **display statement** begins with `Display`, followed by an expression or literal text, and ends with a period.
7. An **ask statement** begins with `Ask`, followed by prompt text, followed by `and store it in`, followed by a variable name, and ends with a period.
8. An **if statement** begins with `If`, followed by a condition, followed by a comma, followed by `then`, and ends with a period. It opens a block.
9. An **otherwise if clause** begins with `Otherwise if`, followed by a condition, followed by a comma, followed by `then`, and ends with a period.
10. An **otherwise clause** is the single word `Otherwise` followed by a period.
11. An **end if** is `End if` followed by a period. It closes the if-block.
12. A **repeat statement** begins with `Repeat`, followed by a number or variable name, followed by `times`, and ends with a period. It opens a block.
13. An **end repeat** is `End repeat` followed by a period.
14. A **while statement** begins with `While`, followed by a condition, followed by a comma, followed by `repeat`, and ends with a period. It opens a block.
15. An **end while** is `End while` followed by a period.
16. A **for each statement** begins with `For each`, followed by an item variable name, followed by `in`, followed by a list variable name, and ends with a period. It opens a block.
17. An **end for each** is `End for each` followed by a period.
18. A **function definition** begins with `Define a function called`, followed by a function name, optionally followed by `that takes` and a comma-separated parameter list, and ends with a period. It opens a block.
19. An **end function** is `End function` followed by a period.
20. A **give back statement** begins with `Give back`, followed by an expression, and ends with a period.
21. A **call statement** begins with `Call`, followed by a function name, optionally followed by `with` and a comma-separated argument list, and ends with a period.
22. A **result call expression** is the phrase `the result of calling`, followed by a function name, optionally followed by `with` and arguments. It appears inside a set statement.
23. A **list literal** is a let statement where the value is `a list containing` followed by a comma-separated list of values.
24. An **empty list literal** is a let statement where the value is `an empty list`.
25. An **add statement** begins with `Add`, followed by a value, followed by `to`, followed by a list name, and ends with a period.
26. A **remove statement** begins with `Remove`, followed by a value, followed by `from`, followed by a list name, and ends with a period.
27. A **length expression** is the phrase `the length of` followed by a list variable name.
28. An **item access expression** is the phrase `item` followed by a number or variable, followed by `of`, followed by a list variable name.
29. A **condition** is an expression, followed by a comparison phrase, followed by another expression. Conditions may be chained with `and` or `or`.
30. An **expression** is a variable name, a literal value, or two expressions joined by an arithmetic word (`plus`, `minus`, `times`, `divided by`, `modulo`).
31. A **variable name** is one or more English words that are not reserved keywords.
32. A **number literal** is a sequence of digit characters, optionally containing one period for decimals.
33. A **boolean literal** is the word `true` or `false`.
34. A **string literal** is any sequence of words wrapped in double quotes (e.g. `"Hello world"`).
35. A **use statement** begins with `Use` followed by a library name, and ends with a period.

---

## 10. Libraries

**Syntax rule:** `Use <library name>.` 

Loads native Python functions from `libs/<library name>_lib.py`. These functions are then available to the `Call` and `the result of calling` statements just like user-defined functions.

**Standard Libraries:**
- **math:** `round`, `floor`, `ceiling`, `square root`, `power`, `absolute value`, `minimum`, `maximum`
- **graphics:** Window and drawing APIs (`create window`, `draw rectangle`, `set background`, `set colour`, `draw circle`, `update display`, `wait`, `close window`)
- **input:** Hardware inputs (`check events`, `is key pressed`, `mouse position`, `is mouse pressed`)
- **random:** Generators (`random integer`, `random decimal`, `random choice`)
- **time:** Clock (`current time`, `current date`, `unix timestamp`, `sleep`)
- **text:** String tools (`uppercase`, `lowercase`, `length of text`, `replace text`, `split text`)
- **file:** I/O (`read file`, `write file`, `append file`, `file exists`)
- **system:** Environment (`operating system`, `current directory`, `shell`)
- **dictionary:** Key-Value Maps (`create dictionary`, `put in dictionary`, `get from dictionary`, `remove from dictionary`, `dictionary keys`)
- **network:** Web requests (`fetch url`, `download file`)
- **json:** Data serialization (`parse json`, `to json string`)
- **type:** Dynamic casting (`type of`, `to text`, `to number`)
- **regex:** Pattern matching (`regex match`, `regex search`, `regex replace`, `regex split`)
- **csv:** Table processing (`read csv`, `write csv`)
- **base64:** Data encoding (`base64 encode`, `base64 decode`)
- **crypto:** Hashing routines (`md5 hash`, `sha256 hash`)
- **dialog:** Native UI alerts and prompts (`show info`, `show error`, `ask yes no`, `ask string`)
- **database:** SQLite relational databases (`connect to database`, `execute sql`, `fetch query`, `close database`)

---

## 11. Error Messages

| Situation | Message |
|---|---|
| Unknown statement | I do not understand the sentence on line N. Every statement should start with a keyword like Let, Set, Display, If, Repeat, While, For each, Define, Call, Add, Remove, Ask, or Note. |
| Missing period | It looks like the statement starting on line N is missing a period at the end. Every sentence in PlainEnglish must end with a period. |
| Undefined variable | I do not know what NAME means on line N. Did you forget to create it with a Let statement first? |
| Type mismatch in arithmetic | I cannot do math with the value VALUE on line N because it is not a number. |
| Division by zero | I cannot divide by zero on line N. Please check your math. |
| Wrong number of arguments | The function NAME expects N parameters but you gave it M on line N. Please check your Call statement. |
| Undefined function | I do not know a function called NAME on line N. Did you forget to define it with a Define a function called statement? |
| Unexpected end of file | The program ended before I found END_KEYWORD to close the block that started on line N. |
| List item not found | I could not find VALUE in the list NAME on line N. The item must be in the list before you can remove it. |
| Index out of range | Item number N is out of range for the list NAME on line N. The list only has M items. |
| File not found | I cannot find the file FILENAME. Please check the file name and try again. |
| Empty program | The file FILENAME appears to be empty. Try writing some PlainEnglish statements and run it again. |
