
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

myText = """What is RAG?"""

prompt = PromptTemplate.from_template(myText)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

chain = prompt | llm

response = chain.invoke({})

print(response.content)


