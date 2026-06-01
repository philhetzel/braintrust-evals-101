import os
from pathlib import Path
from braintrust import Eval, init_function, init_dataset
from autoevals import ExactMatch, NumericDiff
from dotenv import load_dotenv

repo_root = Path(__file__).resolve().parents[4]  # file -> 02_use_braintrust_objects -> evals -> src -> py -> root
load_dotenv(repo_root / ".env")

PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT")

Eval(
    PROJECT_NAME,
    data=init_dataset(PROJECT_NAME, name="Countries"),
    task=init_function(project_name=PROJECT_NAME, slug="country-structured-prompt"),
    scores=[
        ExactMatch,
        NumericDiff,
    ],
)
