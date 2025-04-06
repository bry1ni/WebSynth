from agno.agent import Agent
from src.mdl.agent import GPT4, TOOLS, INSTRUCTION
from src.mdl.agent.utils import extract_response_from_agent


web_synth = Agent(
    name="web_synth",
    model=GPT4,
    instructions=INSTRUCTION,
    tools=TOOLS,
    markdown=True
)

# Function to generate a response
def get_bot_response(user_input):
    result = web_synth.run(
        user_input,
        stream=False
        )
    
    response = extract_response_from_agent(result)
    return response