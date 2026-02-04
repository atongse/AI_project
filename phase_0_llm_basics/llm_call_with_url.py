import requests
url = "http://localhost:11434/api/generate"

payload = {
    "model" : "gemma3",
    "prompt" : "Give me 3 startup ideas using AI",
    "stream" : False
}

resp = requests.post(url, json=payload)
print(resp.json()["response"])




