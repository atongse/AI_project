import hashlib

PROMPT_VERSION = "v1"   # bump this manually when prompt changes

def llm_cache_key(query: str, model: str):
    payload = f"{model}|{PROMPT_VERSION}|{query}"
    return hashlib.sha256(payload.encode()).hexdigest()
