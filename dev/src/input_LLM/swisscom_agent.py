# from langchain.agents import AgentExecutor, create_react_agent
# from langchain.tools import Tool
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from swisscom_llm import SwisscomLLM  # Your wrapper
# from web_scraping import DisasterNewsScraper  # Your scraper
# from rag_pipeline import RAGPipeline  # Your RAG class
# import requests
# from bs4 import BeautifulSoup

# # Initialize Swisscom LLM (for agents)
# swisscom_llm = SwisscomLLM(api_key="YOUR_SWISSCOM_API_KEY")

# # Tool 1: Recursive Scraper (follows links for full content)
# def recursive_scrape(url, depth=1, max_depth=2, max_items=5):
#     if depth > max_depth:
#         return []
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         soup = BeautifulSoup(response.text, 'html.parser')
#         articles = []  # Extract headlines/links (use your scraper logic)
#         full_texts = []
#         # Example: Follow links and get body text
#         for link in soup.find_all('a', href=True)[:max_items]:
#             article_url = link['href']
#             if not article_url.startswith('http'):
#                 from urllib.parse import urljoin
#                 article_url = urljoin(url, article_url)
#             try:
#                 art_resp = requests.get(article_url)
#                 art_soup = BeautifulSoup(art_resp.text, 'html.parser')
#                 body = art_soup.find('article') or art_soup.find('div', class_='content')
#                 text = body.get_text(strip=True) if body else ''
#                 full_texts.append(text[:2000])  # Limit length
#             except:
#                 pass
#         # Recurse on a relevant link (e.g., first one)
#         if articles and depth < max_depth:
#             full_texts += recursive_scrape(articles[0]['url'], depth + 1, max_depth)
#         return full_texts
#     except Exception as e:
#         return [f"Error: {e}"]

# scrape_tool = Tool(
#     name="RecursiveScraper",
#     func=recursive_scrape,
#     description="Recursively scrapes disaster news from a URL, following links up to depth 2 for full content."
# )

# # Tool 2: RAG Context Retriever (from your rag_pipeline)
# rag = RAGPipeline("YOUR_SWISSCOM_API_KEY")  # Adapted for Swisscom
# def rag_retrieve(query):
#     rag.build_index()  # Or specify locality
#     texts, _ = rag.retrieve(query)
#     return "\n".join(texts)

# rag_tool = Tool(
#     name="RAGRetriever",
#     func=rag_retrieve,
#     description="Retrieves relevant context from scraped disaster news using RAG."
# )

# # Agent Setup
# tools = [scrape_tool, rag_tool]
# memory = ConversationBufferMemory(memory_key="chat_history")

# prompt = PromptTemplate.from_template(
#     "You are a disaster management agent. Use tools to scrape news recursively, retrieve context, summarize problems, and suggest govt/NGO actions.\n{input}\n{agent_scratchpad}"
# )

# agent = create_react_agent(
#     llm=swisscom_llm,  # Your Swisscom wrapper
#     tools=tools,
#     prompt=prompt
# )

# executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, max_iterations=5)

# # Run the agent
# result = executor.invoke({"input": "Analyze flooding issues in Asia: scrape recent news, retrieve context, summarize problems, and suggest actions for govt and NGOs."})
# print("Agent Output:", result['output'])


# agentic_pipeline.py
import os
import openai
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI  # OpenAI-compatible for Swisscom
from web_scraping import DisasterNewsScraper  # Your scraper
from rag_pipeline import RAGPipeline  # Your RAG class
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Setup Swisscom client (your code)
client = openai.OpenAI(
    api_key=os.getenv("SWISSCOM_API"),
    base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
)

# LangChain LLM wrapper for Swisscom (OpenAI-compatible)
llm = OpenAI(
    openai_api_key=os.getenv("SWISSCOM_API"),
    base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1",
    model="swiss-ai/Apertus-70B"  # Or Apertus-8B if preferred
)

# Tool 1: Recursive Scraper (follows links for full content)
def recursive_scrape(url, depth=0, max_depth=2, max_items=5):
    if depth > max_depth:
        return []
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        full_texts = []
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)[:max_items] if 'disaster' in a.text.lower() or 'flood' in a.text.lower()]  # Filter relevant
        for link in links:
            try:
                art_resp = requests.get(link, timeout=10)
                art_soup = BeautifulSoup(art_resp.text, 'html.parser')
                body = art_soup.find('article') or art_soup.find('div', class_='content-body') or art_soup
                text = body.get_text(strip=True)[:2000]  # Limit length
                if text:
                    full_texts.append(text)
            except:
                pass
        # Recurse on first relevant link
        if links and depth < max_depth:
            full_texts += recursive_scrape(links[0], depth + 1, max_depth)
        return full_texts
    except Exception as e:
        return [f"Scraping error: {e}"]

scrape_tool = Tool(
    name="RecursiveScraper",
    func=recursive_scrape,
    description="Recursively scrapes disaster news from a URL, following relevant links up to depth 2 for full article content."
)

# Tool 2: RAG Context Retriever (from your rag_pipeline)
rag = RAGPipeline()  # If RAG needs key, adjust; assumes it works without for retrieval
def rag_retrieve(query):
    rag.build_index()  # Rebuild or specify locality
    texts, _ = rag.retrieve(query)
    return "\n".join(texts)

rag_tool = Tool(
    name="RAGRetriever",
    func=rag_retrieve,
    description="Retrieves relevant context from scraped disaster news using RAG."
)

# Agent Setup (Multi-Agent via React pattern)
tools = [scrape_tool, rag_tool]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

prompt = PromptTemplate.from_template(
    "You are a disaster management agent. Use tools to scrape news recursively, retrieve context, then summarize problems and suggest govt/NGO actions.\n"
    "Break down complex queries into steps. Always verify data before summarizing.\n"
    "{input}\n{agent_scratchpad}"
)

agent = create_react_agent(
    llm=llm,  # Swisscom via OpenAI wrapper
    tools=tools,
    prompt=prompt
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,  # Prints agent thoughts/steps
    max_iterations=10  # Prevent infinite loops
)

# Run the agent with example query
if __name__ == "__main__":
    result = executor.invoke({
        "input": "Analyze flooding issues in Asia: start by scraping recent news from https://reliefweb.int/disasters, retrieve context, summarize key problems, and suggest actions for govt and NGOs."
    })
    print("Agent Output:", result['output'])
