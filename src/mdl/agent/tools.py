from src.mdl.agent.utils import tool, format_tool_output

import asyncio
from crawl4ai import *
import re


async def crawl_url(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result.markdown

@tool
def execute_crawl(url: str) -> str:
    """
    Crawls a specified URL and extracts its content in markdown format.
    
    Use this tool when you need to extract detailed information from a specific webpage.
    This is ideal for gathering in-depth content when you already have a relevant URL.
    
    Args:
        url: The complete URL to crawl (must include http:// or https:// protocol).
              Example: "https://example.com/article"
    
    Returns:
        The webpage content converted to markdown format, including text, tables, and 
        basic formatting. Returns error message if the URL is invalid or cannot be accessed.
    
    Note: 
        - Only use with publicly accessible webpages
        - Some websites may block automated crawling
        - For dynamic JavaScript-heavy sites, results may be limited
    """
    return format_tool_output(asyncio.run(crawl_url(url)))

@tool
def extract_url(query: str) -> str:
    """
    Extracts the first valid URL found in a text string.
    
    Use this tool as the first step when a user provides a message containing a URL
    that needs to be analyzed. The extracted URL can then be passed to execute_crawl().
    
    Args:
        query: Text string that potentially contains one or more URLs.
               Example: "Can you analyze this page: https://example.com/article"
    
    Returns:
        The first complete URL found in the query, exactly as it appears.
        Returns an empty string if no valid URL is found.
    
    Example usage flow:
        1. User asks: "What's on this site: https://example.com/page"
        2. extract_url() → returns "https://example.com/page"
        3. Pass this result to execute_crawl()
    """
    # Regular expression pattern to match URLs
    # This pattern matches common URL formats (http, https, ftp) as well as URLs without protocol
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*|www\.(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*'
    
    # Search for the URL pattern in the query
    match = re.search(url_pattern, query)
    
    # Return the matched URL or empty string if not found
    return format_tool_output(match.group(0) if match else "")


if __name__ == "__main__":
    print(execute_crawl("https://www.zad-ai.com/"))
