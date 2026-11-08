import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  

model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
print("Testing model:", model_name)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),)

response = client.models.generate_content(
    model=model_name,
    contents="Say hello to Farzaneh in one short, friendly sentence.",
)

print(response.text)