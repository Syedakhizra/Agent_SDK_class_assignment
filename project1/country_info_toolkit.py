from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_capital(country: str) -> str:
    capitals= {
        "pakistan" : "Islamabad",
        "india" : " New Delhi",
        "china" : "Beijing",
        "usa" : "Washington, D.C."
    }
    return capitals.get(country.lower(), "Unknown")



@function_tool
def get_language(country: str) -> str:
    languages= {
        "pakistan" : "Urdu",
        "india" : " Hindi",
        "china" : "Mandarin",
        "usa" : "English"
    }
    return languages.get(country.lower(), "Unknown")


@function_tool
def get_population(country: str) -> str:
    populations= {
        "pakistan" :"240 million",
        "india" : " 1.4 billion",
        "china" : "1.41 billion",
        "usa" : "331 billion"
    }
    return populations.get(country.lower(), "Unknown")


orchestrator = Agent(
    name= "Country Info Orchestrator",
    instructions="You are a country info agent when the users gives you a country name so you used the tools " \
    "and provide full information.. when the users gve  those country who dont mention our list so you said sorry i have no info" \
    "about this country",
    tools=[get_capital, get_language, get_population],
)


prompt = input("Enter a country name:  ")
result = Runner.run_sync(orchestrator , prompt)
print(result.final_output)

