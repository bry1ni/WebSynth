import asyncio
from langchain_google_vertexai import ChatVertexAI
from src.scout import generate_url, scrape_and_save
from langchain.output_parsers.json import SimpleJsonOutputParser


if __name__ == "__main__":
    # Ensure your VertexAI credentials are configured
    model = ChatVertexAI(model="gemini-1.5-flash")
    # JSON Parser
    json_parser = SimpleJsonOutputParser()
    # Generate URLs
    results = generate_url("Latest automotive technology innovations in 2024", json_parser=json_parser, model=model)
    urls = list(map(lambda x: x['url'], results['research_urls']))
    # Scrape URLs and save contents
    asyncio.run(scrape_and_save(urls))