from autoevals import LLMClassifier
from braintrust import Eval, init_function, init_dataset
from dotenv import load_dotenv
import os
from pathlib import Path

# Load the single .env at the repo root (works from any directory)
repo_root = Path(__file__).resolve().parents[4]  # file -> 03_write_custom_scorers -> evals -> src -> py -> root
load_dotenv(repo_root / ".env")

PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT")
MODEL = os.getenv("PREFERRED_MODEL")

brevity_check = LLMClassifier(
    name="Brevity Check",
    description="Check if the output is too long",
    prompt_template="""
    You are a helpful assistant that checks if the output is too long or too short.
    The output is: {{output.short_history}}

    An output is too long if it is longer than 6 sentences. If it is too long, return "long". If it is not too long, return "brief".
    """,
    choice_scores={"brief": 1, "long": 0},
    model=MODEL
)

eval_summary = Eval(
    name=PROJECT_NAME,
    data=init_dataset(PROJECT_NAME, name="Countries"),
    task=init_function(PROJECT_NAME, slug="country-structured-prompt"),
    scores=[brevity_check]
)

# eval_summary

# export BRAINTRUST_API_KEY=<YOUR_API_KEY>
# braintrust eval src/evals/03_write_custom_scorers/write_custom_scorers.py