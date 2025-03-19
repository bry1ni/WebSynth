import json
import os
import inspect
import importlib.util
from typing import Dict, List, Any
import re


def get_agents_tools() -> Dict[str, List[Any]]:
    """
    Dynamically retrieves tool functions organized by agent name from the tools directory.
    Each .py file in the tools directory represents an agent's toolset.

    Returns:
        Dict[str, List[Any]]: Dictionary mapping agent names to their respective tools list
        Example: {
            'orchestrator': [tool1, tool2],
            'research': [tool3, tool4],
            ...
        }
    """
    tools_dir = "src/tools"
    agent_tools = {}

    # Iterate through all .py files in the tools directory
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            # Get agent name from filename (without .py extension)
            agent_name = filename[:-3]

            # Import the module
            module_name = f"src.tools.{agent_name}"
            module_spec = importlib.util.spec_from_file_location(
                module_name,
                os.path.join(tools_dir, filename)
            )

            if module_spec and module_spec.loader:
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)

                # Initialize tool list for this agent
                agent_tools[agent_name] = []

                # Inspect members of the module
                for name, obj in inspect.getmembers(module):
                    # Check if the object is callable and has tool decorator attributes
                    if callable(obj) and hasattr(obj, "_is_tool") and obj._is_tool:
                        agent_tools[agent_name].append(obj)

                # Remove agent entry if no tools were found
                if not agent_tools[agent_name]:
                    del agent_tools[agent_name]

    return agent_tools


def get_tool_from(tools : dict, agent_name: str, tool_name: str) -> Any:
    """
    Retrieves a specific tool from a specific agent.
    
    Args:
        agent_name (str): Name of the agent that has the tool.
        tool_name (str): Name of the tool to retrieve.
            
    Returns:
        Any: The requested tool function.
        
    Raises:
        KeyError: If agent_name is not found in the TOOLS dictionary.
        ValueError: If the specified tool_name is not found for the agent.
    """
    if agent_name not in tools:
        raise KeyError(f"Agent '{agent_name}' not found in available tools.")
    
    # Find the tool with matching name
    matching_tools = [tool for tool in tools[agent_name] if tool.__name__ == tool_name]
    
    if not matching_tools:
        raise ValueError(f"Tool '{tool_name}' not found for agent '{agent_name}'")
    
    return matching_tools[0]


def extract_response_from_agent(response):

    assistant_response = next(
        (msg.content for msg in response.messages if msg.role == "assistant" and msg.content), 
        None
    )

    return assistant_response


def tool(name=None, description=None):
    """
    Decorator to mark a function as a tool and add metadata.
    
    Args:
        name (str, optional): Custom name for the tool. Defaults to function name.
        description (str, optional): Description of what the tool does. 
                                    Defaults to function docstring.
    
    Returns:
        Callable: The decorated function
    """
    def decorator(func):
        # Mark this function as a tool
        func._is_tool = True
        
        # Add metadata
        func.tool_metadata = {
            "name": name or func.__name__,
            "description": description or func.__doc__ or "",
            "function": func.__name__
        }
        
        return func
    
    # Handle case where decorator is used without arguments
    if callable(name):
        func = name
        name = None
        return decorator(func)
    
    return decorator

def is_url(string) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        string (str): The string to check.
        
    Returns:
        bool: True if the string is a valid URL, False otherwise.
    """
    
    # Regular expression pattern for URL validation
    # This handles http, https, ftp protocols, with or without www
    # and various domain extensions
    pattern = re.compile(
        r'^(?:http|https|ftp)s?://'  # http://, https://, ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(re.match(pattern, string))


def format_tool_output(tool_message: Any) -> str:
    """
    Formats the tool message into a JSON string ensuring it's always a valid str.
    
    Args:
        tool_message (Any): The tool message to be converted (typically a dict).
    
    Returns:
        str: JSON formatted string representation of the tool message.
    """
    return json.dumps(tool_message, ensure_ascii=False)

def load_prompt(file_path):
    """
    Load the content of a `.md` file as a string.

    Args:
        file_path (str): Path to the markdown file.

    Returns:
        str: Content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()