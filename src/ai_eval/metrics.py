"""Deterministic metrics for evaluating generated responses."""

from __future__ import annotations

import re

_TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\S")


def _normalize(text: str) -> str:
    """Normalize whitespace for deterministic string comparison."""
    return " ".join(text.strip().split())


def _tokens(text: str) -> set[str]:
    """Return a case-normalized token set."""
    return {token.lower() for token in _TOKEN_PATTERN.findall(text)}


def exact_match(candidate: str, reference: str) -> float:
    """Return 1.0 when normalized strings match, otherwise 0.0."""
    return float(_normalize(candidate) == _normalize(reference))


def token_jaccard(candidate: str, reference: str) -> float:
    """Compute Jaccard similarity between token sets.

    Returns 1.0 when both inputs contain no tokens.
    """
    candidate_tokens = _tokens(candidate)
    reference_tokens = _tokens(reference)

    if not candidate_tokens and not reference_tokens:
        return 1.0

    union = candidate_tokens | reference_tokens
    if not union:
        return 1.0

    return len(candidate_tokens & reference_tokens) / len(union)


def length_consistency(candidate: str, reference: str) -> float:
    """Score how similar candidate and reference lengths are.

    The score is in ``[0, 1]`` and uses normalized character counts.
    Empty-versus-empty scores 1.0; empty-versus-nonempty scores 0.0.
    """
    candidate_length = len(_normalize(candidate))
    reference_length = len(_normalize(reference))

    if candidate_length == reference_length == 0:
        return 1.0
    if candidate_length == 0 or reference_length == 0:
        return 0.0

    return min(candidate_length, reference_length) / max(
        candidate_length, reference_length
    )
