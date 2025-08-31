from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

mood_agent = Agent(
    name="Mood Agent",
    instructions=(
        "You are a helpful agent. The user tells you how they feel. "
        "If they say 'happy' you respond: I detected your mood is happy. "
        "If they say 'sad' you respond: I detected your mood is sad. "
        "If they say 'stressed' you respond: I detected your mood is stressed. "
        "Otherwise you respond: I cannot detect your mood clearly."
    )
)

activity_agent = Agent(
    name="Activity Agent",
    instructions=(
        "You are an activity suggestion agent. "
        "If the mood is sad you suggest: 🌸 You seem sad. Try talking to a friend or listening to soft music. "
        "If the mood is stressed you suggest: 🧘 You seem stressed. Take a short walk or try meditation. "
        "If the mood is happy you suggest: 😃 You are happy! Keep enjoying your mood. "
        "Otherwise you say: No extra activity needed."
    )
)

user_input = input("How are you feeling today? ")


mood_result = Runner.run_sync(mood_agent, user_input)
print(mood_result.final_output)


activity_result = Runner.run_sync(activity_agent, mood_result.final_output)
print(activity_result.final_output)