
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from phase_2_rag.create_db import CreateDB
class CallRag:
    vec_db = CreateDB()
    retriever = vec_db.vector_store.as_retriever(
        search_kwargs={"k" : 3}
    )

    def run_rag(self, question):
        llm = OllamaLLM(model="gemma3", temperature=0)

        prompt = PromptTemplate.from_template(
            """
        Answer ONLY using the context below.
        If the answer is not present, say:
        "I don't know based on the provided documents."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """.strip()
        )


        rag_chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
        )

        for chunk in rag_chain.stream(question):
            if isinstance(chunk, str):
                yield chunk
            elif hasattr(chunk, "content"):           
                yield chunk.content


