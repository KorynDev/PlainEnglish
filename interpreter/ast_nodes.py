"""
AST node definitions for PlainEnglish.

Every construct in the language maps to one of these dataclasses.
The tree-walking interpreter visits them to execute the program.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any


# ---------------------------------------------------------------------------
# Program root
# ---------------------------------------------------------------------------

@dataclass
class Program:
    statements: List[Statement] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

@dataclass
class Statement:
    line: int = 0


# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------

@dataclass
class LetStatement(Statement):
    name: str = ""
    value: Any = None  # Expression or literal


@dataclass
class SetStatement(Statement):
    name: str = ""
    value: Any = None


# ---------------------------------------------------------------------------
# Expressions
# ---------------------------------------------------------------------------

@dataclass
class NumberLiteral(Statement):
    value: float = 0


@dataclass
class TextLiteral(Statement):
    value: str = ""


@dataclass
class BooleanLiteral(Statement):
    value: bool = False


@dataclass
class VariableRef(Statement):
    name: str = ""


@dataclass
class BinaryOp(Statement):
    left: Any = None
    op: str = ""        # plus, minus, times, divided by, modulo
    right: Any = None


@dataclass
class ListLiteral(Statement):
    items: List[Any] = field(default_factory=list)


@dataclass
class EmptyListLiteral(Statement):
    pass


@dataclass
class LengthOf(Statement):
    list_name: str = ""


@dataclass
class ItemAccess(Statement):
    index: Any = None   # expression for the index
    list_name: str = ""


@dataclass
class ResultCall(Statement):
    func_name: str = ""
    args: List[Any] = field(default_factory=list)


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

@dataclass
class DisplayStatement(Statement):
    parts: List[Any] = field(default_factory=list)


@dataclass
class AskStatement(Statement):
    prompt_parts: List[Any] = field(default_factory=list)
    variable_name: str = ""


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

@dataclass
class Comparison(Statement):
    left: Any = None
    op: str = ""        # is equal to, is not equal to, is greater than, etc.
    right: Any = None


@dataclass
class BooleanCheck(Statement):
    name: str = ""
    expected: bool = True


@dataclass
class CompoundCondition(Statement):
    left: Any = None
    logic: str = ""     # and, or
    right: Any = None


@dataclass
class IfBlock(Statement):
    condition: Any = None
    body: List[Statement] = field(default_factory=list)
    elseif_clauses: List[ElseIfClause] = field(default_factory=list)
    else_body: List[Statement] = field(default_factory=list)


@dataclass
class ElseIfClause(Statement):
    condition: Any = None
    body: List[Statement] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Loops
# ---------------------------------------------------------------------------

@dataclass
class RepeatLoop(Statement):
    count: Any = None  # expression
    body: List[Statement] = field(default_factory=list)


@dataclass
class WhileLoop(Statement):
    condition: Any = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class ForEachLoop(Statement):
    item_name: str = ""
    list_name: str = ""
    body: List[Statement] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

@dataclass
class FunctionDef(Statement):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class FunctionCall(Statement):
    name: str = ""
    args: List[Any] = field(default_factory=list)


@dataclass
class GiveBackStatement(Statement):
    value: Any = None


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------

@dataclass
class AddToList(Statement):
    value: Any = None
    list_name: str = ""


@dataclass
class RemoveFromList(Statement):
    value: Any = None
    list_name: str = ""


# ---------------------------------------------------------------------------
# Comments (parsed then discarded — included for completeness)
# ---------------------------------------------------------------------------

@dataclass
class Comment(Statement):
    text: str = ""
