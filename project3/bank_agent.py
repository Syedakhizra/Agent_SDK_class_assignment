
   #                      🏦 Bank Agent Mini Project with Guardrails & Handoffs

from dotenv import load_dotenv
load_dotenv()
from agents import (
    Agent, Runner, RunContextWrapper,
    function_tool, input_guardrail, output_guardrail,
    GuardrailFunctionOutput
)
from pydantic import BaseModel


class Account(BaseModel):
    name: str
    pin: int
    balance: int = 1000000
    loan_amount : int = 50000


class GuardrailOutput(BaseModel):
    is_not_bank_related: bool


guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="Check if the query is bank related" \
    "if not , set is_not_bank_related = True.",
    output_type=GuardrailOutput,
)

@input_guardrail
async def check_bank_related(ctx:RunContextWrapper[None], agent:Agent, input:str)->GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input , context = ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_bank_related
    )

@output_guardrail
def no_apologies_guardrail(ctx:RunContextWrapper[None], agent:Agent, output: str) -> GuardrailFunctionOutput:
    if "sorry" in output.lower():
        return GuardrailFunctionOutput(output_info="Apologies blocked",tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Safe Output",tripwire_triggered=False)


def check_user(ctx:RunContextWrapper[Account], agent: Agent)->bool:
     return ctx.context.name == "Khizra" and ctx.context.pin == 1234
      

@function_tool(is_enabled=check_user)
def check_balance(wrapper : RunContextWrapper[Account]):
    user = wrapper.context
    return f"The balance of {user.name} account is {user.balance}"


@function_tool(is_enabled=check_user)
def check_loan(wrapper : RunContextWrapper[Account]):
    user = wrapper.context
    return f"{user.name}. your outstanding loan amount is ${user.loan_amount}"



bank_agent = Agent(
    name= "Bank Agent",
    instructions="You are a bank agent. Handle account ad balance queries.Only respond if the user is authenticated",
    tools=[check_balance],
    input_guardrails=[check_bank_related],
    output_guardrails=[no_apologies_guardrail],
)


loan_agent = Agent(
    name="Loan Agent",
    instructions="You are loan agent, Handle user loan related queries. Only respond if the user is authenticated",
    tools=[check_loan],
    input_guardrails=[check_bank_related],
    output_guardrails=[no_apologies_guardrail],
)

triage_agent = Agent(
    name= "Triage Agent",
    instructions="You are the triage agent."
    "if the query is about balance or account-> return bank agent" \
    "if the query is about loan -> return loan Agent",
    handoffs=[bank_agent, loan_agent],
    input_guardrails=[check_bank_related],
    output_guardrails=[no_apologies_guardrail],
)

user_context = Account(name="Khizra" , pin = 1234)

prompt = input("Enter your question about bank related?")
result = Runner.run_sync(triage_agent, prompt , context= user_context)

print(result.final_output)