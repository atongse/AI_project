import hashlib
import redis
import requests

class EmbeddingService:
    def __init__(self, model: str = "all-minilm"):
        self.model = model
        self.redis = redis.Redis(
            host="10.20.190.19",
            port=6379,
            decode_responses=False
        )

    def _key(self, text: str) -> str:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"embed:{self.model}:{h}"

    def _embed_one(self, text: str) -> list[float]:
        print("Embedding text length:", len(text))
        resp = requests.post(
            "http://127.0.0.1:11434/api/embeddings",
            json={
                "model": self.model,
                "prompt": text
            },
            timeout=120
        )
        print("Status:", resp.status_code, resp.text[:200])
        resp.raise_for_status()
        return resp.json()["embedding"]


    def embed(self, texts: list[str]) -> list[list[float]]:
        results = []

        for i, text in enumerate(texts):
            key = self._key(text)
            cached = self.redis.get(key)

            if cached:
                results.append(
                    list(map(float, cached.decode().split(",")))
                )
                continue

            print(f"Embedding {i+1}/{len(texts)}")
            vec = self._embed_one(text)
            self.redis.set(key, ",".join(map(str, vec)))
            results.append(vec)

        return results
