import os
from dotenv import load_dotenv
from braintrust import load_prompt
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(dotenv_path="../../.env")

# Get the Braintrust project name from the environment variables
PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT", "My App")

# Configure an OpenAI client with the Braintrust API Key and the URL of the Braintrust AI proxy (URL shown is Braintrust's SaaS AI Proxy)
# "Building" a prompt will work without using the Braintrust AI Proxy as well as long as the model provider can accept OpenAI prompt arguments
openai = OpenAI(
    api_key=os.getenv("BRAINTRUST_API_KEY"),
    base_url="https://api.braintrust.dev/v1/proxy",
)


def main():
    # Use the load_prompt function to load the prompt from the Braintrust project
    prompt = load_prompt(
        project=PROJECT_NAME,
        slug="country-structured-prompt",
        api_key=os.getenv("BRAINTRUST_API_KEY"),
        no_trace=True,  # set no_trace to True in order to remove span data and directly build the prompt into an OpenAI compliant object
    )
    
    # Use the build function to build the prompt into an OpenAI compliant object
    prompt_config = prompt.build(input="France")  # `input` is a variable in this prompt, which we can set during the build of the prompt.
    
    response = openai.chat.completions.create(**prompt_config)
    
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

# Example response:
# {
#     "area": 551695,
#     "capital": "Paris",
#     "currency": "Euro (EUR)",
#     "language": "French",
#     "government": "Unitary semi-presidential republic",
#     "population": 68000000,
#     "short_history": "France has a long and influential history, from being part of the Roman Empire to the rise of the Frankish kingdoms. 
#         It became a powerful monarchy in the Middle Ages, played a central role in the Renaissance and Enlightenment, 
#         and underwent the French Revolution in 1789, which led to the end of the monarchy and the rise of the republic. 
#         France has been a major player in European and world affairs, including both World Wars, and is a founding member of the European Union."
# } 