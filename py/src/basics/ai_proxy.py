import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load the single .env at the repo root (file -> basics -> src -> py -> root)
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# Use any model that you have configured an API Key for in Braintrust
# Accepted models are listed here: https://www.braintrust.dev/docs/guides/proxy#list-of-supported-models-and-providers
# This example uses the Claude 4 Sonnet model. You will need to provide an Anthropic API Key to Braintrust via the AI Providers UI for this model to work.
MODEL = os.getenv("PREFERRED_MODEL")

# Configure an OpenAI client with the Braintrust API Key and the URL of the Braintrust AI proxy (URL shown is Braintrust's SaaS AI Proxy)
openai = OpenAI(
    api_key=os.getenv("BRAINTRUST_API_KEY"),
    base_url="https://gateway.braintrust.dev"
    # base_url="https://api.braintrust.dev/v1/proxy", # Braintrust's SaaS AI Proxy is deprecated in favor of the new Gateway Proxy
)


def main():
    response =  openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        seed=42,  # Optional: set a seed to invoke the AI Proxy's cache
    )
    
    print(response.choices[0].message.content)


if __name__ == "__main__":
  main()