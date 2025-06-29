import os
from braintrust import Eval
from autoevals import ExactMatch, EmbeddingSimilarity
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../../.env")

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
def process_inputs(input_text, hooks):
    hooks.metadata["example"] = "writing to metadata" # Write to metadata during the task run
    return input_text


Eval(
    PROJECT_NAME,
    data=lambda: dataset,
    task=process_inputs,  # input and hooks are automatically passed to the task function
    scores=[
        ExactMatch,  # using ExactMatch from AutoEvals. Compares the output and expected values
        EmbeddingSimilarity(model="text-embedding-ada-002"),  # using EmbeddingSimilarity from AutoEvals. Compares the output and expected values using cosine similarity
    ],
    experiment_name="Using AutoEvals",
)

# export BRAINTRUST_API_KEY=<YOUR_API_KEY>
# braintrust eval src/evals/00_using_autoevals/using_autoevals.py 