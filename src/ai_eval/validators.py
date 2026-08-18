"""Static validators for AI-generated Python source code."""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class PythonValidation:
    """Result of a Python syntax-validation pass."""

    is_valid: bool
    error_message: str | None = None
    line: int | None = None
    offset: int | None = None


@dataclass(frozen=True)
class PythonStructure:
    """Simple AST-derived structure summary for Python source."""

    functions: int
    classes: int
    imports: int
    branches: int


def validate_python(source: str) -> PythonValidation:
    """Validate Python syntax without executing the source."""
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return PythonValidation(
            is_valid=False,
            error_message=exc.msg,
            line=exc.lineno,
            offset=exc.offset,
        )

    return PythonValidation(is_valid=True)


def analyze_python(source: str) -> PythonStructure:
    """Return a simple AST structure summary.

    Raises:
        SyntaxError: If ``source`` is not valid Python.
    """
    tree = ast.parse(source)

    functions = 0
    classes = 0
    imports = 0
    branches = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1
        elif isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try)):
            branches += 1

    return PythonStructure(
        functions=functions,
        classes=classes,
        imports=imports,
        branches=branches,
    )
