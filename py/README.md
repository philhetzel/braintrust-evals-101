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

## Anatomy of Custom Scorers

Custom scorers are the heart of effective AI evaluations. They judge the quality of an output on a scale from 0 to 1, allowing you to quantify how well your AI system performs on specific tasks.

### What is an Eval?
![What is an Eval](../assets/WhatIsAnEval.png)

An evaluation consists of three main components:
- **Dataset**: Input/expected output pairs that represent your test cases
- **Task**: The AI system or function you're evaluating
- **Scorers**: Functions that measure how well the task output matches expectations

### Two Types of Custom Scorers

#### 1. Code-Based Custom Scorers
![Code based custom scorers](../assets/AnatomyOfCodeBasedScorer.png)

Code-based scorers give you complete programmatic control over evaluation logic. They can:
- Take up to four arguments: `input`, `output`, `expected`, and `metadata`
- Implement arbitrarily complex scoring algorithms
- Return a score between 0 and 1
- Access task metadata for context-aware scoring

**Example use cases:**
- Mathematical accuracy checking
- JSON format validation
- Custom similarity metrics
- Domain-specific business logic

##### Creating a custom code-cased scorer

You can also create a function to score the outputs of your Eval task. Like Eval tasks, code based scorers can be of arbitrary complexity. They can (but don't always have to) take four arguments:
- `input`: Is derived from the evaluation case dataset's input field.
- `output`: Is derived from the Eval task's returned output
- `expected`: Is derived from the evaluation case dataset's expected field
- `metadata`: Is derived from both the evaluation case dataset's metadata field OR any information written to `hooks.metadata` during the task's execution

#### 2. LLM-as-a-Judge Scorers
![Custom LLM-as-a-judge scorers](../assets/AnatomyOfLLMJudge.png)

LLM-as-a-judge scorers use language models to evaluate outputs, perfect for nuanced or subjective criteria. They:
- Use `LLMClassifierFromTemplate()` for TypeScript, `LLMClassifier()` function for python
- Allow for dynamically providing information from your Dataset or Eval Task through the `{{input}}`, `{{output}}`, `{{expected}}`, and. `{{metadata}}` variables
- Map LLM choices to numerical scores (0-1 scale)
- Handle complex, contextual evaluation criteria

**Example use cases:**
- Content quality assessment
- Tone and style evaluation
- Factual accuracy checking
- Creative output assessment

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



## 🔧 Running Evaluations

**Important**: Always run evaluations from the `py` directory:

```bash
# Make sure you're in the py directory
cd py

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Export environment variables from .env file
# Unix/macOS
export $(grep -v '^#' .env | xargs)

# Windows
for /f "usebackq tokens=1,2 delims==" %i in (".env") do if not "%i"=="#*" set %i=%j

# Run evaluations
braintrust eval src/evals/00_using_autoevals/using_autoevals.py
braintrust eval src/evals/01_customizing_autoevals/customizing_autoevals.py
braintrust eval src/evals/02_use_braintrust_objects/use_braintrust_objects.py
braintrust eval src/evals/03_write_custom_scorers/write_custom_scorers.py
```

Alternatively, you can run with `uv run` if you export the variables first:
```bash
# Unix/macOS
export $(grep -v '^#' .env | xargs)
uv run braintrust eval src/evals/00_using_autoevals/using_autoevals.py

# Windows
for /f "usebackq tokens=1,2 delims==" %i in (".env") do if not "%i"=="#*" set %i=%j
uv run braintrust eval src/evals/00_using_autoevals/using_autoevals.py
``` 