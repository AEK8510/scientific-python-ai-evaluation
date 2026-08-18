# Scientific Python AI Evaluation

A compact, test-driven Python project for evaluating AI-generated scientific and Python outputs.

This repository is a **public portfolio and engineering demonstration project**. It shows practical patterns for deterministic evaluation, static Python validation, pairwise comparison, reproducible metrics, and CI-backed software quality. It does not contain confidential employer, research, or customer code.

## What this project demonstrates

- clean Python package design;
- deterministic evaluation metrics;
- static validation of AI-generated Python without executing untrusted code;
- pairwise ranking of candidate responses;
- structured evaluation reports;
- unit tests with `pytest`;
- automated quality checks with GitHub Actions;
- type hints and modern Python packaging.

## Use case

AI coding and scientific-assistant systems often generate several candidate answers. A useful evaluation layer should combine simple objective checks into a transparent score rather than relying on one opaque metric.

This package provides small reusable components to:

1. validate Python syntax;
2. compare generated text with a reference;
3. measure token overlap and length consistency;
4. summarize Python source structure with the AST;
5. produce a weighted score;
6. rank two candidate responses.

## Repository structure

```text
scientific-python-ai-evaluation/
├── src/
│   └── ai_eval/
│       ├── __init__.py
│       ├── evaluator.py
│       ├── metrics.py
│       └── validators.py
├── tests/
│   ├── test_evaluator.py
│   ├── test_metrics.py
│   └── test_validators.py
├── examples/
│   └── demo.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
└── README.md
```

## Installation

```bash
git clone https://github.com/AEK8510/scientific-python-ai-evaluation.git
cd scientific-python-ai-evaluation
python -m venv .venv
```

Activate the environment and install the project:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Quick example

```python
from ai_eval import evaluate_python_response, rank_candidates

reference = '''
def kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity**2
'''

candidate_a = '''
def kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity**2
'''

candidate_b = '''
def kinetic_energy(mass, velocity)
    return mass * velocity
'''

result = evaluate_python_response(candidate_a, reference)
print(result.total_score)

winner = rank_candidates(candidate_a, candidate_b, reference)
print(winner.winner)
```

The validator uses Python's `ast` module and **does not execute generated code**.

## Evaluation components

### Text similarity

The package includes normalized exact match and Jaccard token similarity. These intentionally simple metrics are deterministic and easy to audit.

### Python static validation

Generated Python is parsed with the standard-library AST. The report includes:

- syntax validity;
- syntax error location when invalid;
- number of functions;
- number of classes;
- number of imports;
- basic branch count.

### Weighted scoring

`evaluate_python_response` combines:

- syntax validity;
- token similarity to a reference;
- response-length consistency.

The weights are explicit and can be changed by the caller.

> This repository is intentionally transparent: these metrics are baseline engineering checks, not a claim that lexical overlap alone measures model intelligence or code correctness.

## Run the demo

```bash
python examples/demo.py
```

## Run tests and quality checks

```bash
pytest
ruff check .
```

## Design principles

- **Safety:** no execution of untrusted generated Python.
- **Reproducibility:** deterministic metrics and explicit weights.
- **Auditability:** structured results expose each component score.
- **Simplicity:** standard library first; minimal dependencies.
- **Testability:** core behavior covered by automated tests.

## Possible extensions

- sandboxed execution for trusted benchmark suites;
- unit-test pass rate as an evaluation signal;
- numerical tolerance metrics for scientific outputs;
- code complexity and maintainability analysis;
- model-to-model pairwise evaluation datasets;
- statistical confidence intervals across benchmark sets;
- asynchronous evaluation pipelines.

## Author

**Ahmed El Kerim, PhD**  
Research Engineer — Scientific Computing | HPC | AI/ML | Engineering Simulation
