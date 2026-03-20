"""
Tree-walking interpreter / evaluator for PlainEnglish.

Walks the AST produced by the parser and executes each node.
"""

from __future__ import annotations
import os
import importlib.util
from typing import Any, Dict, List, Optional, Set
from . import ast_nodes as ast
from . import errors


# ---------------------------------------------------------------------------
# Sentinel for "no return value"
# ---------------------------------------------------------------------------

_NO_RETURN = object()


class _ReturnSignal(Exception):
    """Used internally to unwind the call stack when Give back is executed."""

    def __init__(self, value: Any):
        self.value = value


# ---------------------------------------------------------------------------
# Environment (scope)
# ---------------------------------------------------------------------------

class Environment:
    def __init__(self, parent: Optional[Environment] = None):
        self.vars: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        key = name.lower()
        if key in self.vars:
            return self.vars[key]
        if self.parent is not None:
            return self.parent.get(name)
        return _NO_RETURN  # not found

    def set(self, name: str, value: Any):
        key = name.lower()
        # If exists in current scope, update it
        if key in self.vars:
            self.vars[key] = value
            return
        # If exists in parent scope, update there
        if self.parent is not None and self.parent.get(name) is not _NO_RETURN:
            self.parent.set(name, value)
            return
        # Otherwise set in current scope
        self.vars[key] = value


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.functions: Dict[str, ast.FunctionDef] = {}
        self.native_functions: Dict[str, Any] = {}
        self._loaded_libs: Set[str] = set()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self, program: ast.Program):
        # First pass: register all function definitions
        for stmt in program.statements:
            if isinstance(stmt, ast.FunctionDef):
                self.functions[stmt.name.lower()] = stmt

        # Second pass: execute top-level statements
        for stmt in program.statements:
            if isinstance(stmt, ast.FunctionDef):
                continue  # already registered
            self._exec(stmt, self.global_env)

    # ------------------------------------------------------------------
    # Statement execution
    # ------------------------------------------------------------------

    def _exec(self, stmt: ast.Statement, env: Environment) -> None:
        if isinstance(stmt, ast.UseStatement):
            self._exec_use(stmt)
        elif isinstance(stmt, ast.LetStatement):
            self._exec_let(stmt, env)
        elif isinstance(stmt, ast.SetStatement):
            self._exec_set(stmt, env)
        elif isinstance(stmt, ast.DisplayStatement):
            self._exec_display(stmt, env)
        elif isinstance(stmt, ast.AskStatement):
            self._exec_ask(stmt, env)
        elif isinstance(stmt, ast.IfBlock):
            self._exec_if(stmt, env)
        elif isinstance(stmt, ast.RepeatLoop):
            self._exec_repeat(stmt, env)
        elif isinstance(stmt, ast.WhileLoop):
            self._exec_while(stmt, env)
        elif isinstance(stmt, ast.ForEachLoop):
            self._exec_for_each(stmt, env)
        elif isinstance(stmt, ast.FunctionCall):
            self._exec_call(stmt, env)
        elif isinstance(stmt, ast.GiveBackStatement):
            value = self._eval(stmt.value, env, stmt.line)
            raise _ReturnSignal(value)
        elif isinstance(stmt, ast.AddToList):
            self._exec_add_to_list(stmt, env)
        elif isinstance(stmt, ast.RemoveFromList):
            self._exec_remove_from_list(stmt, env)
        elif isinstance(stmt, ast.Comment):
            pass
        else:
            raise errors.unknown_statement(stmt.line)

    # --- Use ---
    def _exec_use(self, stmt: ast.UseStatement) -> None:
        name = stmt.library_name.lower().replace(' ', '_')
        if name in self._loaded_libs:
            return

        # Find libs/ relative to this file's parent directory (PlainEnglish root)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        libs_dir = os.path.join(project_root, 'libs')
        module_path = os.path.join(libs_dir, f'{name}_lib.py')

        if not os.path.exists(module_path):
            raise errors.library_not_found(stmt.library_name, stmt.line)

        # Dynamically load the module
        try:
            spec = importlib.util.spec_from_file_location(f"plainenglish.libs.{name}", module_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot create module spec for {module_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Register functions
            if hasattr(module, 'register'):
                module.register(self)
            else:
                raise AttributeError(f"The library '{stmt.library_name}' does not have a register(interpreter) function.")

        except Exception as e:
            raise errors.library_load_error(stmt.library_name, str(e), stmt.line)

        self._loaded_libs.add(name)

    # --- Let ---
    def _exec_let(self, stmt: ast.LetStatement, env: Environment):
        value = self._eval(stmt.value, env, stmt.line)
        env.set(stmt.name, value)

    # --- Set ---
    def _exec_set(self, stmt: ast.SetStatement, env: Environment) -> None:
        value = self._eval(stmt.value, env, stmt.line)
        env.set(stmt.name, value)

    # --- Display ---
    def _exec_display(self, stmt: ast.DisplayStatement, env: Environment) -> None:
        pieces: list[str] = []
        for part in stmt.parts:
            val = self._eval(part, env, stmt.line)
            pieces.append(self._format_value(val))
        output = ' '.join(pieces)
        # Clean up double spaces and spaces before commas/punctuation
        output = output.replace(' ,', ',')
        print(output)

    def _format_value(self, val: Any) -> str:
        """Format a value for display output."""
        if isinstance(val, bool):
            return 'true' if val else 'false'
        if isinstance(val, float):
            if val == int(val):
                return str(int(val))
            return str(val)
        if isinstance(val, list):
            return ', '.join(self._format_value(item) for item in val)
        return str(val)

    # --- Ask ---
    def _exec_ask(self, stmt: ast.AskStatement, env: Environment) -> None:
        prompt_pieces: list[str] = []
        for part in stmt.prompt_parts:
            val = self._eval(part, env, stmt.line)
            prompt_pieces.append(str(val))
        prompt = ' '.join(prompt_pieces)
        prompt = prompt.replace(' ,', ',')
        user_input = input(prompt + ' ')
        # Try to convert to number
        try:
            if '.' in user_input:
                user_input = float(user_input)
            else:
                user_input = int(user_input)
        except ValueError:
            pass  # keep as string
        env.set(stmt.variable_name, user_input)

    # --- If ---
    def _exec_if(self, stmt: ast.IfBlock, env: Environment) -> None:
        if self._eval_condition(stmt.condition, env, stmt.line):
            for s in stmt.body:
                self._exec(s, env)
            return

        for clause in stmt.elseif_clauses:
            if self._eval_condition(clause.condition, env, clause.line):
                for s in clause.body:
                    self._exec(s, env)
                return

        for s in stmt.else_body:
            self._exec(s, env)

    # --- Repeat ---
    def _exec_repeat(self, stmt: ast.RepeatLoop, env: Environment) -> None:
        count = self._eval(stmt.count, env, stmt.line)
        if not isinstance(count, (int, float)):
            raise errors.type_mismatch_arithmetic(count, stmt.line)
        for _ in range(int(count)):
            for s in stmt.body:
                self._exec(s, env)

    # --- While ---
    def _exec_while(self, stmt: ast.WhileLoop, env: Environment) -> None:
        iteration_limit = 1_000_000
        i = 0
        while self._eval_condition(stmt.condition, env, stmt.line):
            for s in stmt.body:
                self._exec(s, env)
            i += 1
            if i > iteration_limit:
                raise errors.RuntimeError_(
                    "This While loop has run more than a million times. "
                    "It might be stuck in an infinite loop. "
                    "Please check the condition.",
                    stmt.line,
                )

    # --- For each ---
    def _exec_for_each(self, stmt: ast.ForEachLoop, env: Environment) -> None:
        lst = env.get(stmt.list_name)
        if lst is _NO_RETURN:
            raise errors.undefined_variable(stmt.list_name, stmt.line)
        if not isinstance(lst, list):
            raise errors.RuntimeError_(
                f'"{stmt.list_name}" is not a list, so I cannot use For each on it.',
                stmt.line,
            )
        for item in lst:
            env.set(stmt.item_name, item)
            for s in stmt.body:
                self._exec(s, env)

    # --- Call ---
    def _exec_call(self, stmt: ast.FunctionCall, env: Environment) -> Any:
        return self._call_function(stmt.name, stmt.args, env, stmt.line)

    # --- Add to list ---
    def _exec_add_to_list(self, stmt: ast.AddToList, env: Environment) -> None:
        lst = env.get(stmt.list_name)
        if lst is _NO_RETURN:
            raise errors.undefined_variable(stmt.list_name, stmt.line)
        if not isinstance(lst, list):
            raise errors.RuntimeError_(
                f'"{stmt.list_name}" is not a list, so I cannot add to it.',
                stmt.line,
            )
        value = self._eval(stmt.value, env, stmt.line)
        lst.append(value)

    # --- Remove from list ---
    def _exec_remove_from_list(self, stmt: ast.RemoveFromList, env: Environment) -> None:
        lst = env.get(stmt.list_name)
        if lst is _NO_RETURN:
            raise errors.undefined_variable(stmt.list_name, stmt.line)
        if not isinstance(lst, list):
            raise errors.RuntimeError_(
                f'"{stmt.list_name}" is not a list, so I cannot remove from it.',
                stmt.line,
            )
        value = self._eval(stmt.value, env, stmt.line)
        if value not in lst:
            raise errors.list_item_not_found(value, stmt.list_name, stmt.line)
        lst.remove(value)

    # ------------------------------------------------------------------
    # Expression evaluation
    # ------------------------------------------------------------------

    def _eval(self, node: Any, env: Environment, line: int) -> Any:
        if node is None:
            return ""

        if isinstance(node, ast.NumberLiteral):
            return node.value

        if isinstance(node, ast.TextLiteral):
            return node.value

        if isinstance(node, ast.BooleanLiteral):
            return node.value

        if isinstance(node, ast.StringLiteral):
            return node.value

        if isinstance(node, ast.VariableRef):
            val = env.get(node.name)
            if val is _NO_RETURN:
                raise errors.undefined_variable(node.name, line)
            return val

        if isinstance(node, ast.BinaryOp):
            left = self._eval(node.left, env, line)
            right = self._eval(node.right, env, line)
            return self._arithmetic(left, node.op, right, line)

        if isinstance(node, ast.ListLiteral):
            return [self._eval(item, env, line) for item in node.items]

        if isinstance(node, ast.EmptyListLiteral):
            return []

        if isinstance(node, ast.LengthOf):
            lst = env.get(node.list_name)
            if lst is _NO_RETURN:
                raise errors.undefined_variable(node.list_name, line)
            if not isinstance(lst, list):
                raise errors.RuntimeError_(
                    f'"{node.list_name}" is not a list, so I cannot get its length.',
                    line,
                )
            return len(lst)

        if isinstance(node, ast.ItemAccess):
            lst = env.get(node.list_name)
            if lst is _NO_RETURN:
                raise errors.undefined_variable(node.list_name, line)
            if not isinstance(lst, list):
                raise errors.RuntimeError_(
                    f'"{node.list_name}" is not a list, so I cannot access items in it.',
                    line,
                )
            index = self._eval(node.index, env, line)
            if not isinstance(index, (int, float)):
                raise errors.type_mismatch_arithmetic(index, line)
            idx = int(index)
            if idx < 1 or idx > len(lst):
                raise errors.index_out_of_range(idx, node.list_name, len(lst), line)
            return lst[idx - 1]  # 1-based indexing

        if isinstance(node, ast.ResultCall):
            return self._call_function(node.func_name, node.args, env, line)

        # Fallback
        return str(node)

    # ------------------------------------------------------------------
    # Condition evaluation
    # ------------------------------------------------------------------

    def _eval_condition(self, cond: Any, env: Environment, line: int) -> bool:
        if isinstance(cond, ast.Comparison):
            left = self._eval(cond.left, env, line)
            right = self._eval(cond.right, env, line)
            return self._compare(left, cond.op, right, line)

        if isinstance(cond, ast.BooleanCheck):
            val = env.get(cond.name)
            if val is _NO_RETURN:
                raise errors.undefined_variable(cond.name, line)
            if cond.expected:
                return bool(val)
            else:
                return not bool(val)

        if isinstance(cond, ast.CompoundCondition):
            left = self._eval_condition(cond.left, env, line)
            if cond.logic == 'and':
                return left and self._eval_condition(cond.right, env, line)
            else:  # or
                return left or self._eval_condition(cond.right, env, line)

        # Treat as truthy expression
        return bool(self._eval(cond, env, line))

    # ------------------------------------------------------------------
    # Arithmetic helpers
    # ------------------------------------------------------------------

    def _arithmetic(self, left: Any, op: str, right: Any, line: int) -> Any:
        # Coerce strings that look like numbers
        left = self._coerce_number(left, line)
        right = self._coerce_number(right, line)

        if not isinstance(left, (int, float)):
            raise errors.type_mismatch_arithmetic(left, line)
        if not isinstance(right, (int, float)):
            raise errors.type_mismatch_arithmetic(right, line)

        if op == 'plus':
            result = left + right
        elif op == 'minus':
            result = left - right
        elif op == 'times':
            result = left * right
        elif op == 'divided by':
            if right == 0:
                raise errors.division_by_zero(line)
            result = left / right
        elif op == 'modulo':
            if right == 0:
                raise errors.division_by_zero(line)
            result = left % right
        else:
            raise errors.RuntimeError_(f'I do not know the operation "{op}".', line)

        # Return int when possible
        if isinstance(result, float) and result == int(result):
            return int(result)
        return result

    def _coerce_number(self, value: Any, line: int) -> Any:
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except ValueError:
                return value
        return value

    # ------------------------------------------------------------------
    # Comparison helpers
    # ------------------------------------------------------------------

    def _compare(self, left: Any, op: str, right: Any, line: int) -> bool:
        # Try numeric comparison
        try:
            l = float(left) if not isinstance(left, (int, float)) else left
            r = float(right) if not isinstance(right, (int, float)) else right
            numeric = True
        except (ValueError, TypeError):
            numeric = False

        if op == 'is equal to':
            if numeric:
                return l == r
            return str(left).lower() == str(right).lower()
        elif op == 'is not equal to':
            if numeric:
                return l != r
            return str(left).lower() != str(right).lower()
        elif op == 'is greater than':
            if numeric:
                return l > r
            return str(left) > str(right)
        elif op == 'is less than':
            if numeric:
                return l < r
            return str(left) < str(right)
        elif op == 'is greater than or equal to':
            if numeric:
                return l >= r
            return str(left) >= str(right)
        elif op == 'is less than or equal to':
            if numeric:
                return l <= r
            return str(left) <= str(right)
        else:
            raise errors.RuntimeError_(f'I do not know the comparison "{op}".', line)

    # ------------------------------------------------------------------
    # Function call helper
    # ------------------------------------------------------------------

    def _call_function(self, name: str, arg_nodes: List[Any], env: Environment, line: int) -> Any:
        key = name.lower()

        # Check native functions first
        if key in self.native_functions:
            args = [self._eval(a, env, line) for a in arg_nodes]
            return self.native_functions[key](args, line)

        if key not in self.functions:
            raise errors.undefined_function(name, line)

        func = self.functions[key]
        if len(arg_nodes) != len(func.params):
            raise errors.wrong_arg_count(name, len(func.params), len(arg_nodes), line)

        # Create new scope for the function
        local_env = Environment(parent=self.global_env)
        for param, arg_node in zip(func.params, arg_nodes):
            local_env.set(param, self._eval(arg_node, env, line))

        # Execute body
        try:
            for stmt in func.body:
                self._exec(stmt, local_env)
        except _ReturnSignal as ret:
            return ret.value

        return None
