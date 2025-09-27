import os
import openai
import pandas as pd
from fastapi import FastAPI
# from process_csv import get_ongoing_past_disasters
'''
Write this in modular format to return the list of links to the top 5 websites 
'''
client = openai.OpenAI(
    api_key=os.getenv("SWISSCOM_API"),
    base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
)
location="Switzerland"
sys_prompts = {
    "Summarize": "You are an Expert Summarizer. Summarize the following article in a concise manner, focusing on the key points and main ideas. Please ensure that you provide only the summary without any additional commentary or information. The output should be in the format Summary: \n\n",
    "Multilingual": "You are a Multilingual Translation Expert. Ensure that the translation is accurate and maintains the original meaning and tone of the article. Please provide the translated text without any additional commentary or information.\n\n",
    "SelectNews": f"You will be given a set of headlines for different news articles. You have to give 5 most relevant headlines depending on the factors like Geographic location of the user --{location}, the recency of the incident, global relevence. Choose the most appropriate headlines based on the disaster type. Please ensure that you provide only the selected headlines without any additional commentary or information. The output should only be 5 headlines, one on each line. DO NOT GIVE ANY ADDITIONAL INFORMATION.\n\n",
    "EstimateImpact": "Go through the following articles and then estimate the potential impact of the current disaster which can be helpful to the humanitarian aid organizations. The impact can be estimated in terms of number of people affected, budget required for response efforts, etc. Please ensure that you provide only the estimates without any additional commentary or information. The output should be in the format Impact: \n\n",
    "Insights": "You are given "
}

app = FastAPI()

# For your information, the different disaster data available to you is of cold wave, drought, earthquake, epidemic, Cyclone, fire, flood, heat wave, insect infestation, land slide, storm, snow avalanche, tsunami, volcano.

def get_ongoing_past_disasters(df):


    ongoing_disasters = []
    past_disasters = []
    links_map = {}

    for index, row in df.iterrows():
        if(row['status'] == 'Ongoing'):
            ongoing_disasters.append({
                'name': row['name'],
                'link': row['link'],
                'time': row['time']
            })
        elif(row['status'] == 'Past Disaster'):
            past_disasters.append({
                'name': row['name'],
                'link': row['link'],
                'time': row['time']
            })

        links_map[row['name']] = row['link']

    return ongoing_disasters, past_disasters, links_map

@app.get('/chatbot')
def generate_text(prompt, sys_msg):


    resp = client.chat.completions.create(
        model="swiss-ai/Apertus-70B",
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt}
        ],
    )

    return resp.choices[0].message.content

def get_system_prompt(task, language="English"):
    if (task == "Summarize"):
        return sys_prompts[task] + "Article: "
    elif (task == "Multilingual"):
        return sys_prompts[task] + f"Translate the article into {language}. " + "Article: "
    elif (task == "SelectNews"):
        return sys_prompts[task] + "Headlines: "
    else:
        print("Task not recognized")


# article = """
# Disaster description (Status: Bolivia entered its seasonal dry period (June to September), a period marked by heightened wildfire risk, particularly in the eastern and Amazonian regions. This risk is exacerbated by slash-and-burn agricultural practices ("chaqueo"), which often become uncontrolled and lead to large-scale fires. On 25 August, the Bolivian government convened a meeting with the diplomatic corps and international organizations to request support for wildfire response. The discussions included needs for equipment, humanitarian aid, and technical assistance to strengthen the national response. On 20 August 2025, the Bolivian government declared a national emergency through Supreme Decree No. 5447 in response to the escalating wildfire crisis. Santa Cruz and Beni have been identified as the most affected departments. (IFRC, 15 Sep 2025),
# """

# """During the night of 16-17 September 2025, heavy rains fell across most communes of the Nord-Ouest department, causing the Trois-Rivières River in Port-de-Paix to overflow suddenly. The floods resulted in extensive inundations across several neighborhoods in Port-de-Paix and Bassin-Bleu. According to the Directorate of Civil Protection, about 823 families were affected."""

# df = pd.read_csv('articles.csv')
# ongoing, past, links_map = get_ongoing_past_disasters(df)

# ongoing_headlines = [item['name'] for item in ongoing]

# heading_list = "\n".join(ongoing_headlines)
# out_headlines = generate_text("Current Disaster: " + article, get_system_prompt("SelectNews") + heading_list)
# relevant_headlines = [line.strip() for line in out_headlines.split("\n") if((line.strip() != '') and (line.strip() in links_map))]


# final_links = []
# for head in relevant_headlines:
#     final_links.append(links_map[head])

# final_links = list(set(final_links))[:5]
# print(final_links)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("swisscom_endpoint:app", host="0.0.0.0", port=8000, reload=True)