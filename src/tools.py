from src.utils import tool, format_tool_output

import asyncio
from crawl4ai import *


async def crawl_url(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result.markdown

@tool
def execute_crawl(url: str) -> str:
    """
    Crawl a URL and return the markdown content.
    Args:
        url: The URL to crawl.
    Returns:
        The markdown content of the URL.
    """
    return format_tool_output(asyncio.run(crawl_url(url)))


if __name__ == "__main__":
    print(execute_crawl("https://www.zad-ai.com/"))
