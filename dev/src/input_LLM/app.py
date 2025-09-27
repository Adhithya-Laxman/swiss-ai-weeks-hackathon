# app.py - Flask backend for Disaster Management Chatbot with Firebase and Apertus API

from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import openai
import json
import firebase_admin
from firebase_admin import credentials, db
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# --- Firebase setup ---
firebase_initialized = False
try:
    cred = credentials.Certificate('swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json')  # Path to the downloaded JSON
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://swiss-ai-hack-default-rtdb.firebaseio.com'
    })
    firebase_initialized = True
    print("✅ Firebase initialized successfully")
except Exception as e:
    print(f"⚠️  Firebase initialization failed: {e}")
    print("   App will run with in-memory storage (data will not persist)")
    firebase_initialized = False

# In-memory storage fallback
in_memory_chats = {}

# --- Swisscom/Apertus API setup ---
api_key = os.getenv("SWISSCOM_API")
if api_key:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
    )
    print("✅ Apertus API client initialized successfully")
else:
    client = None
    print("⚠️  SWISSCOM_API not set - API calls will fail")

# Sample JSON context (from your query) - in production, load dynamically
DISASTER_CONTEXT = [
  {
    "SECTION_TITLE": "Ebola Outbreak in Democratic Republic of Congo",
    "SECTION_CONTENT": "Health authorities in the Democratic Republic of Congo have declared an outbreak of Ebola virus disease in Kasai Province. 28 suspected cases and 15 deaths, including four health workers, have been reported. The outbreak has affected Bulape and Mweka health zones, where officials are conducting investigations. The cause of the outbreak has been confirmed to be the Ebola Zaire strain.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "Estimated $10-30 million for immediate relief efforts such as medical supplies, emergency food and water, and support for health workers",
    "TIME_OF_OCCURENCE": "4 September 2025"
  },
  {
    "SECTION_TITLE": "Flash Floods Devastate Sierra Leone: A Marathon of Relief and Recovery in Progress",
    "SECTION_CONTENT": "Between August 31 and September 5, 2025, Sierra Leone experienced devastating flash floods across 17 communities in seven districts. Over 11,080 people from more than 2,216 households were affected, with over 4,000 displaced and seeking shelter in schools or with host families. Homes, buildings, and critical infrastructure including schools and health facilities were damaged or destroyed, and more than 2,500 hectares of farmland were submerged. United Methodist Church's WNCC Disaster Ministries is currently (10.8.24) in the Relief phase, where critical supplies and Early Response Teams are being mobilized. This phase is demanding but vital in bridging the gap between chaos and recovery, and it requires significant support. Recovery is expected to take years, and long-term support will be needed for rebuilding homes and communities. Initial estimates for relief and recovery could be in the millions of dollars. The exact amount is not provided but based on similar disaster relief costs, it could be in the range of $5 to $10 million or more.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "5000000",
    "TIME_OF_OCCURENCE": "September 2025"
  },
  {
    "SECTION_TITLE": "Afghan Earthquake - Rescue, Relief, and Recovery",
    "SECTION_CONTENT": "On 31 August 2025 at 23.47 local time, a 6+ magnitude earthquake struck Afghanistan's Nangarhar Province near the Pakistan border, significantly impacting communities in four provinces - Kunar, Laghman, Nangarhar, and Nuristan. The initial quake felt in neighboring provinces. The epicenter was located 30 km northeast of Jalalabad, with hypocenter at 8-10 km deep, exacerbating the disaster's effect. Casualty figures have steadily grown to at least 800 deaths, 2,000 injuries, and 12,000 directly affected individuals, with numbers expected to rise as affected areas are accessed. Rescue efforts are ongoing, with initial findings indicating widespread and severe needs across 25 inter-agency assessment teams. Immediate relief efforts are underway with over 2,000 people killed, 3,100 injured, and 5,400 homes destroyed. An updated emergency response plan aims to assist 457,000 people in high-risk areas including women, children, and displaced persons. The crisis is compounded by terrain difficulty and remote access.",
    "CLASSIFICATION": "Relief and Recovery",
    "PREDICTED_COST": 139600000,
    "TIME_OF_OCCURENCE": "31 August 2025"
  },
  {
    "SECTION_TITLE": "Southern Yemen Flooding - Response Overview",
    "SECTION_CONTENT": "Severe flooding caused by torrential rains has affected 100,000 people in Yemen, destroying homes and critical infrastructure. The International Rescue Committee (IRC) and other humanitarian organizations are mounting urgent response efforts. The crisis has led to the displacement of thousands, especially internally displaced people (IDPs). To effectively respond, efforts will focus on immediate rescue and then shift to relief efforts to provide essential services like food, water, shelter, and medical aid. Long-term recovery plans will require significant investment to rebuild homes, infrastructure, and agriculture. Protection risks, disease outbreaks, and further flooding due to additional heavy rain pose serious challenges.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "Estimated cost for the relief efforts could be in the range of $10-15 million. However, this is a preliminary estimation and the actual cost could be higher due to the scale and complexity of the disaster and the ongoing needs of the affected population. Rebuilding and recovery efforts could require a significantly higher investment over the longer term.",
    "TIME_OF_OCCURENCE": "August 2025"
  },
  {
    "SECTION_TITLE": "Ebola Outbreak in Democratic Republic of the Congo",
    "SECTION_CONTENT": "Health authorities in the Democratic Republic of the Congo have declared an outbreak of Ebola virus disease in Kasai Province where 28 suspected cases and 15 deaths have been reported. This outbreak, confirmed to be caused by Ebola Zaire, has affected Bulape and Mweka health zones and been declared on September 4, 2025. Health officials are carrying out investigations and providing necessary assistance.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "Estimated to be upwards of $20 million for immediate relief efforts, including provision of medical supplies, equipment, staff deployment, community public health education, and support to affected communities. Further costs may be required for long-term recovery efforts and mitigation depending on the spread and severity of the outbreak.",
    "TIME_OF_OCCURENCE": "September 4, 2025"
  },
  {
    "SECTION_TITLE": "Flash Floods in Sierra Leone: A Disaster Classification & Estimated Cost",
    "SECTION_CONTENT": "Between 31 August and 5 September 2025, Sierra Leone witnessed a series of devastating flash floods affecting 17 communities in seven districts. The floods have impacted over 11,080 people from more than 2,216 households, displacing 4,000 people. Homes, schools, and critical infrastructure like health facilities were damaged or destroyed, and over 2,500 hectares of farmland submerged, affecting livelihoods and food security. Since late August, the relief phase has started with efforts to provide essential needs, but with thousands displaced and infrastructure damaged, comprehensive recovery plans are needed for years to come. The estimated cost for relief and recovery could range from millions to tens of millions of dollars, depending on the extent of damage, the speed of recovery, and the resilience of the affected communities. This ongoing disaster therefore falls under the Relief phase, with recovery phase efforts anticipated to last several years. It is likely that these amounts will rise over time due to further assessments.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "Estimated between $100M to $500M (as a rough preliminary figure, subject to detailed assessments)",
    "TIME_OF_OCCURENCE": "Late August 2025"
  },
  {
    "SECTION_TITLE": "Earthquake in Nangarhar Province, Afghanistan",
    "SECTION_CONTENT": "On 31 August 2025 at 23:47 local time, a 6+ magnitude earthquake struck Afghanistan’s Nangarhar Province near the Pakistan border, with the most affected areas identified as Kunar Province, Laghman Province, Nangarhar Province, and Nuristan Province. The humanitarian impact is severe, with over 2,000 people injured and 6,000 homes destroyed or damaged. Initial figures indicate up to 12,000 people are directly affected, with damage also reported in Chawkay and Nurgal districts in Kunar Province, Dara-e-Nur district in Nangarhar Province, among others. As additional quakes and aftershocks have also occurred since, the casualty figures are expected to rise as search and rescue teams reach affected areas. Humanitarian response and assessment are ongoing, with initial estimates indicating up to 497,000 people affected and significant need for shelter, food, water, and medical assistance. The actual number of people affected and relief needs are expected to increase as further assessments are completed.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": "Estimated US$100 million for relief efforts, which could rise based on the full scale of damage, reach of humanitarian assessments, and ongoing risk from further aftershocks and quakes.",
    "TIME_OF_OCCURENCE": "31 August 2025"
  },
  {
    "SECTION_TITLE": "Bolivia Wildfires: Relief Phase Initiated",
    "SECTION_CONTENT": "Bolivia faces heightened wildfire risk during its seasonal dry period, particularly in the eastern and Amazonian regions. The risk is exacerbated by slash-and-burn agricultural practices. After declaring a national emergency through Supreme Decree No. 5447 on 20 August 2025, the Bolivian government requested international support for wildfire response on 25 August. This support includes equipment, humanitarian aid, and technical assistance, especially in the most affected departments of Santa Cruz and Beni. This response falls under the Relief phase, with the focus being on immediate needs and stabilization efforts to prevent further damage.",
    "CLASSIFICATION": "Relief",
    "PREDICTED_COST": {
      "equipment": 500000,
      "humanitarian_aid": 1000000,
      "technical_assistance": 200000
    },
    "TIME_OF_OCCURENCE": "August 2025"
  }
]


# Chat storage functions (Firebase with in-memory fallback)
def append_message_to_firebase(chat_id, input_text, output_text):
    if firebase_initialized:
        try:
            ref = db.reference(f'chats/{chat_id}')
            ts = int(time.time() * 1000)
            ref.child(str(ts)).set({
                'input': input_text,
                'output': output_text,
                'timestamp': ts
            })
            return True
        except Exception as e:
            print(f"Error saving to Firebase: {e}")
            print("Falling back to in-memory storage")
    
    # Fallback to in-memory storage
    if chat_id not in in_memory_chats:
        in_memory_chats[chat_id] = []
    
    ts = int(time.time() * 1000)
    in_memory_chats[chat_id].append({
        'input': input_text,
        'output': output_text,
        'timestamp': ts
    })
    return True


def get_chat_history(chat_id):
    if firebase_initialized:
        try:
            ref = db.reference(f'chats/{chat_id}')
            data = ref.order_by_key().get()
            if data:
                # Convert to list and sort by timestamp
                messages = []
                for key, value in data.items():
                    if isinstance(value, dict) and 'input' in value and 'output' in value:
                        messages.append(value)
                # Sort by timestamp if available, otherwise by key
                messages.sort(key=lambda x: x.get('timestamp', int(key)))
                return messages
            return []
        except Exception as e:
            print(f"Error retrieving from Firebase: {e}")
            print("Falling back to in-memory storage")
    
    # Fallback to in-memory storage
    if chat_id in in_memory_chats:
        return sorted(in_memory_chats[chat_id], key=lambda x: x.get('timestamp', 0))
    return []


# Flask routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', context=json.dumps(DISASTER_CONTEXT))

@app.route('/game')
def game():
    return render_template('game.html', context=json.dumps(DISASTER_CONTEXT))

@app.route('/game-chatbot')
def game_chatbot():
    # Get disaster context from URL parameters
    disaster_title = request.args.get('disaster', '')
    disaster_context = request.args.get('context', '')
    
    # Find matching disaster from our context
    selected_disaster = None
    if disaster_title:
        for disaster in DISASTER_CONTEXT:
            if disaster_title.lower() in disaster['SECTION_TITLE'].lower():
                selected_disaster = disaster
                break
    
    return render_template('game_chatbot.html', 
                         context=json.dumps(DISASTER_CONTEXT),
                         selected_disaster=json.dumps(selected_disaster) if selected_disaster else None,
                         disaster_title=disaster_title,
                         disaster_context=disaster_context)


@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.json
        chat_id = data.get('chat_id', 'default_chat')
        msg = data.get('message', '').strip()
        
        if not msg:
            return jsonify({'response': 'Please enter a message.', 'error': True})

        # Get chat history as context for LLM
        history = get_chat_history(chat_id)
        formatted_history = "\n".join([f"User: {m['input']}\nAssistant: {m['output']}" for m in history])

        # Compose prompt for LLM with previous chat and disaster context
        system_prompt = """You are a helpful disaster management assistant. You have access to information about various disasters and can help with:
        - Disaster response planning
        - Relief efforts coordination
        - Resource allocation
        - Emergency protocols
        - Recovery strategies
        
        Use the provided disaster context information to give accurate and helpful responses.
        
        IMPORTANT: Format your responses using markdown for better readability:
        - Use **bold** for important terms and disaster names
        - Use ### for section headers
        - Use numbered lists (1., 2., 3.) for multiple items
        - Use bullet points (- or •) for sub-items
        - Use *italics* for emphasis
        - Structure information clearly with proper formatting"""
        
        # Include disaster context in the prompt
        context_info = "\n".join([f"Disaster: {item['SECTION_TITLE']}\nDetails: {item['SECTION_CONTENT']}\nClassification: {item['CLASSIFICATION']}\nCost: {item['PREDICTED_COST']}\nTime: {item['TIME_OF_OCCURENCE']}\n" for item in DISASTER_CONTEXT])
        
        full_prompt = f"Disaster Context Information:\n{context_info}\n\nChat history:\n{formatted_history}\n\nUser: {msg}"

        # Call the Apertus API via OpenAI client
        if client is None:
            out = "Sorry, the AI service is not available. Please set the SWISSCOM_API environment variable to enable AI responses."
        else:
            try:
                resp = client.chat.completions.create(
                    model="swiss-ai/Apertus-70B",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                out = resp.choices[0].message.content
            except Exception as e:
                print(f"API Error: {e}")  # Debug logging
                if "401" in str(e) or "Unauthorized" in str(e):
                    out = "Sorry, the API key is invalid. Please check your SWISSCOM_API environment variable."
                elif "404" in str(e) or "Not Found" in str(e):
                    out = "Sorry, the Apertus model endpoint is not available. Please check the API configuration."
                else:
                    out = f"Sorry, there was an error with the AI service: {str(e)}"

        # Save new user and model messages to Firebase
        save_success = append_message_to_firebase(chat_id, msg, out)
        if not save_success:
            print("Warning: Failed to save message to Firebase")

        return jsonify({'response': out, 'error': False})
        
    except Exception as e:
        print(f"Error in chat_api: {e}")
        return jsonify({'response': f'Sorry, there was an error processing your request: {str(e)}', 'error': True})


if __name__ == '__main__':
    app.run(debug=True)
