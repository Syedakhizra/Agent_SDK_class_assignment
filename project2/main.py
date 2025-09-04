from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class UserContext(BaseModel):
    name: str
    is_premium_user: bool = False
    issue_type: str = "general"


@function_tool
def refund(wrapper: RunContextWrapper[UserContext]) -> str:
    user = wrapper.context
    if user.is_premium_user:
        return f"Refund approved for {user.name}"
    else:
        return "Refund not available. Only premium users can request refunds."


@function_tool
def restart_service(wrapper: RunContextWrapper[UserContext]) -> str:
    user = wrapper.context
    if user.issue_type == "technical":
        return f"Service restarted for {user.name}. Please check again."
    else:
        return "Restart only works for technical issues."


@function_tool
def general_info(wrapper: RunContextWrapper[UserContext]) -> str:
    user = wrapper.context
    return f"Hello {user.name}, thanks for reaching out! How can I assist you today?"


billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing and refund queries using the refund tool.",
    tools=[refund],
)

technical_agent = Agent(
    name="Technical Agent",
    instructions="You handle technical issues using the restart_service tool.",
    tools=[restart_service],
)

general_agent = Agent(
    name="General Agent",
    instructions="You handle general queries using the general_info tool.",
    tools=[general_info],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are the triage agent. Based on the user's query, you must hand off to exactly one of: "
        "'Billing Agent', 'Technical Agent', or 'General Agent'. "
        "Reply ONLY with one of these three names."
    ),
    handoffs=[billing_agent, technical_agent, general_agent],
)


def main():
    name = input("Name: ")
    premium = input("Premium user? (yes/no): ").lower() == "yes"
    issue_type = input("Issue type (billing/technical/general): ").lower()

    ctx = UserContext(name=name, is_premium_user=premium, issue_type=issue_type)

    query = input("\nPlease describe your issue: ")

    
    choice = Runner.run_sync(triage_agent, query).final_output.strip()

    agent = {
        "Billing Agent": billing_agent,
        "Technical Agent": technical_agent,
        "General Agent": general_agent,
    }.get(choice, general_agent)


    print(f"\n Handoff: {choice}")

    result = Runner.run_sync(agent, query, context=ctx)
    
    print("Response:", result.final_output)


if __name__ == "__main__":
    main()
