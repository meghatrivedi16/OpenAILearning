# learning_advisor_agent.py - Defines the eLearning Program Advisor agent with tools for course details, cohort availability, discount calculation, and weather checking.
# This agent is designed to help learners choose the right course and cohort based on their questions and needs.

import os
from typing import Any, Dict

import httpx
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool


load_dotenv()

INTERNAL_API_BASE_URL = os.getenv(
    "INTERNAL_API_BASE_URL",
    "http://localhost:8001"
)


@function_tool
async def get_course_details(course_id: str) -> Dict[str, Any]:
    """
    Get course details from the internal eLearning course API.

    Args:
        course_id: Course identifier.
        Examples:
        - agentic-ai
        - responsible-genai
    """

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{INTERNAL_API_BASE_URL}/courses/{course_id}"
        )
        response.raise_for_status()
        return response.json()


@function_tool
async def get_course_cohorts(course_id: str) -> Dict[str, Any]:
    """
    Get available cohorts for a course from the internal eLearning API.

    Args:
        course_id: Course identifier.
        Examples:
        - agentic-ai
        - responsible-genai
    """

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{INTERNAL_API_BASE_URL}/courses/{course_id}/cohorts"
        )
        response.raise_for_status()
        return response.json()


@function_tool
async def calculate_course_discount(
    course_id: str,
    learner_type: str
) -> Dict[str, Any]:
    """
    Calculate the learner's discount and final course price.

    Args:
        course_id: Course identifier.
        learner_type: Type of learner.
        Examples:
        - student
        - corporate
        - early-bird
        - general
    """

    payload = {
        "course_id": course_id,
        "learner_type": learner_type
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{INTERNAL_API_BASE_URL}/discount",
            json=payload
        )
        response.raise_for_status()
        return response.json()


@function_tool
async def get_weather_for_city(city: str) -> Dict[str, Any]:
    """
    Get current weather for a city using an external public weather API.

    Args:
        city: City name.
        Examples:
        - Bangalore
        - Mumbai
        - Delhi
    """

    async with httpx.AsyncClient(timeout=10) as client:
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "city": city,
                "error": "City not found"
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,precipitation,wind_speed_10m"
            }
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        return {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": weather_data.get("current", {})
        }


learning_advisor_agent = Agent(
    name="eLearning Program Advisor",
    instructions="""
You are an eLearning program advisor.

Your job is to help learners choose the right course and cohort.

You have access to tools for:
- Course details
- Cohort availability
- Discount calculation
- Weather check for in-person cohorts

Important behavior rules:

1. Use tools whenever the learner asks about:
   - Course information
   - Course price
   - Discounts
   - Cohort availability
   - Seat availability
   - City or weather suitability

2. Do not invent:
   - Prices
   - Dates
   - Seat counts
   - Weather conditions
   - Course duration
   - Course mode

3. Course ID inference:
   - If the learner says "Agentic AI", "AI agents", "agents course",
     "agent course", or "Agentic AI Foundations",
     use course_id = "agentic-ai".

   - If the learner says "Responsible GenAI", "Responsible Generative AI",
     "AI governance", "guardrails", or "AI safety",
     use course_id = "responsible-genai".

4. Learner type inference:
   - If the learner says "student", use learner_type = "student".
   - If the learner says "corporate", "working professional",
     "company sponsored", or "employee", use learner_type = "corporate".
   - If the learner says "early bird", use learner_type = "early-bird".
   - If learner type is unclear, use learner_type = "general".

5. Weather handling:
   - Only call the weather tool if the learner mentions a city,
     in-person attendance, travel, or asks whether conditions are suitable.
   - If the cohort is online, do not over-emphasize weather.

6. Response style:
   - Be concise, practical, and learner-friendly.
   - Summarize the useful facts from the tools.
   - Give a clear recommendation.
   - Mention uncertainty where relevant.
   - Do not expose raw JSON unless the learner asks for technical details.

7. Final answer structure:
   Use this format when appropriate:

   Course:
   Cohort availability:
   Price:
   Weather / location note:
   Recommendation:
""",
    tools=[
        get_course_details,
        get_course_cohorts,
        calculate_course_discount,
        get_weather_for_city,
    ],
)


async def ask_learning_advisor(user_question: str) -> str:
    """
    Reusable function called by the FastAPI wrapper.

    This function receives the learner's question from the API layer,
    runs the OpenAI Agent, allows the Agent to call tools as needed,
    and returns the final response.
    """

    result = await Runner.run(
        learning_advisor_agent,
        user_question
    )

    return result.final_output