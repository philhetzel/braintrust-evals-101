import os
from braintrust import Eval
from autoevals import ExactMatch, EmbeddingSimilarity
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from py directory (works from any directory)
py_dir = Path(__file__).parents[3]  # Go up 3 levels: file -> 00_using_autoevals -> evals -> src -> py
load_dotenv(py_dir / ".env")

PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT")

dataset = [
    {
        "input": "foo",
        "expected": "foo",
        "metadata": {
            "next": "bar",
        },
    },
    {
        "input": "bar",
        "expected": "bar",
        "metadata": {
            "next": "baz",
        },
    },
]

# this is the function that we will place into the Eval's task argument
# tasks have two arguments: input and hooks
# `input` originates in the input field of the Eval's data argument
# `hooks` is an object that allows you to actively write to the task's metadata (potentially to use in scorers)
# we'll talk more about hooks in the next example
def process_inputs(input, hooks):
    hooks.metadata["example"] = "writing to metadata" # Write to metadata during the task run
    
    return input # what the task returns becomes the `output` of a task, which is then sent to scorers


Eval(
    PROJECT_NAME,
    data=lambda: dataset, # data will have a mandatory `input` field, and optional `expected` and `metadata` fields. Datasets stored in Braintrust can be loaded direction through init_dataset()
    task=process_inputs,  # input and hooks are automatically passed to the task function
    scores=[
        ExactMatch,  # using ExactMatch from AutoEvals. Compares the output and expected values
        EmbeddingSimilarity(model="text-embedding-ada-002"),  # using EmbeddingSimilarity from AutoEvals. Compares the output and expected values using cosine similarity
    ],
    experiment_name="Using AutoEvals",
)

# export BRAINTRUST_API_KEY=<YOUR_API_KEY>
# braintrust eval src/evals/00_using_autoevals/using_autoevals.py 