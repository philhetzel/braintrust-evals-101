import dotenv from "dotenv";
import { loadPrompt } from "braintrust";
import { OpenAI } from "openai";

// Load environment variables from .env file
dotenv.config();

// Get the Braintrust project name from the environment variables
const PROJECT_NAME: string = process.env.BRAINTRUST_PROJECT || "My App";

// Configure an OpenAI client with the Braintrust API Key and the URL of the Braintrust AI proxy (URL shown is Braintrust's SaaS AI Proxy)
// "Building" a prompt will work without using the Braintrust AI Proxy as well as long as the model provider can accept OpenAI prompt arguments
const openai = new OpenAI({
  apiKey: process.env.BRAINTRUST_API_KEY,
  baseURL: "https://api.braintrust.dev/v1/proxy",
});

async function main() {
  // Use the loadPrompt function to load the prompt from the Braintrust project
  const prompt = await loadPrompt({
    projectName: PROJECT_NAME,
    slug: "country-structured-prompt",
    apiKey: process.env.BRAINTRUST_API_KEY,
    noTrace: true, // set noTrace to true in order to remove span data and directly build the prompt into an OpenAI compliant object
  });
  // Use the build function to build the prompt into an OpenAI compliant object
  const response = await openai.chat.completions.create({
    ...prompt.build({ input: "France" }), // `input` is a variable in this prompt, which we can set during the build of the prompt.
  });

  console.log(response.choices[0].message.content);
  
}

main();
// Example response:
// {
    // "area":551695,
    // "capital":"Paris",
    // "currency":"Euro (EUR)",
    // "language":"French",
    // "government":"Unitary semi-presidential republic",
    // "population":68000000,
    // "short_history":"France has a long and influential history, from being part of the Roman Empire to the rise of the Frankish kingdoms. 
        // It became a powerful monarchy in the Middle Ages, played a central role in the Renaissance and Enlightenment, 
        // and underwent the French Revolution in 1789, which led to the end of the monarchy and the rise of the republic. 
        // France has been a major player in European and world affairs, including both World Wars, and is a founding member of the European Union."
// }
