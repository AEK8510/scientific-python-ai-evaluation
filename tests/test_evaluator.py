"""Tests for high-level evaluation behavior."""

import pytest

from ai_eval.evaluator import evaluate_python_response, rank_candidates


REFERENCE = """
def square(value: float) -> float:
    return value**2
"""


def test_valid_reference_like_candidate_scores_high() -> None:
    result = evaluate_python_response(REFERENCE, REFERENCE)
    assert result.total_score == pytest.approx(1.0)
    assert result.validation.is_valid
    assert result.structure is not None


def test_invalid_candidate_has_zero_syntax_score() -> None:
    candidate = "def square(value)\n    return value**2"
    result = evaluate_python_response(candidate, REFERENCE)
    assert result.syntax_score == 0.0
    assert result.structure is None


def test_pairwise_ranking_prefers_valid_matching_candidate() -> None:
    good = REFERENCE
    bad = "def square(value)\n    return value"
    result = rank_candidates(good, bad, REFERENCE)
    assert result.winner == "candidate_a"
    assert result.score_margin > 0


def test_weight_validation() -> None:
    with pytest.raises(ValueError):
        evaluate_python_response(
            REFERENCE,
            REFERENCE,
            weights={"syntax": 1.0},
        )


def test_weights_are_normalized() -> None:
    result = evaluate_python_response(
        REFERENCE,
        REFERENCE,
        weights={"syntax": 2.0, "similarity": 2.0, "length": 1.0},
    )
    assert result.total_score == pytest.approx(1.0)
