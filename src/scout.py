import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode

import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain.output_parsers.json import SimpleJsonOutputParser

load_dotenv()

def generate_url(query: str, json_parser, model) -> str:
    prompt = """
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
    
    formatted_prompt = prompt.format(query=query)

    response = model.generate_content(formatted_prompt)

    jasonified_response = json_parser.parse(response.text)

    return jasonified_response



async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://www.nbcnews.com/business")
        # Soone will be change to result.markdown
        print(result.markdown_v2.raw_markdown) 

if __name__ == "__main__":
    #asyncio.run(main())
    # LLM = GIMINI 1.5
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # JSON Parser
    json_parser = SimpleJsonOutputParser()
    results = generate_url("Latest automotive technology innovations in 2024", json_parser=json_parser, model=model)
    urls = list(map(lambda x: x['url'], results['research_urls']))
    print(urls)