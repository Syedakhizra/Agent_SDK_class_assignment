from dotenv import load_dotenv
load_dotenv()
from agents import Agent,Runner,function_tool,RunContextWrapper,input_guardrail,output_guardrail,GuardrailFunctionOutput,ModelSettings
from pydantic import BaseModel


class UserContext(BaseModel):
    name:str
    member_id:str = None
    

class GuardrailOutput(BaseModel):
    is_not_library_related : bool


guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="You are a guardrail agent. Only allow queries related to searching" \
    "books, check availability or library timings for anything else " \
    "set is_not_library_related =True.",
    output_type=GuardrailOutput,
)


@input_guardrail
async def check_library_related(ctx: RunContextWrapper[None], agent: Agent, input: str)->GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent,input,context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_library_related
    )



book_data = {
    "python programming": 3,
    "data science": 2,
    "machine learning": 0,
    "ai agents": 5,
}

@function_tool
def search_book(book_name :str) -> str:
    if book_name.lower() in book_data:
        return f"{book_name} exist in the library catalog"
    else:
        return f"{book_name} not found in the library"
    
def is_member(ctx: RunContextWrapper[UserContext], agent:Agent) -> bool:
    return ctx.context.member_id is not None



@function_tool(is_enabled=is_member)
def check_availability(wrapper: RunContextWrapper[UserContext], book_name: str) -> str:
    user = wrapper.context
    if book_name.lower() in book_data:
        copies = book_data[book_name.lower()]
        return f"'{book_name}' availability: {copies} copies."
    return f"No record found for '{book_name}'."

    

@function_tool
def library_timings()-> str:
    return f"Library timings are 9 AM to 8 PM , Monday to Saturday "


def dynamic_instruction(ctx: RunContextWrapper[UserContext] , agent:Agent):
    return f"user name is {ctx.context.name}. Always greet them by name and you help user with book search , availaibility and timings. "


library_agent = Agent(
    name="Library Assistant",
    instructions=dynamic_instruction,
    tools=[search_book,check_availability,library_timings],
    input_guardrails=[ check_library_related],
    model_settings=ModelSettings(
        temperature=0.3,
        tool_choice="auto",
        max_tokens=120
    )
)


ctx = UserContext(name="Khizra" , member_id="M123")

prompt = input("Enter your query about library... ")
result = Runner.run_sync(library_agent,prompt,context=ctx)
print(result.final_output)