import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ResearchScraper:
    def __init__(self, model, json_parser):
        self.model = model
        self.json_parser = json_parser
        load_dotenv()

    def generate_url(self, query: str) -> dict:
        """
        Generates a list of highly relevant, credible URLs for conducting research on a given topic.
        """
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""
                You are an advanced web research specialist tasked with generating a list of highly relevant, credible URLs for conducting comprehensive research on a given topic. Your goal is to provide a diverse set of authoritative sources that cover different angles and perspectives.

                RESEARCH URL GENERATION INSTRUCTIONS:
                1. Generate a list of 5-7 unique, high-quality URLs
                2. Ensure URLs are from reputable sources
                3. Cover different perspectives and aspects of the topic
                4. Prioritize recent, authoritative sources
                5. Avoid duplicate domains
                6. Focus on academic, professional, and industry-leading websites

                OUTPUT REQUIREMENTS:
                - Strictly use the following JSON structure
                - Include metadata to justify URL selection
                - Ensure all URLs are valid and publicly accessible

                {{
                "research_urls": [
                    {{
                    "url": "full_url_here",
                    "domain": "domain_name",
                    "relevance_score": 0-10,
                    "content_focus": "specific_angle_of_research",
                    "rationale": "brief_explanation_why_url_was_selected"
                    }}
                ],
                "generation_timestamp": "current_iso_timestamp"
                }}

                CRITICAL RULES:
                - NEVER include placeholder or example URLs
                - ALL URLs must be REAL and VALID
                - URLs must be directly related to the research topic
                - Verify each URL is likely to contain substantial, relevant information

                RESEARCH TOPIC: {query}
            """
        )
        
        research_chain = LLMChain(
            llm=self.model,
            prompt=prompt_template,
            output_parser=self.json_parser
        )
        
        response = research_chain.run(query=query)
        jasonified_response = self.json_parser.parse(response)

        return jasonified_response

    async def crawl_url(self, url):
        """
        Crawls a single URL to retrieve its content.
        """
        async with AsyncWebCrawler(verbose=True) as crawler:
            try:
                result = await crawler.arun(url=url)
                return result.markdown_v2.raw_markdown
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                return None

    async def scrape_and_save(self, urls, output_file="knowledgeBase.md"):
        """
        Scrapes a list of URLs and saves the content to a markdown file.
        """
        tasks = [self.crawl_url(url) for url in urls]
        results = await asyncio.gather(*tasks)

        with open(output_file, "a") as f:
            for url, content in zip(urls, results):
                if content:
                    f.write(f"# Source: {url}\n")
                    f.write(content)
                    f.write("\n\n")
                else:
                    f.write(f"# Source: {url}\n")
                    f.write("Failed to retrieve content.\n\n")