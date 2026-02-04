from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import OllamaLLM
from pydantic import Field, BaseModel


class CapitalResponse(BaseModel):
    country :str = Field(..., description="Name of the country")
    capital : str= Field(..., description="Name of the capital")

parser = PydanticOutputParser(pydantic_object=CapitalResponse)

prompt = ChatPromptTemplate.from_messages(
        [
        ( "system", "You are helpful assistant. Answer using specific JSON format. \n {format_instructions}"
         "If not, return a JSON object with country='UNKNOWN' and capital='UNKNOWN'. " ),
        ("user", "{query}")
        ]
    )

ollama_llm = OllamaLLM(model="gemma3", temperature=0.9)

chain = prompt | ollama_llm | parser
 
res = chain.invoke({"query" : "Capital of Jupiter?", "format_instructions" : parser.get_format_instructions() })


print(type(res))
print(res)