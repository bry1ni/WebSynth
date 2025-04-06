import os

from dotenv import find_dotenv, load_dotenv

from src.mdl.agent.utils import load_prompt
from src.mdl.agent.tools import execute_crawl

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat

load_dotenv(find_dotenv())

PROMPTS_DIR = os.path.dirname(__file__)
INSTRUCTION_PATH = os.path.join(PROMPTS_DIR, "instructions.md")
INSTRUCTION = load_prompt(INSTRUCTION_PATH)

GPT4 = OpenAIChat(
    id="gpt-4o",
    temperature=0.5) 

TOOLS = [execute_crawl, DuckDuckGoTools()]