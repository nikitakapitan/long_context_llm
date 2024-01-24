import requests
import json

def query_llm(prompt, endpoint):
    payload = json.dumps({
        "prompt": prompt,
        "max_new_tokens": 4096,
        "top_p": 0.95,
        "temperature": 0.7,
        "repetition_penalty": 1.15,
        "do_sample": True,
        "key": "API_KEY"
    })
    headers = {
        'key': '******',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    return response.text