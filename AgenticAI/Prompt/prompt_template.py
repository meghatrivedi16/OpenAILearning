from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# 1. Create the prompt template
prompt = PromptTemplate.from_template(
    """
    You are a {role}.

    Explain the topic: {topic}

    Use a {tone} tone.
    Keep the answer suitable for {audience}. Keep the answer within 250 words.
    """
)

# 2. Instantiate the LLM object
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)  # Adjust parameters as needed

# 3. Create the chain (LCEL - LangChain Expression Language chains runnables in LangChain) by combining the prompt and the LLM
chain = prompt | llm

# 4. Run the chain with dynamic values
response = chain.invoke({
    "role": "teacher",
    "topic": "dynamic prompting in LangChain",
    "tone": "simple and beginner-friendly",
    "audience": "new Python learners"
})

print(response.content)