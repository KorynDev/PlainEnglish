# PlainEnglish Quick Reference Cheat Sheet

> **File extension:** `.ple` | **Only symbols allowed:** `,` and `.` | Every statement ends with a **period**.

---

## Variables

| Action | Syntax |
|---|---|
| Create a variable | `Let name be Alice.` |
| Create a number | `Let score be 0.` |
| Create a decimal | `Let pi be 3.14.` |
| Create a boolean | `Let is ready be true.` |
| Update a variable | `Set score to 100.` |
| Arithmetic | `Set total to a plus b.` |

**Arithmetic words:** `plus`, `minus`, `times`, `divided by`, `modulo`

---

## Conditions

```
If score is greater than 50, then.
  Display You passed.
Otherwise if score is equal to 50, then.
  Display Right on the line.
Otherwise.
  Display Keep trying.
End if.
```

**Comparisons:** `is equal to`, `is not equal to`, `is greater than`, `is less than`, `is greater than or equal to`, `is less than or equal to`

**Boolean:** `is ready is true`, `is ready is false`

**Compound:** `score is greater than 50 and is ready is true`

---

## Loops

### Counted Loop
```
Repeat 5 times.
  Display Hello.
End repeat.
```

### While Loop
```
While counter is less than 10, repeat.
  Set counter to counter plus 1.
End while.
```

### For Each Loop
```
For each item in colours.
  Display item.
End for each.
```

---

## Input and Output

| Action | Syntax |
|---|---|
| Print to screen | `Display Hello world.` |
| Print a variable | `Display score.` |
| Read user input | `Ask What is your name and store it in name.` |

---

## Functions

### Define
```
Define a function called greet that takes person.
  Display Hello, person.
End function.
```

### Call (no return value)
```
Call greet with Alice.
```

### Call (capture return value)
```
Define a function called double that takes x.
  Let result be x times 2.
  Give back result.
End function.

Set answer to the result of calling double with 5.
```

---

## Lists

| Action | Syntax |
|---|---|
| Create a list | `Let fruits be a list containing apple, banana, cherry.` |
| Empty list | `Let items be an empty list.` |
| Add an item | `Add grape to fruits.` |
| Remove an item | `Remove banana from fruits.` |
| Get length | `Set count to the length of fruits.` |
| Access by position | `Set first to item 1 of fruits.` |
| Loop through | `For each fruit in fruits.` ... `End for each.` |

---

## Libraries

Import standard features into your program with `Use`. (Make sure the matching `<name>_lib.py` exists in the `libs/` folder).

| Library | Features |
|---|---|
| **math** | `round`, `floor`, `ceiling`, `square root`, `power`, `absolute value`, `minimum`, `maximum` |
| **graphics** | `create window`, `set background`, `draw rectangle`, `draw circle`, `update display`, `wait`, `close window` |
| **input** | `check events`, `is key pressed`, `mouse position`, `is mouse pressed` |

```
Use math.
Set answer to the result of calling square root with 64.
```

---

## Comments

```
Note This line is ignored by the interpreter.
```

---

## Running a Program

```
python plainenglish.py yourfile.ple
```
