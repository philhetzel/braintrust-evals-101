# Braintrust Evaluations Tutorial - Python

This tutorial demonstrates how to perform AI and LLM evaluations using [Braintrust](https://www.braintrust.dev) with Python.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Braintrust account and API key

### Installation

1. **Install uv (if not already installed):**
   ```bash
   # Unix/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   # Download and run installer from https://github.com/astral-sh/uv/releases
   ```

2. **Create a virtual environment with Python 3.12:**
   ```bash
   cd py
   uv venv --python 3.12
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Set up environment variables:**   
   Create a `.env` file in the `py` directory and add your API keys:
   ```env
   BRAINTRUST_API_KEY=your_braintrust_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   BRAINTRUST_PROJECT=a_unique_project_name
   PREFERRED_MODEL=gpt-4o-mini
   ```

5. **Export BRAINTRUST_API_KEY to environment:**
   ```bash
   # Unix/macOS
   export BRAINTRUST_API_KEY=$(grep "BRAINTRUST_API_KEY=" .env | cut -d'=' -f2)
   
   # Windows
   for /f "tokens=2 delims==" %i in ('findstr "BRAINTRUST_API_KEY=" .env') do set BRAINTRUST_API_KEY=%i
   ```

6. **Load your sample Braintrust environment:**
   ```bash
   uv run python src/setup/braintrust_setup.py
   ```

   This will load a prompt and a dataset into a your Braintrust project named after your environment variable BRAINTRUST_PROJECT.

## 📚 Tutorial Overview

This tutorial covers several key evaluation scenarios:

### 1. AI Proxy (`src/basics/ai_proxy.py`)
- **Task**: Using Braintrust AI proxy
- **Learning**: Model configuration, API setup
- **Important**: This example uses Claude 4 Sonnet. You must configure an Anthropic API key in [Braintrust's AI Providers page](https://www.braintrust.dev/docs/guides/proxy#using-braintrust-api-keys) for this to work

### 2. Using Braintrust as a Prompt Store (`src/basics/prompt_building.py`)
- **Task**: Building and using prompts
- **Learning**: Prompt templates, variable substitution

### 3. Using AutoEvals (`src/evals/00_using_autoevals/using_autoevals.py`)
- **Task**: Basic evaluation with AutoEvals
- **Learning**: Built-in scoring functions

### 4. Customizing AutoEvals (`src/evals/01_customizing_autoevals/customizing_autoevals.py`)
- **Task**: Using AutoEvals where customization is needed
- **Learning**: Creating custom evaluators

### 5. Using Braintrust assets (`src/evals/02_use_braintrust_objects/use_braintrust_objects.py`)
- **Task**: Calling datasets and functions directly from Braintrust
- **Learning**: How to use Braintrust as a central store for datasets, prompts, and functions

### 6. Writing custom scorers (`src/evals/03_write_custom_scorers/write_custom_scorers.py`)
- **Task**: Write custom scorers
- **Learning**: How to to use inputs, outputs, expected outputs, and metadata in scorers.

## What is an Eval?

[Watch this video for a complete explanation!](https://www.loom.com/share/827e68cd769f4e6ab1f1dec6ac61dc5f?sid=a5ae5a44-8f0c-4d0f-96de-bb156be5669e)

### Description
An Eval is a way to judge the quality of some task or function's output. Usually that task is an LLM and prompt but that is not always the case. Evals are made up of three things:
- **Data**: An array of inputs that you want to place into a task to create outputs. Can also include the expected values after a task transforms the input as well as any metadata of interest.
- **Task**: Some function that takes an input and transforms it. Usually an LLM and prompt but can be either more or less complex.
- **Scorers**: A function that judges the quality of an output between 0 and 1. Judgement can be made via an LLM-as-a-judge or a deterministic code-based function.

![What is an Eval](../assets/WhatIsAnEval.png)

### What does an Eval look like:

```python
 Eval("Name of your Braintrust Project",
      task=task,  # your task function's identifier. The Eval assumes that the task has arguments of input and hooks
      data=init_dataset(project=project_name, dataset="WeatherActivityDataset"),  # your data with inputs and optional metadata and expected fields. This example pulls a dataset from Braintrust directly however you can load any data into an Eval as long as it has a field called "input"
      scores=[tool_call_check, structure_check, faithfulness_check]  # function identifiers for scores.
  )
```

### How do I run an Eval?

In Braintrust, Eval experiments can be run via the command line. If writing your evals in python, you can initiate a Braintrust experiment by running:

```bash
braintrust eval path/to/eval/eval_filename.py
```

## How do Eval tasks work?

Eval tasks are a blank slate - usually Eval tasks are a combination of a prompt and a model; however, Eval tasks can be much more complicated (or even much simpler) than that! When setting up an Eval task, create a function that has two arguments: `input` and `hooks`.
- `input`: When running `Eval()` in Braintrust, `Eval()` is going to pass the `data`'s input field dynamically to the function assigned to the `task` argument. Inputs can be as simple as a string or as complex as a multi turn conversation with multi-modal attachments. 
- `hooks`: Hooks is an object that you can use to either retrieve or write metadata to an Eval task. An example: let's imagine that you are running a RAG pipeline. The output returned by your task should be the assistant's final reponse but you may want to keep the context that your LLM brought back from a vector dataset. You can assign the context brought back from the vector database to `hooks.metadata["context"]`, and then retrieve that information later in a scoring function.

```python
def task(input, hooks):
      # transform your input to create an output
      task_output = input + "how's this for a transformation?"

      # write to a task's metadata
      hooks.metadata["value_you_want_later"] = "See you in the scoring function!"

      # send the task's output to a scoring function
      return task_output
```

## Creating a custom LLM-as-a-Judge scrorer

Often you will want to create an LLM with a prompt that determines the quality of another LLM's output. Braintrust enables engineers to create custom LLM scorers through the `LLMClassifier()` function in the `autoevals` package. The function takes several arguments
- `name`: What you want to call the LLM-as-a-judge in the Braintrust Experiment results
-  `prompt_template`: Describes in plain language what you want the prompt to judge. You can insert variables into the prompt template by using  `{{mustache}}` references. Within the prompt, you should be precise about what you want the LLM to judge. Give specific choices ("a", "b", "c") to the judge within the language of the promptTemplate which will match with the choices in the `choice_scores` argument. Common variables to insert into prompts are:
    - `{{input}}`: Is derived from the evaluation case dataset's input field.
    - `{{output}}`: Is derived from the Eval task's returned output
    - `{{expected}}`: Is derived from the evaluation case dataset's expected field
    - `{{metadata}}`: Is derived from both the evaluation case dataset's metadata field OR any information written to `hooks.metadata` during the task's execution
- `choice_scores`: A mapping of 0-1 scores associated with each possible choice
- `model`: The LLM that you want to use for scoring
- `use_cot`: Whether or not you want the prompt to be appended with chain-of-thought reasoning. Not to be confused with the reasoning component of newer models

**Example:**
```python
brevity_check = LLMClassifier(
    name="Brevity Check",
    description="Check if the output is too long",
    prompt_template="""
    You are a helpful assistant that checks if the output is too long or too short.
    The output is: {{output.short_history}}

    An output is too long if it is longer than 6 sentences. If it is too long, return "long". If it is not too long, return "brief".
    """,
    choice_scores={"brief": 1, "long": 0},
    model="gpt-4o-mini"
)
```

![Custom LLM-as-a-judge](../assets/AnatomyOfLLMJudge.png)

## Creating a custom code-cased scorer

You can also create a function to score the outputs of your Eval task. Like Eval tasks, code based scorers can be of arbitrary complexity. They can (but don't always have to) take four arguments:
- `input`: Is derived from the evaluation case dataset's input field.
- `output`: Is derived from the Eval task's returned output
- `expected`: Is derived from the evaluation case dataset's expected field
- `metadata`: Is derived from both the evaluation case dataset's metadata field OR any information written to `hooks.metadata` during the task's execution

```python
def determine_exact_match(output: str, expected: str): #can include input, output, expected, and metadata as arguments.
    return {
        "score": 1 if output == expected else 0,
        "name": "Custom Exact Match",
    }
```
![Custom code scorer](../assets/AnatomyOfCodeBasedScorer.png)