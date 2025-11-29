"""Safe math expression evaluator with date/time support."""
import ast
import operator
# todo: edge case
import math
from datetime import datetime, timedelta
from typing import Any

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

SAFE_FUNCS = {
    "abs": abs, "round": round, "min": min, "max": max,
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "ceil": math.ceil, "floor": math.floor,
    "pi": math.pi, "e": math.e,
}


def _eval_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"unsupported constant: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op_fn = SAFE_OPS.get(type(node.op))
        if not op_fn:
            raise ValueError(f"unsupported operator: {type(node.op).__name__}")
        return op_fn(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op_fn = SAFE_OPS.get(type(node.op))
        if not op_fn:
            raise ValueError(f"unsupported unary op: {type(node.op).__name__}")
        return op_fn(_eval_node(node.operand))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCS:
            fn = SAFE_FUNCS[node.func.id]
            args = [_eval_node(a) for a in node.args]
            if callable(fn):
                return fn(*args)
            return fn
        raise ValueError(f"unsupported function: {ast.dump(node.func)}")
    if isinstance(node, ast.Name) and node.id in SAFE_FUNCS:
        val = SAFE_FUNCS[node.id]
        if not callable(val):
            return val
    raise ValueError(f"unsupported expression: {ast.dump(node)}")


def safe_eval(expression: str) -> float:
    """Evaluate a math expression safely without exec/eval."""
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body)


def current_time() -> str:
    return datetime.now().isoformat()


def days_between(date1: str, date2: str) -> int:
    d1 = datetime.fromisoformat(date1)
    d2 = datetime.fromisoformat(date2)
    return abs((d2 - d1).days)
