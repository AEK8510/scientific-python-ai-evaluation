"""Small demonstration of pairwise evaluation."""

from ai_eval import evaluate_python_response, rank_candidates

REFERENCE = """
def kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity**2
"""

CANDIDATE_A = """
def kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity**2
"""

CANDIDATE_B = """
def kinetic_energy(mass, velocity)
    return mass * velocity
"""


def main() -> None:
    """Evaluate one response and then compare two candidates."""
    evaluation = evaluate_python_response(CANDIDATE_A, REFERENCE)
    print("Candidate A score:", evaluation.total_score)
    print("Candidate A syntax valid:", evaluation.validation.is_valid)
    print("Candidate A structure:", evaluation.structure)

    comparison = rank_candidates(CANDIDATE_A, CANDIDATE_B, REFERENCE)
    print("Pairwise winner:", comparison.winner)
    print("Score margin:", comparison.score_margin)


if __name__ == "__main__":
    main()
