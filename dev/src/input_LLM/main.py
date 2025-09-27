# main.py
# This script orchestrates the full pipeline:
# 1. Run selenium_getlinks.py to scrape and generate articles.csv.
# 2. Use swisscom_endpoint.py to select top 5 relevant links based on a current disaster description.
# 3. For each selected link, use rag_pipeline's scraper to extract 'section_title' and content.
# 4. Read phases_of_disaster.txt for context.
# 5. Send prompt to LLM to classify into Rescue, Relief, or Recovery and generate a suitable heading.

import sys
import os
import pandas as pd
from selenium_getlinks import scrape, save_csv  # Assuming selenium_getlinks has these functions
from swisscom_endpoint import generate_text, get_system_prompt  # Assuming it has these
from rag_pipeline import RAGPipeline  # To access the scraper
import sys
import os
import pandas as pd
from selenium_getlinks import scrape, save_csv  # Assuming selenium_getlinks has these functions
from swisscom_endpoint import generate_text, get_system_prompt  # Assuming it has these
from rag_pipeline import RAGPipeline  # To access the scraper
from fastapi import FastAPI

# Hardcoded or configurable
MAIN_URL = "https://reliefweb.int/disasters"  # Example URL to scrape
CSV_FILE = "articles.csv"
PHASES_FILE = "phases_of_disaster.txt"
# CURRENT_DISASTER = """Bolivia entered its seasonal dry period (June to September), a period marked by heightened wildfire risk, particularly in the eastern and Amazonian regions. This risk is exacerbated by slash-and-burn agricultural practices ("chaqueo"), which often become uncontrolled and lead to large-scale fires. On 25 August, the Bolivian government convened a meeting with the diplomatic corps and international organizations to request support for wildfire response. The discussions included needs for equipment, humanitarian aid, and technical assistance to strengthen the national response. On 20 August 2025, the Bolivian government declared a national emergency through Supreme Decree No. 5447 in response to the escalating wildfire crisis. Santa Cruz and Beni have been identified as the most affected departments. (IFRC, 15 Sep 2025)"""  # From your example
import json
import re
import os

# Inside the for loop, after getting classification
# Extract JSON from the response
import json
import re
import os

# def form_json(classification):
#     pattern = r'``````'
#     match = re.search(pattern, classification, re.DOTALL)

#     if match:
#         json_str = match.group(1).strip()
#         try:
#             data_obj = json.loads(json_str)
#             # Check if serializable (by attempting to dump)
#             json.dumps(data_obj)  # This will raise if not serializable

#             json_file = 'output.json'
            
#             # Load existing data if file exists
#             if os.path.exists(json_file):
#                 with open(json_file, 'r', encoding='utf-8') as f:
#                     existing_data = json.load(f)
#                     if not isinstance(existing_data, list):
#                         existing_data = []
#             else:
#                 existing_data = []
            
#             # Append new object
#             existing_data.append(data_obj)
            
#             # Save back to file
#             with open(json_file, 'w', encoding='utf-8') as f:
#                 json.dump(existing_data, f, indent=2)
            
#             print(f"Appended JSON to {json_file}")
#         except (json.JSONDecodeError, TypeError) as e:
#             print(f"Error: Response is not valid/serializable JSON: {e}")
#     else:
#         print(f"Error: No JSON block found in response")

def form_json(classification):
    # Try to extract JSON inside ```json ... ``` or ``` ```
    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", classification, re.DOTALL)

    if code_block:
        json_str = code_block.group(1).strip()
    else:
        # If no code block, assume entire response is JSON
        json_str = classification.strip()

    try:
        data_obj = json.loads(json_str)
        json.dumps(data_obj)  # validate serializable

        json_file = "output.json"

        # Load existing data if file exists
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
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
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Appended JSON to {json_file}")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"❌ Error: Response is not valid/serializable JSON\n{e}")

def main():
    # main.py
    # This script orchestrates the full pipeline:
    # 1. Run selenium_getlinks.py to scrape and generate articles.csv.
    # 2. Use swisscom_endpoint.py to select top 5 relevant links based on a current disaster description.
    # 3. For each selected link, use rag_pipeline's scraper to extract 'section_title' and content.
    # 4. Read phases_of_disaster.txt for context.
    # 5. Send prompt to LLM to classify into Rescue, Relief, or Recovery and generate a suitable heading.

    # Hardcoded or configurable
    MAIN_URL = "https://reliefweb.int/disasters"  # Example URL to scrape
    CSV_FILE = "articles.csv"
    PHASES_FILE = "phases_of_disaster.txt"
    # CURRENT_DISASTER = """Bolivia entered its seasonal dry period (June to September), a period marked by heightened wildfire risk, particularly in the eastern and Amazonian regions. This risk is exacerbated by slash-and-burn agricultural practices ("chaqueo"), which often become uncontrolled and lead to large-scale fires. On 25 August, the Bolivian government convened a meeting with the diplomatic corps and international organizations to request support for wildfire response. The discussions included needs for equipment, humanitarian aid, and technical assistance to strengthen the national response. On 20 August 2025, the Bolivian government declared a national emergency through Supreme Decree No. 5447 in response to the escalating wildfire crisis. Santa Cruz and Beni have been identified as the most affected departments. (IFRC, 15 Sep 2025)"""  # From your example

    # Step 1: Scrape and save to CSV using selenium_getlinks
    print("Step 1: Scraping main URL and saving to CSV...")
    scraped_data = scrape(MAIN_URL)
    save_csv(scraped_data, CSV_FILE)
    print(f"Scraped {len(scraped_data)} articles to {CSV_FILE}")

    # Step 2: Select top 5 relevant links using swisscom_endpoint
    print("Step 2: Selecting top 5 relevant news...")
    df = pd.read_csv(CSV_FILE)
    ongoing_headlines = df[df['status'].str.lower() == 'ongoing']['name'].tolist()
    heading_list = "\n".join(ongoing_headlines)
    sys_msg = get_system_prompt("SelectNews")  # Assuming this returns the prompt
    selected_text = generate_text("" , sys_msg + heading_list)
    relevant_headlines = [line.strip() for line in selected_text.split("\n") if line.strip()]
    links_map = dict(zip(df['name'], df['link']))
    
    final_links = [links_map.get(head, '') for head in relevant_headlines if head in links_map][:5]
    print(f"Selected links: {final_links}")

    # Step 3: Read phases context
    with open(PHASES_FILE, 'r', encoding='utf-8') as f:
        phases_context = f.read().strip()

    # Step 4: Initialize RAG (but we only need its scraper for detailed extraction)
    rag = RAGPipeline()

    # Step 5: For each link, scrape details, classify with LLM
    print("Step 5: Classifying and generating headings for selected links...")
    # for link in final_links:
    #     print(f"Processing {link}...")
    #     scraped_details = rag.scraper.scrape_site(link, max_items=1)  # Scrape single page
    #     if scraped_details and isinstance(scraped_details, list) and scraped_details[0].get('section_title'):
    #         section_title = scraped_details[0]['section_title']
    #         section_content = scraped_details[0]['section_content']
    #         prompt = f"Classify the following disaster content into one of: Rescue, Relief, Recovery. Provide a suitable heading. Content: {section_content}\nPhases context: {phases_context}. IMPORTANT: Now I need to render the summarized content with the corresponding classification in the front end directly! So give content in that way like in a news article for the user to read. I also want you to estimate the amount of money that could be required to mitigation and relief for this disaster. GIVE THE RESULT AS A JSON OBJECT WITH THE FOLLOWING KEYS : SECTION_TITLE, SECTION_CONTENT, CLASSIFICATION, PREDICTED_COST, TIME_OF_OCCURENCE. !!!!! GIVE ONLYY THE JSON NOTHING MORE NOTHING LESSS !!!!!"
    #         sys_msg = "You are a disaster classification expert."  # Adjust as needed
    #         classification = generate_text(prompt, sys_msg)
    #         form_json(classification)

    #         print(f"Link: {link}\nSection Title: {section_title}\nClassification and Heading: {classification}\n---")
    #     else:
    #         print(f"No section data found for {link}")

    # In your loop:
    for link in final_links:
        print(f"Processing {link}...")
        scraped_details = rag.scraper.scrape_site(link, max_items=1)  # Scrape single page
        if scraped_details and isinstance(scraped_details, list) and scraped_details[0].get('section_title'):
            section_title = scraped_details[0]['section_title']
            section_content = scraped_details[0]['section_content']
            prompt = f"Classify the following disaster content into one of: Rescue, Relief, Recovery. Provide a suitable heading. Content: {section_content}\nPhases context: {phases_context}. IMPORTANT: Now I need to render the summarized content with the corresponding classification in the front end directly! So give content in that way like in a news article for the user to read. I also want you to estimate the amount of money that could be required to mitigation and relief for this disaster. GIVE THE RESULT AS A JSON OBJECT WITH THE FOLLOWING KEYS : SECTION_TITLE, SECTION_CONTENT, CLASSIFICATION, PREDICTED_COST, TIME_OF_OCCURENCE. !!!!! GIVE ONLYY THE JSON NOTHING MORE NOTHING LESSS !!!!!"
            sys_msg = "You are a disaster classification expert."  # Adjust as needed
            classification = generate_text(prompt, sys_msg)
            form_json(classification)  # Call the function to extract and save JSON

            print(f"Link: {link}\nSection Title: {section_title}\nClassification and Heading: {classification}\n---")
        else:
            print(f"No section data found for {link}")

if "__main__" == __name__:
    main()
