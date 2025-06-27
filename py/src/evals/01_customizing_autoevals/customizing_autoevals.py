import os
from braintrust import Eval
from autoevals import ExactMatch, EmbeddingSimilarity
from dotenv import load_dotenv
from typing import Dict, Any

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
def process_inputs(input_text, hooks):
    hooks.metadata["result"] = input_text  # write to the task's metadata
    return input_text


# Normally the AutoEvals scorer compares the embedding similarity of the task's output and expected value
# Here, we remap the expected value to the task's metadata.result field
def determined_embedding_similarity(metadata: dict, output: str):
    return EmbeddingSimilarity().eval(
        expected=metadata["next"],
        output=output,
    )


# This is a deterministic custom scorer. Custom scorers can take input, output, expected, and metadata as arguments.
def determine_exact_match(output: str, expected: str):
    return {
        "score": 1 if output == expected else 0,
        "name": "Custom Exact Match",
    }


Eval(
    PROJECT_NAME,
    data=lambda: dataset,
    task=process_inputs,  # input and hooks are automatically passed to the task function
    scores=[
        determine_exact_match,  # using a custom scorer
        ExactMatch,  # using ExactMatch from AutoEvals. Gathers the output and expected values from the task and dataset, respectively
        determined_embedding_similarity,  # using remapped AutoEval
    ],
    experiment_name="Customizing AutoEvals",
)

# export BRAINTRUST_API_KEY=<YOUR_API_KEY>
# braintrust eval customizing_autoevals.py 