import os
from braintrust import Eval, init_function, init_dataset
from autoevals import ExactMatch, NumericDiff
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../../.env")

PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT")

Eval(
    PROJECT_NAME,
    data=init_dataset(PROJECT_NAME, dataset="Countries"),
    task=init_function(project_name=PROJECT_NAME, slug="country-structured-prompt"),
    scores=[
        ExactMatch,
        NumericDiff,
    ],
)

# export BRAINTRUST_API_KEY=<YOUR_API_KEY>
# uv run python -m braintrust eval src/evals/02_use_braintrust_objects/use_braintrust_objects.py 