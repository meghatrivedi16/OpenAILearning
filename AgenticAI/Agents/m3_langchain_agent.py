"""
LAB: Live Agent with yfinance
COURSE: Agentic AI Architecture (Module 3)
TEACHER: Manas Dasgupta

DESCRIPTION:
This version connects the agent to live market data using the yfinance SDK.
It uses LangChain's newer create_agent API instead of create_react_agent.

This version removes StreamlitCallbackHandler and adds simple diagnostics
so developers can understand when tools are being called.
"""

import streamlit as st
import datetime
import yfinance as yf
from dotenv import load_dotenv

# LangChain Imports
from langchain.agents import create_agent
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

# --- STEP 1: DEFINE LIVE TOOLS ---

@tool
def get_stock_price(ticker: str) -> str:
    """
    Retrieves the LIVE current stock price for a given ticker symbol.
    Examples: AAPL, TSLA, GOOGL, NVDA.
    Use this whenever you need up-to-date financial market data.
    """

    diagnostic_msg = f"TOOL CALL: get_stock_price(ticker='{ticker}')"
    print(diagnostic_msg)
    st.info(diagnostic_msg)

    try:
        stock = yf.Ticker(ticker)
        current_price = stock.fast_info["last_price"]

        result = f"The current live price of {ticker} is ${current_price:.2f}"

        print(f"TOOL RESULT: {result}")
        st.write(f"✅ Tool result: {result}")

        return result

    except Exception as e:
        error_msg = f"Error fetching live data for {ticker}: {e}"

        print(f"TOOL ERROR: {error_msg}")
        st.error(error_msg)

        return error_msg


@tool
def get_days_until_date(date_str: str) -> str:
    """
    Calculates the number of days from today until a future date.
    Input format must be YYYY-MM-DD.
    Example: 2027-12-31.
    """

    diagnostic_msg = f"TOOL CALL: get_days_until_date(date_str='{date_str}')"
    print(diagnostic_msg)
    st.info(diagnostic_msg)

    try:
        future = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (future - today).days

        result = f"There are {delta} days until {date_str}."

        print(f"TOOL RESULT: {result}")
        st.write(f"✅ Tool result: {result}")

        return result

    except Exception as e:
        error_msg = f"Error calculating days until date: {e}"

        print(f"TOOL ERROR: {error_msg}")
        st.error(error_msg)

        return error_msg


@tool
def calculate_growth(input_str: str) -> str:
    """
    Calculates simple growth.

    Input MUST be a comma-separated string:
    principal, rate, years

    Example:
    1500.50, 5, 10
    """

    diagnostic_msg = f"TOOL CALL: calculate_growth(input_str='{input_str}')"
    print(diagnostic_msg)
    st.info(diagnostic_msg)

    try:
        principal, rate, years = map(float, input_str.split(","))

        growth = principal * (1 + (rate / 100) * years)

        result = (
            f"A ${principal:.2f} investment at {rate}% over {years} years "
            f"grows to ${growth:.2f}."
        )

        print(f"TOOL RESULT: {result}")
        st.write(f"✅ Tool result: {result}")

        return result

    except Exception as e:
        error_msg = f"Input error. Use format 'principal, rate, years'. Details: {e}"

        print(f"TOOL ERROR: {error_msg}")
        st.error(error_msg)

        return error_msg


# Registry of live tools
tools = [
    get_stock_price,
    get_days_until_date,
    calculate_growth,
]

# --- STEP 2: AGENT SETUP ---

system_prompt = """
You are a financial assistant that can reason step-by-step and use tools.

You can:
- Fetch live stock prices.
- Calculate days until a future date.
- Calculate simple investment growth.

When the user asks a complex question, break it into tool-based steps.

Examples:
- If the user asks how much 10 shares of NVDA would be worth in 3 years at 12% growth:
  1. Fetch the live NVDA stock price.
  2. Multiply the price by 10.
  3. Use calculate_growth with principal, rate, and years.
  4. Explain the result clearly.

Before using a tool, briefly decide which tool is needed.
Always give a clear final answer.
Mention that market prices are live estimates from Yahoo Finance and may change.
"""

agent = create_agent(
    model="openai:gpt-4o",
    tools=tools,
    system_prompt=system_prompt,
)

# --- STEP 3: STREAMLIT INTERFACE ---

st.set_page_config(page_title="Live Agent Tool Orchestration", layout="wide")

st.title("Module 3: Live Agent Tool Orchestration")
st.markdown("### LangChain `create_agent` with Real-Time yfinance Data")

query = st.text_input(
    "Enter a complex query:",
    placeholder="How much would 10 shares of NVDA be worth in 3 years at 12% growth?",
)

if query:
    st.divider()
    st.subheader("Developer Diagnostics")

    st.write(f"🧑‍💻 User query received: `{query}`")
    print(f"USER QUERY: {query}")

    with st.spinner("Agent is reasoning and using tools if needed..."):

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
            config={
                "recursion_limit": 10,
            },
        )

    st.divider()
    st.subheader("Raw Agent Message Trace")

    for index, message in enumerate(response["messages"]):
        message_type = message.__class__.__name__

        st.markdown(f"#### Message {index + 1}: `{message_type}`")

        print(f"\nMESSAGE {index + 1}: {message_type}")
        print(message)

        if hasattr(message, "content"):
            st.write("Content:")
            st.code(message.content)

        if hasattr(message, "tool_calls") and message.tool_calls:
            st.write("Tool calls:")
            st.json(message.tool_calls)

        if hasattr(message, "name") and message.name:
            st.write(f"Tool name: `{message.name}`")

    st.divider()
    st.subheader("Final Result")

    final_message = response["messages"][-1]
    st.success(final_message.content)