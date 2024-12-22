import asyncio
from langchain_google_vertexai import ChatVertexAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from src.scout import ResearchScraper

if __name__ == "__main__":
    # Ensure your VertexAI credentials are configured
    model = ChatVertexAI(model="gemini-1.5-flash")
    # JSON Parser
    json_parser = SimpleJsonOutputParser()
    # Instantiate the ResearchScraper
    scraper = ResearchScraper(model=model, json_parser=json_parser)
    # Generate URLs
    results = scraper.generate_url("Latest automotive technology innovations in 2024")
    urls = list(map(lambda x: x['url'], results['research_urls']))
    # Scrape URLs and save contents
    asyncio.run(scraper.scrape_and_save(urls))
