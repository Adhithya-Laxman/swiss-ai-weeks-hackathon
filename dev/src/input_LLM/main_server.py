# main_server.py
import os
import re
import json
import pandas as pd
from fastapi import FastAPI
from selenium_getlinks import scrape, save_csv
from swisscom_endpoint import generate_text, get_system_prompt
from rag_pipeline import RAGPipeline

app = FastAPI()

# Hardcoded/configurable
MAIN_URL = "https://reliefweb.int/disasters"
CSV_FILE = "articles.csv"
PHASES_FILE = "phases_of_disaster.txt"
OUTPUT_FILE = "output.json"


def form_json(classification: str):
    """
    Extract JSON from classification response and append to output.json.
    Returns the parsed JSON object.
    """
    # Try to extract JSON inside ```json ... ``` or ``` ```
    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", classification, re.DOTALL)
    if code_block:
        json_str = code_block.group(1).strip()
    else:
        json_str = classification.strip()

    try:
        data_obj = json.loads(json_str)
        json.dumps(data_obj)  # validate serializable

        # Load existing data if file exists
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
            if not isinstance(existing_data, list):
                existing_data = []
        else:
            existing_data = []

        # Append new object
        existing_data.append(data_obj)

        # Save back to file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Appended JSON to {OUTPUT_FILE}")
        return data_obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"❌ Error: Response is not valid/serializable JSON\n{e}")
        return {"error": "Invalid JSON from LLM", "raw": classification}


@app.get("/get_news")
def backend():
    # Step 1: Scrape main URL and save to CSV
    scraped_data = scrape(MAIN_URL)
    save_csv(scraped_data, CSV_FILE)

    # Step 2: Select top 5 relevant links
    df = pd.read_csv(CSV_FILE)
    ongoing_headlines = df[df['status'].str.lower() == 'ongoing']['name'].tolist()
    heading_list = "\n".join(ongoing_headlines)
    sys_msg = get_system_prompt("SelectNews")
    selected_text = generate_text("", sys_msg + heading_list)
    relevant_headlines = [line.strip() for line in selected_text.split("\n") if line.strip()]
    links_map = dict(zip(df['name'], df['link']))
    final_links = [links_map.get(head, '') for head in relevant_headlines if head in links_map][:5]

    # Step 3: Read phases context
    with open(PHASES_FILE, 'r', encoding='utf-8') as f:
        phases_context = f.read().strip()

    # Step 4: Initialize RAG (for scraper)
    rag = RAGPipeline()

    # Step 5: Process links
    results = []
    for link in final_links:
        scraped_details = rag.scraper.scrape_site(link, max_items=1)
        if scraped_details and isinstance(scraped_details, list) and scraped_details[0].get('section_title'):
            section_content = scraped_details[0]['section_content']
            prompt = (
                f"Classify the following disaster content into one of: Rescue, Relief, Recovery. "
                f"Provide a suitable heading. Render the summarized content with the corresponding classification "
                f"in the front end directly like a news article. Estimate the amount of money required for mitigation "
                f"and relief. GIVE THE RESULT AS A JSON OBJECT WITH KEYS: SECTION_TITLE, SECTION_CONTENT, "
                f"CLASSIFICATION, PREDICTED_COST, TIME_OF_OCCURENCE. ONLY RETURN JSON.\n\n"
                f"Content: {section_content}\nPhases context: {phases_context}."
            )
            sys_msg = "You are a disaster classification expert."
            classification = generate_text(prompt, sys_msg)
            parsed = form_json(classification)
            results.append({"link": link, "data": parsed})
        else:
            results.append({"link": link, "error": "No section data found"})

    # Return all accumulated JSON from file
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            accumulated = json.load(f)
    else:
        accumulated = []

    return {"new_results": results, "all_results": accumulated}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_server:app", host="0.0.0.0", port=8000, reload=True)
