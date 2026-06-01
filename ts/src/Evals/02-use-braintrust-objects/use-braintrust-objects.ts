import { loadPrompt, Eval, initFunction, initDataset } from "braintrust";
import {ExactMatch, NumericDiff} from "autoevals"
import dotenv from "dotenv";
import * as path from "path";

// Load the single .env at the repo root (02-use-braintrust-objects -> Evals -> src -> ts -> root)
dotenv.config({ path: path.resolve(__dirname, "../../../../.env") });

const PROJECT_NAME: string = process.env.BRAINTRUST_PROJECT || "multiturn-agent";

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