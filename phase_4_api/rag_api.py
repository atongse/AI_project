from fastapi import FastAPI
from pydantic import BaseModel
from phase_2_rag.call_llm import CallRag
from phase_2_rag.open_router_llm import OpenRouteLLM
from fastapi.responses import StreamingResponse

llm_open_router = OpenRouteLLM()
call_rag = CallRag()
app = FastAPI()

class RAGRequest(BaseModel):
    query: str

def stream_rag_answer(query:str):
    for chunk in call_rag.run_rag(query):
        yield chunk

@app.get("/")
def index():
    return {"app": "RAG"}

@app.post("/rag")
def get_answer(req: RAGRequest):
    ans = call_rag.run_rag(req.query)
    return {"answer": ans}

from fastapi.responses import StreamingResponse

@app.post("/rag/stream")
def rag_stream(req: RAGRequest):
    return StreamingResponse(
        call_rag.run_rag(req.query),
        media_type="text/plain"
    )

@app.post("/rag/open_router")
def open_router_llm(req:RAGRequest):
    answer = llm_open_router.llm(req.query)
    return {"answer": answer}

@app.post("/rag/open_router/stream")
def open_router_llm(req:RAGRequest):
    def token_generator():
        for chunk in llm_open_router.stream(req.query):
            yield chunk

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )