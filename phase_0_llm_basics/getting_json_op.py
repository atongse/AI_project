import ollama, json


SCHEMA = {
    "title" : "string",
    "summary" : "string",
    "keywords" : ["string"]
}
text = "LangChain is a framework for developing applications powered by language models. It enables chaining, tool use, memory, and retrieval."

result = ollama.chat(
    model="gemma3",
    stream=False,
    messages = [
    {
        "role": "system",
        "content": "You extract structured JSON only. No explanations."
    },
    {
        "role": "user",
        "content": f"""
        Return JSON strictly matching this schema:
        {json.dumps(SCHEMA, indent=2)}

        Text:
        {text}
        """
            }
        ],
    options={
        "temperature" : 0.9
    }

)

print(result.message.content)