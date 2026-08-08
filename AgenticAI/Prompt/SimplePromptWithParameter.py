import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

myText = """

You are interrecting with kids.

You are a {role}.

Use tone {tone}.

Explain {topic}.

Answer in short.
"""

prompt = PromptTemplate.from_template(myText)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

chain = prompt | llm

response = chain.invoke({"role": "teacher", "tone": "friendly", "topic": "AI RAG"})

print(response.content)
