"""High-level evaluation and pairwise ranking utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .metrics import length_consistency, token_jaccard
from .validators import PythonStructure, PythonValidation, analyze_python, validate_python

_DEFAULT_WEIGHTS = {
    "syntax": 0.45,
    "similarity": 0.45,
    "length": 0.10,
}


@dataclass(frozen=True)
class EvaluationResult:
    """Structured evaluation result for one Python candidate."""

    total_score: float
    syntax_score: float
    similarity_score: float
    length_score: float
    validation: PythonValidation
    structure: PythonStructure | None


@dataclass(frozen=True)
class PairwiseResult:
    """Result of comparing two candidates against one reference."""

    winner: str
    candidate_a: EvaluationResult
    candidate_b: EvaluationResult
    score_margin: float


def _validated_weights(weights: Mapping[str, float] | None) -> dict[str, float]:
    selected = dict(_DEFAULT_WEIGHTS if weights is None else weights)
    expected = set(_DEFAULT_WEIGHTS)

    if set(selected) != expected:
        raise ValueError(f"weights must contain exactly: {sorted(expected)}")
    if any(value < 0 for value in selected.values()):
        raise ValueError("weights must be non-negative")

    total = sum(selected.values())
    if total <= 0:
        raise ValueError("at least one weight must be positive")

    return {key: value / total for key, value in selected.items()}


def evaluate_python_response(
    candidate: str,
    reference: str,
    *,
    weights: Mapping[str, float] | None = None,
) -> EvaluationResult:
    """Evaluate generated Python against a reference without executing it."""
    normalized_weights = _validated_weights(weights)
    validation = validate_python(candidate)

    syntax_score = float(validation.is_valid)
    similarity_score = token_jaccard(candidate, reference)
    length_score = length_consistency(candidate, reference)

    total_score = (
        normalized_weights["syntax"] * syntax_score
        + normalized_weights["similarity"] * similarity_score
        + normalized_weights["length"] * length_score
    )

    structure = analyze_python(candidate) if validation.is_valid else None

    return EvaluationResult(
        total_score=round(total_score, 6),
        syntax_score=syntax_score,
        similarity_score=round(similarity_score, 6),
        length_score=round(length_score, 6),
        validation=validation,
        structure=structure,
    )


def rank_candidates(
    candidate_a: str,
    candidate_b: str,
    reference: str,
    *,
    weights: Mapping[str, float] | None = None,
) -> PairwiseResult:
    """Rank two Python candidates against the same reference.

    Ties are reported explicitly instead of being broken arbitrarily.
    """
    result_a = evaluate_python_response(candidate_a, reference, weights=weights)
    result_b = evaluate_python_response(candidate_b, reference, weights=weights)
    margin = result_a.total_score - result_b.total_score

    if margin > 0:
        winner = "candidate_a"
    elif margin < 0:
        winner = "candidate_b"
    else:
        winner = "tie"

    return PairwiseResult(
        winner=winner,
        candidate_a=result_a,
        candidate_b=result_b,
        score_margin=round(abs(margin), 6),
    )
