from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()


product_suggester = Agent(
    name="Product Suggester Agent",
    instructions="You are a helpful agent when the user says:I have a headache so you suggest that" \
    " You can take Panadol. It helps with headache and fever.when the user says:I have stomach pain " \
    " so you suggest that: You can take an antacid. It helps with stomach pain. when the user says:" \
    " I have cold so you suggest that:You can take anti-cold syrup. It helps relieve flu and sneezingwhen user says anything else " \
    "so you says i am here only for suggestion the  best products for you. "
)



prompt = input("Tell me about your problem?  ")
result = Runner.run_sync(product_suggester, prompt)
print(result.final_output)

