
import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from phase_2_rag.create_db import CreateDB
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
vec_db = CreateDB()
retriever = vec_db.vector_store.as_retriever(
        search_kwargs={"k" : 3}
    )

class OpenRouteLLM:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not self.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in .env")
        self.model_name= "openrouter"
        self.llm_client = ChatOpenAI(
            model="arcee-ai/trinity-mini:free",
            openai_api_key=self.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.9,
            streaming=True
        )

        self.prompt = PromptTemplate.from_template("""
Answer ONLY using the context below.
If the answer is not present, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""".strip())

        self.chain = (
            {
                "question": lambda x: x["question"],
                "context": lambda x: retriever.invoke(x["question"]),
            }
            | self.prompt
            | self.llm_client
        )

    # 🔹 Non-streaming
    def llm(self, question: str) -> str:
        response = self.chain.invoke({"question": question})
        return response.content

    # 🔹 Streaming
    import json

def stream(self, question: str):
    for chunk in self.chain.stream({"question": question}):
        if not chunk.content:
            continue

        # chunk.content is JSON text from OpenRouter
        data = json.loads(chunk.content)

        delta = data["choices"][0]["delta"]
        text = delta.get("content")

        if text:
            yield text

