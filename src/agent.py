from agno.agent import Agent
from src import GPT4, TOOLS, ZBOT_INSTRUCTION
from src.utils import extract_response_from_agent


web_synth = Agent(
    name="zbot",
    model=GPT4,
    instructions=ZBOT_INSTRUCTION,
    tools=TOOLS,
    markdown=True
)

# Function to generate a response
def get_bot_response(user_input):
    result = web_synth.run(
        user_input,
        stream=True
        )
    
    response = extract_response_from_agent(result)
    return response