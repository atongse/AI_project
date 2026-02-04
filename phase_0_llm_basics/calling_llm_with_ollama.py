import ollama, time


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        time_elasped = end - start
        print(f"TIME: {time_elasped:.2f}")
        return res
    return wrapper

@time_it
def chat_ollama(query):
    result = ollama.chat(
        model="gemma3",
        stream=False,
        messages=[{
            "role": "user",
            "content": query
                }]
    )
    return result

query = "what is the capital of India?"
res = chat_ollama(query)
print(res)