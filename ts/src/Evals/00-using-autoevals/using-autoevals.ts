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
// we'll talk more about hooks in the next example
async function processInputs(input: string, hooks: any) {
  return input;
}

Eval(PROJECT_NAME, {
  data: () => dataset,
  task: processInputs, // input and hooks are automatically passed to the task function
  scores: [
    ExactMatch, // using ExactMatch from AutoEvals. Compares the output and expected values
    EmbeddingSimilarity.partial({model: "text-embedding-ada-002"}), // using EmbeddingSimilarity from AutoEvals. Compares the output and expected values using cosine similarity. Partial can edit the default arguments of the autoeval
  ],
  experimentName: "Using AutoEvals",
});

// export BRAINTRUST_API_KEY=<YOUR_API_KEY>
// npx braintrust eval src/Evals/01-basic-eval/basic-eval.ts