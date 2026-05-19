To run:

```
export BRAINTRUST_API_KEY=<YOUR_API_KEY>
braintrust eval src/evals/00_using_autoevals/using_autoevals.py 
```

We use an `ExactMatch` scorer and an `EmbeddingSimilarity` scorer here:

- EmbeddingSimilarity gives us a measure of Semantic comparison (i.e. embeddings encode meaning. "The capital of France is Paris." and "Paris is France's capital." would score near 1.0 with EmbeddingSimilarity but 0.0 with ExactMatch).
- Embeddings are far cheaper and lower-latency than running an LLM-as-judge scorer (e.g., Factuality),
  so it's a good default fuzzy scorer to pair with stricter checks.