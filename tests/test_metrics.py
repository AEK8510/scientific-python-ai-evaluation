"""Tests for deterministic evaluation metrics."""

import pytest

from ai_eval.metrics import exact_match, length_consistency, token_jaccard


def test_exact_match_normalizes_whitespace() -> None:
    assert exact_match("x = 1\n", "x   =   1") == 1.0


def test_token_jaccard_identical_text_is_one() -> None:
    assert token_jaccard("return x + y", "return x + y") == 1.0


def test_token_jaccard_partial_overlap() -> None:
    score = token_jaccard("return x + y", "return x + z")
    assert 0.0 < score < 1.0


def test_length_consistency_is_symmetric() -> None:
    first = length_consistency("abc", "abcdef")
    second = length_consistency("abcdef", "abc")
    assert first == pytest.approx(second)
    assert first == pytest.approx(0.5)


def test_empty_lengths() -> None:
    assert length_consistency("", "") == 1.0
    assert length_consistency("", "value") == 0.0
