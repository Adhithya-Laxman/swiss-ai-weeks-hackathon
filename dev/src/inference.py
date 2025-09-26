from transformers import AutoTokenizer, AutoModelForCausalLM
# from huggingface_hub import login

access_token = ""
# login(token=access_token)
model_name = "swiss-ai/Apertus-8B-2509"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, token=access_token)

def generate_text(prompt):
    # Manually format the prompt for models without chat_template
    text = f"User: {prompt}\nAssistant:"
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Generate the output
    generated_ids = model.generate(**model_inputs, max_new_tokens=256)

    # Get and decode the output
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :]
    result = tokenizer.decode(output_ids, skip_special_tokens=True)
    return result

def get_news_article(article_folder):
    


def get_input(news_article):



    input = news_article + ""

def get_prompt(article_type):

# summarize, multilingual, scale of impact, 


def get_support_type(news_article):


