import { loadPrompt, Eval, initFunction, initDataset } from "braintrust";
import {ExactMatch, NumericDiff} from "autoevals"
import dotenv from "dotenv";

dotenv.config();

const PROJECT_NAME: string = process.env.BRAINTRUST_PROJECT || "My App";

Eval(
    PROJECT_NAME, 
    {
        data: initDataset(PROJECT_NAME, {dataset: "Countries"}),
        task: initFunction({projectName: PROJECT_NAME, slug: "country-structured-prompt"}),
        scores: [
            ExactMatch,
            NumericDiff
        ]
    }
)

// export BRAINTRUST_API_KEY=<YOUR_API_KEY>
// npx braintrust eval src/Evals/02-use-braintrust-objects/use-braintrust-objects.ts