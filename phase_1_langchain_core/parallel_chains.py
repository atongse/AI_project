from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableParallel

llm = OllamaLLM(model="gemma3", temperature=0)

answer = ChatPromptTemplate.from_template(
    "Answer the question: \n{query}"
)

explain = ChatPromptTemplate.from_template(
    "Explain the reasoning in two steps: \n{query}"
)

parallel = RunnableParallel(
    answer = answer | llm,
    explaination = explain | llm
)

res = parallel.invoke({"query":"what is capital of India"})
