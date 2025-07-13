# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a tutorial repository demonstrating AI and LLM evaluations using Braintrust. It contains parallel implementations in both TypeScript and Python, with comprehensive examples of evaluation patterns, scoring functions, and integration with the Braintrust platform.

## Development Commands

### TypeScript (ts/ directory)
- `cd ts && npm install` - Install dependencies
- `cd ts && npx tsx src/Basics/ai-proxy.ts` - Run individual TypeScript files
- `cd ts && npx braintrust eval src/Evals/00-using-autoevals/using-autoevals.ts` - Run evaluations
- No build/test scripts defined in package.json - files are run directly with tsx

### Python (py/ directory)  
- `cd py && uv sync` - Install dependencies using uv package manager
- `cd py && uv run python src/setup/braintrust_setup.py` - Initialize Braintrust project setup
- `cd py && uv run python -m braintrust eval src/evals/00_using_autoevals/using_autoevals.py` - Run evaluations
- `cd py && uv run python src/basics/ai_proxy.py` - Run individual Python files
- Code formatting: `black` and `ruff` (configured in pyproject.toml, line-length 88)

## Architecture & Key Components

### Core Structure
- **Dual-language tutorial**: Parallel TypeScript (`ts/`) and Python (`py/`) implementations
- **Braintrust integration**: Uses Braintrust platform for evaluation orchestration, datasets, prompts, and scoring
- **Evaluation patterns**: Demonstrates AutoEvals, custom scorers, prompt/model comparison, and advanced scenarios

### Key Directories
- `ts/src/Basics/` & `py/src/basics/` - AI proxy setup and prompt building fundamentals
- `ts/src/Evals/` & `py/src/evals/` - Progressive evaluation examples (00-03 numbered sequence)
- `ts/src/Setup/` & `py/src/setup/` - Braintrust project initialization utilities
- `braintrust/` - Shared data files (countries.ts/py) used across examples

### Evaluation Execution Pattern
All evaluations use the `Eval()` function with this structure:
```typescript
Eval(PROJECT_NAME, {
  data: () => dataset,           // Input/expected pairs
  task: taskFunction,            // Function being evaluated  
  scores: [scorer1, scorer2],    // Scoring functions
  experimentName: "Description"
})
```

### Environment Configuration
Both implementations require:
- `BRAINTRUST_API_KEY` - For Braintrust platform access
- `OPENAI_API_KEY` - For AI model access  
- `BRAINTRUST_PROJECT` - Project name for organization
- `PREFERRED_MODEL` - Model selection (Python only)

### AI Proxy Usage
Uses Braintrust AI Proxy (https://api.braintrust.dev/v1/proxy) as OpenAI-compatible endpoint, supporting multiple model providers through unified interface. Default model: `claude-4-sonnet-20250514`.

## Running Evaluations

Execute evaluations with the `braintrust eval` command pointing to specific evaluation files. Each numbered example (00-03) demonstrates progressively advanced evaluation concepts:

1. **00**: Basic AutoEvals usage
2. **01**: Customizing AutoEvals  
3. **02**: Using Braintrust objects (datasets, prompts)
4. **03**: Custom scorers and advanced patterns