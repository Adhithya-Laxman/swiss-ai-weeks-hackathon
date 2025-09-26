from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("swiss-ai/Apertus-8B-2509")
model = AutoModelForCausalLM.from_pretrained("swiss-ai/Apertus-8B-2509")

def generate_text(prompt):

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_news_article(article_folder):



def get_input(news_article):



    input = news_article + ""

def get_prompt(article_type):

# summarize, multilingual, scale of impact, 


def get_support_type(news_article):


