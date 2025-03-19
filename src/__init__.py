import os

from dotenv import find_dotenv, load_dotenv

from src.utils import load_prompt
from src.tools import execute_crawl

from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat

load_dotenv(find_dotenv())

PROMPTS_DIR = os.path.dirname(__file__)
ZBOT_INSTRUCTION_PATH = os.path.join(PROMPTS_DIR, "instructions.md")
ZBOT_INSTRUCTION = load_prompt(ZBOT_INSTRUCTION_PATH)

GPT4 = OpenAIChat(
    id="gpt-4o",
    temperature=0.5)

TOOLS = [execute_crawl, TavilyTools()]