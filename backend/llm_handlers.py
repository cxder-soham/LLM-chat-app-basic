import openai
from dotenv import load_dotenv
import google.generativeai as genai
import os
from openai import OpenAI
import json
import requests


def call_openai(prompt):
    try:
        # response = openai.completions.create(
        #     model="gpt-3.5-turbo",  # Updated model name
        #     prompt=prompt,
        #     max_tokens=150
        # )
        # return response.choices[0].text.strip()
        load_dotenv()
        client = OpenAI()

        openai.api_key = os.getenv('OPENAI_API_KEY')

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt
                }
            ], max_tokens=150
        )
        return completion.choices[0].message

    except Exception as e:
        return f"OpenAI Error: {e}"


def call_gemini(prompt):
    try:
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def call_llama(prompt):
    try:
        load_dotenv()
        API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
        payload = {	"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.text
                  

    except Exception as e:
        return f"Error: {e}"