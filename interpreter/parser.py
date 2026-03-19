"""
Parser for PlainEnglish.

Takes the list of (line, sentence) pairs from the lexer and produces
an AST (see ast_nodes.py).

The parser is pattern-based: it checks each sentence against known
syntactic patterns and dispatches to the appropriate builder.
"""

from __future__ import annotations
from typing import List, Tuple, Any, Optional
from . import ast_nodes as ast
from .errors import unknown_statement, unexpected_eof, ParseError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _words(sentence: str) -> List[str]:
    """Split a sentence into tokens (words and commas kept separate)."""
    tokens: list[str] = []
    buf: list[str] = []
    for ch in sentence:
        if ch == ',':
            if buf:
                tokens.append(''.join(buf).strip())
                buf = []
            tokens.append(',')
        elif ch == ' ':
            if buf:
                word = ''.join(buf).strip()
                if word:
                    tokens.append(word)
                buf = []
        else:
            buf.append(ch)
    if buf:
        word = ''.join(buf).strip()
        if word:
            tokens.append(word)
    return tokens


def _lower_tokens(tokens: List[str]) -> List[str]:
    return [t.lower() if t != ',' else t for t in tokens]


def _is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def _parse_number(text: str) -> int | float:
    f = float(text)
    if f == int(f) and '.' not in text:
        return int(f)
    return f


def _find_sequence(ltokens: List[str], seq: List[str], start: int = 0) -> int:
    """Find the starting index of a contiguous sub-sequence in ltokens."""
    seq_len = len(seq)
    for i in range(start, len(ltokens) - seq_len + 1):
        if ltokens[i:i + seq_len] == seq:
            return i
    return -1


def _split_on_commas(tokens: List[str]) -> List[List[str]]:
    """Split a token list on commas, returning groups."""
    groups: list[list[str]] = []
    current: list[str] = []
    for t in tokens:
        if t == ',':
            if current:
                groups.append(current)
            current = []
        else:
            current.append(t)
    if current:
        groups.append(current)
    return groups


# ---------------------------------------------------------------------------
# Expression parser
# ---------------------------------------------------------------------------

_ARITHMETIC_OPS = ['plus', 'minus', 'times', 'modulo']
_ARITHMETIC_TWO_WORD = [['divided', 'by']]


def _parse_expression(tokens: List[str], line: int) -> Any:
    """Parse an expression from a list of word tokens.

    Handles: number literals, boolean literals, variable references,
    arithmetic (left-to-right), length of, item N of, result of calling.
    """
    if not tokens:
        return ast.TextLiteral(line=line, value="")

    ltokens = _lower_tokens(tokens)

    # --- the result of calling <func> with <args> ---
    idx = _find_sequence(ltokens, ['the', 'result', 'of', 'calling'])
    if idx != -1:
        rest = tokens[idx + 4:]
        lrest = ltokens[idx + 4:]
        widx = -1
        for j, t in enumerate(lrest):
            if t == 'with':
                widx = j
                break
        if widx != -1:
            fname = ' '.join(rest[:widx])
            arg_tokens = rest[widx + 1:]
            groups = _split_on_commas(arg_tokens)
            args = [_parse_expression(g, line) for g in groups]
        else:
            fname = ' '.join(rest)
            args = []
        return ast.ResultCall(line=line, func_name=fname, args=args)

    # --- the length of <list> ---
    idx = _find_sequence(ltokens, ['the', 'length', 'of'])
    if idx != -1:
        list_name = ' '.join(tokens[idx + 3:])
        return ast.LengthOf(line=line, list_name=list_name)

    # --- item <n> of <list> ---
    if ltokens[0] == 'item' and len(tokens) >= 4:
        of_idx = -1
        for j in range(2, len(ltokens)):
            if ltokens[j] == 'of':
                of_idx = j
                break
        if of_idx != -1:
            index_expr = _parse_expression(tokens[1:of_idx], line)
            list_name = ' '.join(tokens[of_idx + 1:])
            return ast.ItemAccess(line=line, index=index_expr, list_name=list_name)

    # --- arithmetic: scan left-to-right for operators ---
    # two-word operators first
    for op_words in _ARITHMETIC_TWO_WORD:
        idx = _find_sequence(ltokens, op_words)
        if idx is not None and idx > 0:
            left = _parse_expression(tokens[:idx], line)
            right = _parse_expression(tokens[idx + len(op_words):], line)
            return ast.BinaryOp(line=line, left=left, op=' '.join(op_words), right=right)

    # single-word operators
    for op in _ARITHMETIC_OPS:
        for j, t in enumerate(ltokens):
            if t == op and j > 0:
                left = _parse_expression(tokens[:j], line)
                right = _parse_expression(tokens[j + 1:], line)
                return ast.BinaryOp(line=line, left=left, op=op, right=right)

    # --- single token ---
    if len(tokens) == 1:
        tok = tokens[0]
        ltok = ltokens[0]
        if _is_number(tok):
            return ast.NumberLiteral(line=line, value=_parse_number(tok))
        if ltok == 'true':
            return ast.BooleanLiteral(line=line, value=True)
        if ltok == 'false':
            return ast.BooleanLiteral(line=line, value=False)
        return ast.VariableRef(line=line, name=tok)

    # --- multi-word: could be a variable name or text literal ---
    # We treat it as a variable reference first; the interpreter will
    # fall back to text if the variable name doesn't resolve.
    return ast.VariableRef(line=line, name=' '.join(tokens))


# ---------------------------------------------------------------------------
# Condition parser
# ---------------------------------------------------------------------------

_COMPARISONS = [
    (['is', 'not', 'equal', 'to'], 'is not equal to'),
    (['is', 'greater', 'than', 'or', 'equal', 'to'], 'is greater than or equal to'),
    (['is', 'less', 'than', 'or', 'equal', 'to'], 'is less than or equal to'),
    (['is', 'greater', 'than'], 'is greater than'),
    (['is', 'less', 'than'], 'is less than'),
    (['is', 'equal', 'to'], 'is equal to'),
]


def _parse_condition(tokens: List[str], line: int) -> Any:
    """Parse a condition which may be compound (and / or)."""
    ltokens = _lower_tokens(tokens)

    # --- compound: and / or ---
    # scan for top-level 'and' or 'or' (not inside a comparison phrase)
    for logic_word in ['and', 'or']:
        # Find logic_word outside comparison phrases
        depth = 0
        for j, t in enumerate(ltokens):
            if t == logic_word and j > 0 and j < len(ltokens) - 1:
                # Make sure 'or' is not part of 'greater than or equal to' / 'less than or equal to'
                if logic_word == 'or':
                    # check if surrounded by comparison phrase
                    before_match = False
                    if j >= 3 and ltokens[j-3:j] == ['greater', 'than', 'or'] or \
                       j >= 3 and ltokens[j-2:j] == ['than', 'or']:
                        before_match = True
                    if j >= 2 and ltokens[j-1:j+1] == ['or', 'equal']:
                        before_match = True
                    # Check if 'or' is part of 'than or equal'
                    if j >= 1 and j + 2 < len(ltokens) and ltokens[j-1] == 'than' and ltokens[j+1] == 'equal':
                        continue
                    if before_match:
                        continue
                left_cond = _parse_condition(tokens[:j], line)
                right_cond = _parse_condition(tokens[j + 1:], line)
                return ast.CompoundCondition(line=line, left=left_cond, logic=logic_word, right=right_cond)

    # --- boolean check: <var> is true / is false ---
    if len(ltokens) >= 2 and ltokens[-1] in ('true', 'false') and ltokens[-2] == 'is':
        var_tokens = tokens[:-2]
        var_name = ' '.join(var_tokens)
        expected = ltokens[-1] == 'true'
        return ast.BooleanCheck(line=line, name=var_name, expected=expected)

    # --- comparison operators ---
    for comp_words, comp_name in _COMPARISONS:
        idx = _find_sequence(ltokens, comp_words)
        if idx is not None and idx > 0:
            left = _parse_expression(tokens[:idx], line)
            right = _parse_expression(tokens[idx + len(comp_words):], line)
            return ast.Comparison(line=line, left=left, op=comp_name, right=right)

    # Fallback: treat as a boolean expression
    return _parse_expression(tokens, line)


# ---------------------------------------------------------------------------
# Statement parsers
# ---------------------------------------------------------------------------

def _parse_let(tokens: List[str], ltokens: List[str], line: int) -> ast.Statement:
    """Parse: Let <name> be <value>."""
    # Find 'be'
    be_idx = -1
    for j in range(1, len(ltokens)):
        if ltokens[j] == 'be':
            be_idx = j
            break
    if be_idx == -1:
        raise ParseError(
            'A Let statement needs the word "be" to set the value. '
            'For example: Let score be 0.',
            line,
        )

    name = ' '.join(tokens[1:be_idx])
    value_tokens = tokens[be_idx + 1:]
    lvalue = _lower_tokens(value_tokens)

    # --- a list containing ... ---
    if len(lvalue) >= 3 and lvalue[0] == 'a' and lvalue[1] == 'list' and lvalue[2] == 'containing':
        item_tokens = value_tokens[3:]
        groups = _split_on_commas(item_tokens)
        items = [_parse_expression(g, line) for g in groups]
        return ast.LetStatement(line=line, name=name, value=ast.ListLiteral(line=line, items=items))

    # --- an empty list ---
    if len(lvalue) >= 3 and lvalue[0] == 'an' and lvalue[1] == 'empty' and lvalue[2] == 'list':
        return ast.LetStatement(line=line, name=name, value=ast.EmptyListLiteral(line=line))

    value = _parse_expression(value_tokens, line)
    return ast.LetStatement(line=line, name=name, value=value)


def _parse_set(tokens: List[str], ltokens: List[str], line: int) -> ast.Statement:
    """Parse: Set <name> to <expression>."""
    to_idx = -1
    for j in range(1, len(ltokens)):
        if ltokens[j] == 'to':
            to_idx = j
            break
    if to_idx == -1:
        raise ParseError(
            'A Set statement needs the word "to" to assign a value. '
            'For example: Set score to 10.',
            line,
        )

    name = ' '.join(tokens[1:to_idx])
    value_tokens = tokens[to_idx + 1:]
    value = _parse_expression(value_tokens, line)
    return ast.SetStatement(line=line, name=name, value=value)


def _parse_display(tokens: List[str], line: int) -> ast.DisplayStatement:
    """Parse: Display <stuff>."""
    parts_raw = tokens[1:]  # everything after 'Display'
    # We split on commas to keep comma-separated text natural.
    # Each token is either a variable ref or text.
    parts: list[Any] = []
    for t in parts_raw:
        if t == ',':
            parts.append(ast.TextLiteral(line=line, value=","))
        elif _is_number(t):
            parts.append(ast.NumberLiteral(line=line, value=_parse_number(t)))
        else:
            # Might be a variable; interpreter will resolve or treat as text.
            parts.append(ast.VariableRef(line=line, name=t))
    return ast.DisplayStatement(line=line, parts=parts)


def _parse_ask(tokens: List[str], ltokens: List[str], line: int) -> ast.AskStatement:
    """Parse: Ask <prompt> and store it in <variable>."""
    idx = _find_sequence(ltokens, ['and', 'store', 'it', 'in'])
    if idx == -1:
        raise ParseError(
            'An Ask statement needs "and store it in" followed by a variable name. '
            'For example: Ask What is your name and store it in name.',
            line,
        )
    prompt_tokens = tokens[1:idx]
    var_name = ' '.join(tokens[idx + 4:])
    prompt_parts = [ast.VariableRef(line=line, name=t) if not _is_number(t) and t != ',' else
                    ast.TextLiteral(line=line, value=t) for t in prompt_tokens]
    return ast.AskStatement(line=line, prompt_parts=prompt_parts, variable_name=var_name)


def _parse_function_def_header(tokens: List[str], ltokens: List[str], line: int):
    """Parse the header of: Define a function called <name> that takes <params>."""
    # Find 'called'
    called_idx = _find_sequence(ltokens, ['called'])
    if called_idx == -1:
        raise ParseError(
            'A function definition needs "Define a function called" followed by a name. '
            'For example: Define a function called greet that takes person.',
            line,
        )
    # Find 'that takes'
    takes_idx = _find_sequence(ltokens, ['that', 'takes'], called_idx)
    if takes_idx != -1:
        fname = ' '.join(tokens[called_idx + 1:takes_idx])
        param_tokens = tokens[takes_idx + 2:]
        groups = _split_on_commas(param_tokens)
        params = [' '.join(g) for g in groups]
    else:
        fname = ' '.join(tokens[called_idx + 1:])
        params = []
    return fname, params


def _parse_call(tokens: List[str], ltokens: List[str], line: int) -> ast.FunctionCall:
    """Parse: Call <name> with <args>."""
    with_idx = -1
    for j in range(1, len(ltokens)):
        if ltokens[j] == 'with':
            with_idx = j
            break
    if with_idx != -1:
        fname = ' '.join(tokens[1:with_idx])
        arg_tokens = tokens[with_idx + 1:]
        groups = _split_on_commas(arg_tokens)
        args = [_parse_expression(g, line) for g in groups]
    else:
        fname = ' '.join(tokens[1:])
        args = []
    return ast.FunctionCall(line=line, name=fname, args=args)


def _parse_add(tokens: List[str], ltokens: List[str], line: int) -> ast.AddToList:
    """Parse: Add <value> to <list>."""
    to_idx = -1
    for j in range(len(ltokens) - 1, 0, -1):
        if ltokens[j] == 'to':
            to_idx = j
            break
    if to_idx == -1:
        raise ParseError(
            'An Add statement needs "to" followed by the list name. '
            'For example: Add 5 to numbers.',
            line,
        )
    value_tokens = tokens[1:to_idx]
    list_name = ' '.join(tokens[to_idx + 1:])
    value = _parse_expression(value_tokens, line)
    return ast.AddToList(line=line, value=value, list_name=list_name)


def _parse_remove(tokens: List[str], ltokens: List[str], line: int) -> ast.RemoveFromList:
    """Parse: Remove <value> from <list>."""
    from_idx = -1
    for j in range(len(ltokens) - 1, 0, -1):
        if ltokens[j] == 'from':
            from_idx = j
            break
    if from_idx == -1:
        raise ParseError(
            'A Remove statement needs "from" followed by the list name. '
            'For example: Remove banana from fruits.',
            line,
        )
    value_tokens = tokens[1:from_idx]
    list_name = ' '.join(tokens[from_idx + 1:])
    value = _parse_expression(value_tokens, line)
    return ast.RemoveFromList(line=line, value=value, list_name=list_name)


# ---------------------------------------------------------------------------
# Block parser (recursive)
# ---------------------------------------------------------------------------

_BLOCK_ENDERS = {
    'if': 'end if',
    'repeat': 'end repeat',
    'while': 'end while',
    'for each': 'end for each',
    'function': 'end function',
}


def parse(sentences: List[Tuple[int, str]]) -> ast.Program:
    """Parse a list of (line, sentence) pairs into an AST Program."""
    program = ast.Program()
    idx = 0
    while idx < len(sentences):
        stmt, idx = _parse_statement(sentences, idx)
        if stmt is not None:
            program.statements.append(stmt)
    return program


def _parse_statement(sentences: List[Tuple[int, str]], idx: int) -> Tuple[Optional[ast.Statement], int]:
    """Parse one statement (possibly a block) starting at sentences[idx].

    Returns (statement, next_idx).
    """
    if idx >= len(sentences):
        return None, idx

    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    if not tokens:
        return None, idx + 1

    first = ltokens[0]

    # --- Let ---
    if first == 'let':
        return _parse_let(tokens, ltokens, line), idx + 1

    # --- Set ---
    if first == 'set':
        return _parse_set(tokens, ltokens, line), idx + 1

    # --- Display ---
    if first == 'display':
        return _parse_display(tokens, line), idx + 1

    # --- Ask ---
    if first == 'ask':
        return _parse_ask(tokens, ltokens, line), idx + 1

    # --- Give back ---
    if first == 'give' and len(ltokens) > 1 and ltokens[1] == 'back':
        value = _parse_expression(tokens[2:], line)
        return ast.GiveBackStatement(line=line, value=value), idx + 1

    # --- Call ---
    if first == 'call':
        return _parse_call(tokens, ltokens, line), idx + 1

    # --- Add ---
    if first == 'add':
        return _parse_add(tokens, ltokens, line), idx + 1

    # --- Remove ---
    if first == 'remove':
        return _parse_remove(tokens, ltokens, line), idx + 1

    # --- If block ---
    if first == 'if':
        return _parse_if_block(sentences, idx)

    # --- Repeat ---
    if first == 'repeat':
        return _parse_repeat_block(sentences, idx)

    # --- While ---
    if first == 'while':
        return _parse_while_block(sentences, idx)

    # --- For each ---
    if first == 'for' and len(ltokens) > 1 and ltokens[1] == 'each':
        return _parse_for_each_block(sentences, idx)

    # --- Define a function ---
    if first == 'define':
        return _parse_function_block(sentences, idx)

    raise unknown_statement(line)


# ---------------------------------------------------------------------------
# Block constructs
# ---------------------------------------------------------------------------

def _collect_body(sentences, start_idx: int, end_markers: List[List[str]], start_line: int, block_type: str):
    """Collect body statements until one of the end_markers is matched.

    Returns (body, matched_marker, next_idx).
    """
    body: list[ast.Statement] = []
    idx = start_idx
    while idx < len(sentences):
        line, sentence = sentences[idx]
        tokens = _words(sentence)
        ltokens = _lower_tokens(tokens)
        for marker in end_markers:
            if ltokens == marker:
                return body, marker, idx + 1
        stmt, idx = _parse_statement(sentences, idx)
        if stmt is not None:
            body.append(stmt)
    # Missing end marker
    end_keyword = ' '.join(end_markers[0]).capitalize()
    raise unexpected_eof(block_type, end_keyword, start_line)


def _parse_if_block(sentences, idx):
    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    # Strip trailing 'then' and any comma before it
    cond_tokens = tokens[1:]  # skip 'If'
    cond_ltokens = ltokens[1:]
    if cond_ltokens and cond_ltokens[-1] == 'then':
        cond_tokens = cond_tokens[:-1]
        cond_ltokens = cond_ltokens[:-1]
    # strip trailing comma
    if cond_tokens and cond_tokens[-1] == ',':
        cond_tokens = cond_tokens[:-1]

    condition = _parse_condition(cond_tokens, line)

    # Collect body until we hit Otherwise if, Otherwise, or End if
    end_markers = [
        ['otherwise', 'if'],  # prefix match — we need special handling
        ['otherwise'],
        ['end', 'if'],
    ]

    if_block = ast.IfBlock(line=line, condition=condition, body=[], elseif_clauses=[], else_body=[])
    body_idx = idx + 1
    current_body: list[ast.Statement] = []

    # Walk through collecting if / elseif / else bodies
    phase = 'if'  # 'if', 'elseif', 'else'
    bidx = body_idx
    while bidx < len(sentences):
        bline, bsentence = sentences[bidx]
        btokens = _words(bsentence)
        bltokens = _lower_tokens(btokens)

        if bltokens == ['end', 'if']:
            if phase == 'if':
                if_block.body = current_body
            elif phase == 'elseif':
                if_block.elseif_clauses[-1].body = current_body
            elif phase == 'else':
                if_block.else_body = current_body
            return if_block, bidx + 1

        if bltokens[0] == 'otherwise' and len(bltokens) > 1 and bltokens[1] == 'if':
            # otherwise if
            if phase == 'if':
                if_block.body = current_body
            elif phase == 'elseif':
                if_block.elseif_clauses[-1].body = current_body

            # parse condition
            cond_t = btokens[2:]  # skip 'Otherwise' 'if'
            cond_lt = bltokens[2:]
            if cond_lt and cond_lt[-1] == 'then':
                cond_t = cond_t[:-1]
                cond_lt = cond_lt[:-1]
            if cond_t and cond_t[-1] == ',':
                cond_t = cond_t[:-1]
            cond = _parse_condition(cond_t, bline)
            if_block.elseif_clauses.append(ast.ElseIfClause(line=bline, condition=cond, body=[]))
            phase = 'elseif'
            current_body = []
            bidx += 1
            continue

        if bltokens == ['otherwise']:
            if phase == 'if':
                if_block.body = current_body
            elif phase == 'elseif':
                if_block.elseif_clauses[-1].body = current_body
            phase = 'else'
            current_body = []
            bidx += 1
            continue

        stmt, bidx = _parse_statement(sentences, bidx)
        if stmt is not None:
            current_body.append(stmt)

    raise unexpected_eof('If', 'End if', line)


def _parse_repeat_block(sentences, idx):
    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    # Repeat <count> times
    # Strip 'times' at end
    count_tokens = tokens[1:]
    if _lower_tokens(count_tokens) and _lower_tokens(count_tokens)[-1] == 'times':
        count_tokens = count_tokens[:-1]
    count_expr = _parse_expression(count_tokens, line)

    body, _, next_idx = _collect_body(sentences, idx + 1, [['end', 'repeat']], line, 'Repeat')
    return ast.RepeatLoop(line=line, count=count_expr, body=body), next_idx


def _parse_while_block(sentences, idx):
    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    # While <condition>, repeat
    cond_tokens = tokens[1:]
    cond_ltokens = _lower_tokens(cond_tokens)
    # strip trailing 'repeat' and comma
    if cond_ltokens and cond_ltokens[-1] == 'repeat':
        cond_tokens = cond_tokens[:-1]
        cond_ltokens = cond_ltokens[:-1]
    if cond_tokens and cond_tokens[-1] == ',':
        cond_tokens = cond_tokens[:-1]

    condition = _parse_condition(cond_tokens, line)
    body, _, next_idx = _collect_body(sentences, idx + 1, [['end', 'while']], line, 'While')
    return ast.WhileLoop(line=line, condition=condition, body=body), next_idx


def _parse_for_each_block(sentences, idx):
    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    # For each <item> in <list>
    # Skip 'For' 'each', then find 'in'
    rest = tokens[2:]
    lrest = _lower_tokens(rest)
    in_idx = -1
    for j, t in enumerate(lrest):
        if t == 'in':
            in_idx = j
            break
    if in_idx == -1:
        raise ParseError(
            'A For each loop needs "in" followed by a list name. '
            'For example: For each item in colours.',
            line,
        )
    item_name = ' '.join(rest[:in_idx])
    list_name = ' '.join(rest[in_idx + 1:])

    body, _, next_idx = _collect_body(sentences, idx + 1, [['end', 'for', 'each']], line, 'For each')
    return ast.ForEachLoop(line=line, item_name=item_name, list_name=list_name, body=body), next_idx


def _parse_function_block(sentences, idx):
    line, sentence = sentences[idx]
    tokens = _words(sentence)
    ltokens = _lower_tokens(tokens)

    fname, params = _parse_function_def_header(tokens, ltokens, line)
    body, _, next_idx = _collect_body(sentences, idx + 1, [['end', 'function']], line, 'Define')
    return ast.FunctionDef(line=line, name=fname, params=params, body=body), next_idx
