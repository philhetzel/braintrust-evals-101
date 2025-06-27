import { OpenAI } from "openai";
import * as dotenv from "dotenv";
import * as path from "path";

// Load .env file from the root directory
dotenv.config();

// Use any model that you have configured an API Key for in Braintrust
// Accepted models are listed here: https://www.braintrust.dev/docs/guides/proxy#list-of-supported-models-and-providers
// This example uses the Claude 4 Sonnect model. You will need to provide an Anthropic API Key to Braintrust via the AI Providers UI for this model to work.
const MODEL = "claude-4-sonnet-20250514";

// Configure an OpenAI client with the Braintrust API Key and the URL of the Braintrust AI proxy (URL shown is Braintrust's SaaS AI Proxy)
const openai = new OpenAI({
    apiKey: process.env.BRAINTRUST_API_KEY,
    baseURL: "https://api.braintrust.dev/v1/proxy",
});

async function main() {
    const response = await openai.chat.completions.create({
        model: MODEL,
        messages: [{ role: "user", content: "Hello, how are you?" }],
        seed: 42, // Optional: set a seed to invoke the AI Proxy's cache
    });
    
    console.log(response.choices[0].message.content);
}

main()
