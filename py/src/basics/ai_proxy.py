import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file from the root directory
load_dotenv()

# Use any model that you have configured an API Key for in Braintrust
# Accepted models are listed here: https://www.braintrust.dev/docs/guides/proxy#list-of-supported-models-and-providers
# This example uses the Claude 4 Sonnet model. You will need to provide an Anthropic API Key to Braintrust via the AI Providers UI for this model to work.
MODEL = "claude-4-sonnet-20250514"

# Configure an OpenAI client with the Braintrust API Key and the URL of the Braintrust AI proxy (URL shown is Braintrust's SaaS AI Proxy)
openai = OpenAI(
    api_key=os.getenv("BRAINTRUST_API_KEY"),
    base_url="https://api.braintrust.dev/v1/proxy",
)


async def main():
    response = await openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        seed=42,  # Optional: set a seed to invoke the AI Proxy's cache
    )
    
    print(response.choices[0].message.content)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 