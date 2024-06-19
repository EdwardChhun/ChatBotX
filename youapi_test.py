import os
import json
import requests 
from dotenv import load_dotenv

load_dotenv()

YOU_API_KEY = os.getenv("YOU_API_KEY")
if not YOU_API_KEY:
    print("API Key isn't present")

def get_ai_snippets_for_query():
    query = input("Type in query: ")
    headers = {"X-API-Key": YOU_API_KEY}
    params = {"query": query}
    return requests.get(
        f"https://api.ydc-index.io/search?query={query}",
        params=params,
        headers=headers,
    ).json()
    
results = get_ai_snippets_for_query()

with open('result.json', 'w') as file:
    json.dump(results, file, indent=4)
    
print("written results into file")