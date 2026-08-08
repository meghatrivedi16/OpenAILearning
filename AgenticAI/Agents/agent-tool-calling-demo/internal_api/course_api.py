# This is a simple FastAPI application that serves as an internal API for an eLearning platform.
# It provides endpoints to retrieve course details, cohort information, and calculate discounts based on learner type

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Internal eLearning Course API")


COURSES = {
    "agentic-ai": {
        "course_id": "agentic-ai",
        "title": "Agentic AI Foundations",
        "duration": "6 weeks",
        "mode": "hybrid",
        "base_price_inr": 18000,
        "description": "Learn agents, tools, planning, memory, tracing, and deployment patterns."
    },
    "responsible-genai": {
        "course_id": "responsible-genai",
        "title": "Responsible Generative AI",
        "duration": "4 weeks",
        "mode": "online",
        "base_price_inr": 12000,
        "description": "Learn AI safety, privacy, guardrails, governance, and human review."
    }
}


COHORTS = {
    "agentic-ai": [
        {
            "cohort_id": "AGAI-WE-001",
            "schedule": "Weekend",
            "start_date": "2026-07-11",
            "city": "Bangalore",
            "available_seats": 8
        },
        {
            "cohort_id": "AGAI-WD-002",
            "schedule": "Weekday Evening",
            "start_date": "2026-07-15",
            "city": "Online",
            "available_seats": 20
        }
    ],
    "responsible-genai": [
        {
            "cohort_id": "RGAI-WE-001",
            "schedule": "Weekend",
            "start_date": "2026-07-06",
            "city": "Online",
            "available_seats": 15
        }
    ]
}


class DiscountRequest(BaseModel):
    course_id: str
    learner_type: str


@app.get("/")
def root():
    return {"message": "Internal Course API is running"}


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    course = COURSES.get(course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.get("/courses/{course_id}/cohorts")
def get_cohorts(course_id: str):
    cohorts = COHORTS.get(course_id)

    if not cohorts:
        raise HTTPException(status_code=404, detail="No cohorts found")

    return {
        "course_id": course_id,
        "cohorts": cohorts
    }


@app.post("/discount")
def calculate_discount(request: DiscountRequest):
    course = COURSES.get(request.course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    learner_type = request.learner_type.lower()

    discount_percent = 0

    if learner_type == "student":
        discount_percent = 20
    elif learner_type == "corporate":
        discount_percent = 10
    elif learner_type == "early-bird":
        discount_percent = 15

    base_price = course["base_price_inr"]
    final_price = base_price - ((base_price * discount_percent) / 100)

    return {
        "course_id": request.course_id,
        "base_price_inr": base_price,
        "learner_type": request.learner_type,
        "discount_percent": discount_percent,
        "final_price_inr": final_price
    }