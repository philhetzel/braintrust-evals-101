import { Eval } from "braintrust";
import { ExactMatch, EmbeddingSimilarity } from "autoevals";
import dotenv from "dotenv";

dotenv.config();

const PROJECT_NAME: string = process.env.BRAINTRUST_PROJECT || "My App";

const dataset = [
  {
    input: "foo",
    expected: "foo",
    metadata: {
      next: "bar",
    },
  },
  {
    input: "bar",
    expected: "bar",
    metadata: {
      next: "baz",
    },
  },
];

// this is the function that we will place into the Eval's task argument
// tasks have two arguments: input and hooks
// `input` originates in the input field of the Eval's data argument
// `hooks` is an object that allows you to actively write to the task's metadata (potentially to use in scorers)
async function processInputs(input: string, hooks: any) {
  hooks.metadata.result = input; // write to the task's metadata
  return input;
}

interface Metadata {
  result?: string;
  next: string;
}

// Normally the AutoEvals scorer compares the embedding similarity of the task's output and expected value
// Here, we remap the expected value to the task's metadata.result field
const determinedEmbeddingSimilarity = (args: {
  output: string;
  metadata: Metadata;
}) => {
  return EmbeddingSimilarity({
    expected: args.metadata.next,
    output: args.output,
  });
};

// This is a deterministic custom scorer. Custom scorers can take input, output, expected, and metadata as arguments.
async function determineExactMatch(args: {
  input: string;
  output: string;
  expected: string;
  metadata: any;
}) {
  return {
    score: args.output === args.expected ? 1 : 0,
    name: "Custom Exact Match",
  };
}

Eval(PROJECT_NAME, {
  data: () => dataset,
  task: processInputs, // input and hooks are automatically passed to the task function
  scores: [
    determineExactMatch, // using a custom scorer
    ExactMatch, // using ExactMatch from AutoEvals
    determinedEmbeddingSimilarity,
  ],
  experimentName: "Basic Eval",
});

// export BRAINTRUST_API_KEY=<YOUR_API_KEY>
// npx braintrust eval src/Evals/01-basic-eval/basic-eval.ts
