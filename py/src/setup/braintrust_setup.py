import os
import braintrust
from braintrust import init_dataset
from dotenv import load_dotenv
import json
load_dotenv(dotenv_path=".env")

PROJECT_NAME = os.getenv("BRAINTRUST_PROJECT")
MODEL = os.getenv("PREFERRED_MODEL")

project = braintrust.projects.create(name=PROJECT_NAME)

country_structured_prompt = project.prompts.create(
    name="Country Structured Prompt",
    slug="country-structured-prompt",
    model=MODEL,
    if_exists="replace",
    messages=[
        {
            "content": "You are a high school geography teacher and are helping students with their class projects. When a student asks you about a country, you will give facts about that country in a structured format.",
            "role": "system"
        },
        {"content": "{{input}}", "role": "user"}
    ],
    params={
        "use_cache": True,
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "CountryStructure",
                "schema": {
                    "type": "object",
                    "required": [
                        "capital",
                        "population",
                        "currency",
                        "language",
                        "government",
                        "area",
                        "short_history"
                    ],
                    "properties": {
                        "area": {"type": "number"},
                        "capital": {"type": "string"},
                        "currency": {"type": "string"},
                        "language": {"type": "string"},
                        "government": {"type": "string"},
                        "population": {"type": "number"},
                        "short_history": {"type": "string"}
                    },
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    }
)


def create_countries_dataset():
    data = [
        {
            "input": "France",
            "expected": {
                "capital": "Paris",
                "population": 68000000,
                "currency": "Euro",
                "language": "French",
                "government": "Semi-presidential republic",
                "area": 248573,
                "short_history": "France has a rich history dating back to the Gauls and the Roman Empire. It became a kingdom in the early Middle Ages. The French Revolution in 1789 drastically reshaped its society. Napoleon Bonaparte rose to power and created an empire. France played a major role in both World Wars. After World War II, it helped found the European Union. It has a history of colonial expansion, especially in Africa and Asia. Today, it is a global power with a strong cultural influence."
            },
            "metadata": {
                "continent": "Europe"
            }
        },
        {
            "input": "Brazil",
            "expected": {
                "capital": "Brasília",
                "population": 203000000,
                "currency": "Brazilian real",
                "language": "Portuguese",
                "government": "Federal presidential republic",
                "area": 3287597,
                "short_history": "Brazil was inhabited by indigenous tribes before Portuguese colonization in 1500. It became a Portuguese colony and later an empire. It gained independence in 1822. Slavery was abolished in 1888. The country became a republic in 1889. It experienced a military dictatorship from 1964 to 1985. Brazil has undergone political and economic changes in recent decades. It remains a major economy and cultural center in South America."
            },
            "metadata": {
                "continent": "South America"
            }
        },
        {
            "input": "Japan",
            "expected": {
                "capital": "Tokyo",
                "population": 125000000,
                "currency": "Japanese yen",
                "language": "Japanese",
                "government": "Constitutional monarchy",
                "area": 145937,
                "short_history": "Japan's early history was influenced by China and Buddhism. It was ruled by emperors and powerful shoguns. The country was isolated for centuries until the 1800s. It rapidly industrialized during the Meiji era. Japan became a major imperial power in the 20th century. After World War II, it adopted a pacifist constitution. It experienced rapid economic growth in the postwar era. Today, it is a leading technological and economic power."
            },
            "metadata": {
                "continent": "Asia"
            }
        },
        {
            "input": "Canada",
            "expected": {
                "capital": "Ottawa",
                "population": 39000000,
                "currency": "Canadian dollar",
                "language": "English and French",
                "government": "Federal parliamentary democracy and constitutional monarchy",
                "area": 3855100,
                "short_history": "Canada was originally inhabited by indigenous peoples. It became a French colony in the 1600s. Britain took control in 1763. It gradually gained independence from the UK. Canada became fully sovereign in 1982. It has welcomed immigrants from around the world. It remains a bilingual country with strong regional identities. Today, Canada is known for its high quality of life and natural beauty."
            },
            "metadata": {
                "continent": "North America"
            }
        },
        {
            "input": "India",
            "expected": {
                "capital": "New Delhi",
                "population": 1410000000,
                "currency": "Indian rupee",
                "language": "Hindi and English",
                "government": "Federal parliamentary republic",
                "area": 1269219,
                "short_history": "India has one of the world's oldest civilizations. It was home to the Indus Valley Civilization. It saw a succession of empires like the Maurya and Mughal. The British colonized it in the 19th century. India gained independence in 1947. It adopted a democratic constitution in 1950. It has grown into a major global economy. India is known for its diversity in culture, language, and religion."
            },
            "metadata": {
                "continent": "Asia"
            }
        },
        {
            "input": "Australia",
            "expected": {
                "capital": "Canberra",
                "population": 27000000,
                "currency": "Australian dollar",
                "language": "English",
                "government": "Federal parliamentary constitutional monarchy",
                "area": 2969900,
                "short_history": "Australia was inhabited by Aboriginal peoples for over 60,000 years. The British began colonization in 1788. It became a federation in 1901. Australia remained closely tied to Britain during its early years. It fought in both World Wars. Post-war immigration transformed its population. It has become a multicultural democracy. Australia is known for its unique wildlife and strong economy."
            },
            "metadata": {
                "continent": "Oceania"
            }
        },
        {
            "input": "Nigeria",
            "expected": {
                "capital": "Abuja",
                "population": 223000000,
                "currency": "Naira",
                "language": "English",
                "government": "Federal presidential republic",
                "area": 356669,
                "short_history": "Nigeria has a rich pre-colonial history with many kingdoms. It became a British colony in the 19th century. It gained independence in 1960. The country experienced civil war in the 1960s. It has gone through military and civilian rule. Nigeria is Africa's most populous country. It is rich in oil and natural resources. Today, it faces challenges but remains a regional leader."
            },
            "metadata": {
                "continent": "Africa"
            }
        },
        {
            "input": "Germany",
            "expected": {
                "capital": "Berlin",
                "population": 84000000,
                "currency": "Euro",
                "language": "German",
                "government": "Federal parliamentary republic",
                "area": 137988,
                "short_history": "Germany was part of the Holy Roman Empire. It unified in 1871 under Prussia. It was a central power in both World Wars. After WWII, it was divided into East and West. The Berlin Wall symbolized the Cold War divide. It reunified in 1990 after the fall of the wall. Germany became a leading EU nation. Today, it has a strong economy and democratic institutions."
            },
            "metadata": {
                "continent": "Europe"
            }
        },
        {
            "input": "Egypt",
            "expected": {
                "capital": "Cairo",
                "population": 110000000,
                "currency": "Egyptian pound",
                "language": "Arabic",
                "government": "Presidential republic",
                "area": 386662,
                "short_history": "Egypt is home to one of the world's oldest civilizations. Ancient Egypt thrived along the Nile for thousands of years. It was conquered by Persians, Greeks, and Romans. Islam spread after Arab conquest in the 7th century. It was a part of the Ottoman Empire. Egypt gained independence in the 20th century. The Suez Canal has strategic importance. Today, it is a cultural and political center in the Arab world."
            },
            "metadata": {
                "continent": "Africa"
            }
        },
        {
            "input": "Mexico",
            "expected": {
                "capital": "Mexico City",
                "population": 130000000,
                "currency": "Mexican peso",
                "language": "Spanish",
                "government": "Federal presidential republic",
                "area": 1964375,
                "short_history": "Mexico has a rich indigenous history with civilizations like the Maya and Aztec. It was colonized by Spain in the 16th century. It gained independence in 1821 after a long struggle. The country experienced political instability and foreign interventions. The Mexican Revolution transformed its society. Mexico industrialized in the 20th century. Today, it is a major economy and cultural center in Latin America."
            },
            "metadata": {
                "continent": "North America"
            }
        }
    ]
    
    # Create and populate the dataset
    dataset = init_dataset(PROJECT_NAME, name="Countries", api_key=os.getenv("BRAINTRUST_API_KEY"))
    for item in data:
        dataset.insert(input=item["input"], expected=item["expected"], metadata=item["metadata"])
    
    return dataset


def create_multiturn_dataset():
    # Read the JSON file and extract input values
    with open("src/setup/data/MultiturnDataset.json", "r") as f:
        json_data = json.load(f)
    
    data = []
    for item in json_data:
        data.append({"input": item["input"]})
    
    # Create and populate the dataset
    dataset = init_dataset(PROJECT_NAME, name="Multiturn", api_key=os.getenv("BRAINTRUST_API_KEY"))
    for item in data:
        dataset.insert(input=item["input"])
    
    return dataset

if __name__ == "__main__":
    #create_countries_dataset()
    create_multiturn_dataset()
    project.publish()
    print("Countries dataset created successfully!") 
    print("Multiturn dataset created successfully!") 