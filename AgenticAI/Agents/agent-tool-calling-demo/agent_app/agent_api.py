# agent_api.py - FastAPI backend for the eLearning Tool Calling Agent demo
# This API serves as the backend for the frontend interface, allowing users to ask questions to the learning advisor agent.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_app.learning_advisor_agent import ask_learning_advisor


app = FastAPI(
    title="eLearning Tool Calling Agent API",
    description="Frontend API wrapper for the OpenAI Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local demo. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AdvisorRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {
        "message": "eLearning Tool Calling Agent API is running"
    }


@app.post("/ask-advisor")
async def ask_advisor(request: AdvisorRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        answer = await ask_learning_advisor(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )