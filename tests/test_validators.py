"""Tests for static Python validation."""

import pytest

from ai_eval.validators import analyze_python, validate_python


def test_valid_python() -> None:
    result = validate_python("def add(a, b):\n    return a + b\n")
    assert result.is_valid
    assert result.error_message is None


def test_invalid_python_reports_location() -> None:
    result = validate_python("def broken(:\n    pass\n")
    assert not result.is_valid
    assert result.line == 1
    assert result.error_message


def test_analyze_python_counts_structure() -> None:
    source = """
import math

class Solver:
    def solve(self, value):
        if value > 0:
            return math.sqrt(value)
        return 0
"""
    structure = analyze_python(source)

    assert structure.functions == 1
    assert structure.classes == 1
    assert structure.imports == 1
    assert structure.branches == 1


def test_analyze_python_rejects_invalid_source() -> None:
    with pytest.raises(SyntaxError):
        analyze_python("def bad(:\n")
