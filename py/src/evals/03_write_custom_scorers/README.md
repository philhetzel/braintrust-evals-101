To run:

```
export BRAINTRUST_API_KEY=<YOUR_API_KEY>
braintrust eval src/evals/03_write_custom_scorers/write_custom_scorers.py
```

This module uses LLMClassifier (from autoevals) which uses an LLM to grade an eval output by picking from a fixed set of labels. Here, that is:

```
choice_scores={"brief": 1, "long": 0},
```
