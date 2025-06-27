# Braintrust Evaluations Tutorial - TypeScript

This tutorial demonstrates how to perform AI and LLM evaluations using [Braintrust](https://www.braintrust.dev) with TypeScript.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- OpenAI API key
- Braintrust account and API key

### Installation

1. **Install dependencies:**
   ```bash
   cd ts
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   BRAINTRUST_API_KEY=your_braintrust_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the tutorial:**
   ```bash
   npm run dev
   ```

## 📚 Tutorial Overview

This tutorial covers several key evaluation scenarios:

### 1. Basic Evaluation (`src/examples/basic-evaluation.ts`)
- **Task**: Sentiment analysis
- **Model**: GPT-3.5 Turbo
- **Scorer**: Exact match
- **Learning**: Basic evaluation setup, simple scoring

### 2. Prompt Comparison (`src/examples/prompt-comparison.ts`)
- **Task**: Text summarization
- **Comparison**: Different prompt templates
- **Scorer**: Word overlap similarity
- **Learning**: A/B testing prompts, measuring prompt effectiveness

### 3. Model Comparison (`src/examples/model-comparison.ts`)
- **Task**: Question answering
- **Comparison**: GPT-3.5 vs GPT-4o-mini
- **Scorers**: Contains match + response length
- **Learning**: Comparing different models, multiple scoring metrics

### 4. Advanced Evaluation (`src/examples/advanced-evaluation.ts`)
- **Task**: Multi-task evaluation (math, factual, JSON, translation)
- **Scoring**: Adaptive scorers based on task type
- **Learning**: Complex evaluation scenarios, custom scoring logic

## 🛠️ Key Components

### Scoring Functions (`src/utils/scorers.ts`)

The tutorial includes several reusable scoring functions:

- **`exactMatch`**: Perfect string match (case-sensitive)
- **`exactMatchIgnoreCase`**: Perfect string match (case-insensitive)
- **`containsMatch`**: Check if expected answer is contained in output
- **`jaccardSimilarity`**: Word overlap similarity metric
- **`levenshteinSimilarity`**: Edit distance-based similarity
- **`numericAccuracy`**: For mathematical problems
- **`jsonValidityScorer`**: Validates JSON format
- **`responseLengthScorer`**: Penalizes inappropriate response lengths

### Dataset Structure

Each evaluation uses a consistent dataset format:
```typescript
const dataset = [
  {
    input: "The input text or question",
    expected: "The expected output",
    metadata?: { /* optional metadata */ }
  },
  // ... more examples
];
```

## 📊 Understanding Results

Braintrust evaluations return comprehensive results including:

- **Summary scores**: Aggregate metrics across all examples
- **Individual results**: Per-example performance
- **Metadata tracking**: Model settings, timestamps, etc.
- **Comparative analysis**: When running multiple evaluations

### Example Result Structure:
```typescript
{
  summary: {
    scores: {
      exactMatch: { mean: 0.85, ... },
      similarity: { mean: 0.72, ... }
    }
  },
  // ... detailed results
}
```

## 🔧 Available Scripts

- **`npm run dev`**: Run the tutorial with hot reloading
- **`npm run build`**: Compile TypeScript to JavaScript
- **`npm start`**: Run the compiled JavaScript
- **`npm test`**: Run Jest tests
- **`npm run type-check`**: Type check without building
- **`npm run clean`**: Remove build artifacts

## 🎯 Best Practices

### 1. Dataset Quality
- Use diverse, representative examples
- Include edge cases and challenging scenarios
- Balance positive and negative examples
- Version your datasets for reproducibility

### 2. Scoring Strategy
- Use multiple scoring metrics when appropriate
- Consider task-specific scoring functions
- Balance automated vs. human evaluation
- Document scoring rationale

### 3. Evaluation Design
- Start with simple evaluations and iterate
- Compare systematically (prompts, models, parameters)
- Track metadata for reproducibility
- Use consistent evaluation environments

### 4. Interpretation
- Look beyond aggregate scores
- Analyze failure cases
- Consider statistical significance
- Document findings and decisions

## 🏗️ Extending the Tutorial

### Adding New Evaluations

1. **Create a new example file** in `src/examples/`
2. **Define your dataset** with input/expected pairs
3. **Implement your task function** (the AI system being evaluated)
4. **Choose or create scoring functions**
5. **Run the evaluation** using `Eval()`
6. **Export your function** and import it in `src/index.ts`

### Custom Scoring Functions

Create custom scorers in `src/utils/scorers.ts`:

```typescript
export function customScorer(args: { 
  input: string; 
  output: string; 
  expected: string;
  metadata?: any;
}): number {
  // Your scoring logic here
  // Return a number between 0 and 1
}
```

### Working with Different Models

The tutorial uses OpenAI, but you can easily adapt for other providers:

```typescript
// For Anthropic Claude
import Anthropic from '@anthropic-ai/sdk';

// For local models
import { Ollama } from 'ollama';

// For Azure OpenAI
import { OpenAI } from 'openai';
const openai = new OpenAI({
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  baseURL: process.env.AZURE_OPENAI_ENDPOINT,
});
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file is properly configured
2. **Rate Limiting**: Add delays between API calls if needed
3. **Type Errors**: Run `npm run type-check` to identify issues
4. **Network Issues**: Check your internet connection and API endpoints

### Getting Help

- **Braintrust Documentation**: [docs.braintrust.dev](https://docs.braintrust.dev)
- **Braintrust Discord**: Join their community for support
- **GitHub Issues**: Report bugs or request features

## 📈 Next Steps

After completing this tutorial:

1. **Integrate with your application**: Use Braintrust in your production AI systems
2. **Explore advanced features**: Online evaluations, continuous monitoring
3. **Build custom dashboards**: Visualize your evaluation results
4. **Implement CI/CD**: Automate evaluations in your development pipeline
5. **Scale up**: Run larger evaluations with more comprehensive datasets

## 🤝 Contributing

Feel free to:
- Add new evaluation examples
- Improve existing scorers
- Enhance documentation
- Report issues or bugs
- Suggest new features

## 📄 License

This tutorial is released under the MIT License. 