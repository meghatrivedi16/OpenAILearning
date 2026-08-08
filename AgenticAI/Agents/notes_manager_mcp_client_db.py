"""
Notes Manager MCP Server (MySQL Persistent Version)
==================================================

Testing
-------
- MCP Inspector: Use the Inspector to interactively test tools and resources at http://localhost:5173.
- Docker Health Checks: Verify server responsiveness via the dedicated endpoint at http://localhost:8005/health.
- CLI Testing: Use an async CLI client to run 'search_notes' or 'get_all_notes' via stdio transport.

Core Features
-------------
- Tools: Action-oriented functions to create, update, delete, and search notes directly in the MySQL database.
- Resources: Dynamic data access for all notes (notes://all) or specific IDs (notes://note/{note_id}).
- Health Check: A custom /health route to satisfy Docker orchestrators without requiring full MCP protocol handshakes.

Sample AI Prompts (Client Side)
------------------------------
- "Create a new note titled 'Project Roadmap' about our Q1 goals with the tag 'work'."
- "Search my notes for any mentions of 'database migration'."
- "Retrieve the full details of note_be31754a."

Error Conditions & Handling
---------------------------
- 401 Authentication Error: Occurs if the 'OPENAI_API_KEY' is missing in the client-side environment.
- 400/406 Protocol Errors: Triggered if standard HTTP 'GET' requests hit the /mcp endpoint instead of the required SSE handshake.
- Connection Errors: Happens if the MySQL server is unreachable or credentials in the .env file are incorrect.
"""

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Configuration
api_key = os.getenv("OPENAI_API_KEY")
server_url = "https://rachell-semimagnetic-gaylene.ngrok-free.dev"  # ngrok URL for local testing

# Initialize synchronous OpenAI client
client = OpenAI(api_key=api_key) if api_key else None

def call_mcp(prompt: str) -> str:
    """
    Sends a prompt to OpenAI synchronously with the Notes Manager MCP server attached as a tool.
    """
    if not client:
        raise RuntimeError("OpenAI client not configured (OPENAI_API_KEY missing).")

    try:
        resp = client.responses.create(
            model="gpt-4o",
            tools=[
                {
                    "type": "mcp",
                    "server_label": "Notes_Manager_MySQL",
                    "server_url": f"{server_url}/mcp",
                    "require_approval": "never",
                },
            ],
            input=prompt,
        )
        return resp.output_text
    except Exception as e:
        return f"Error executing MCP call: {str(e)}"

# ============================================
# MAIN ASYNC LOOP
# ============================================
def main():
    print(f"--- MCP Client Connected to {server_url} ---")

    # Example: Run requests sequentially using the synchronous client
    prompts = [
        #"Create a note titled 'Collection Task 5' with content 'Project Data 5 Collection'.",
        "List all unique tags in my notes system.",
        # "Create a new note titled 'Project Brief' about some sample Project initiation details with the tag 'project'.",
        # "Search my notes for any mentions of 'Collection'.",
        # "Retrieve the full details of note_2170b0ed.",
        # "Update note_2170b0ed to add the tag 'urgent'.",
        #"Delete note_a6469a37 from my notes.",
        #"Get all my notes as a JSON list.",
    ]

    for i, p in enumerate(prompts, start=1):
        result = call_mcp(p)
        print(f"Result {i}: {result}")


if __name__ == "__main__":
    main()