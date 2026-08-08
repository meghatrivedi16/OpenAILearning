"""Notes Manager (MySQL-backed) MCP server

Purpose:
 - Provides a small MCP (FastMCP) service that persists notes to a MySQL
     database. Exposes tools for create/update/search/delete and resources
     for fetching notes as JSON.

Example requests (command-line):
 - Health check: `curl http://localhost:8005/health`

Sample Usage prompts (Client Side):
 - "Create a new note titled 'Project Roadmap' about our Q1 goals with the tag 'work'."
 - "Search my notes for any mentions of 'database migration'."
 - "Retrieve the full details of note_be31754a."
 - "Update note_be31754a to add the tag 'urgent'."
 - "Delete note_be31754a from my notes."
 - "Get all my notes as a JSON list."

"""

import json
import os
from fastmcp import FastMCP
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
from starlette.responses import PlainTextResponse
# In-process TTL cache (simple single-process cache). Install with:
# pip install cachetools
from cachetools import TTLCache

# Load DB credentials
load_dotenv()

# Cache namespace: keys used below are 'notes:all' and 'notes:{note_id}'
_cache = TTLCache(maxsize=1024, ttl=60)  # 60 second TTL

# Initialize MCP
mcp = FastMCP(name="Notes_Manager_MySQL")

# ============================================
# DATABASE UTILITIES
# ============================================

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# ============================================
# HEALTH CHECK
# ============================================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return PlainTextResponse("OK")

# ============================================
# TOOLS - Persistent Actions
# ============================================

@mcp.tool
def create_note(title: str, content: str, tags: list[str] = None) -> dict:
    """Create a new note and persist it to MySQL."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Generate a unique string ID similar to your previous format
    import uuid
    note_uuid = f"note_{str(uuid.uuid4())[:8]}"
    tags_json = json.dumps(tags or [])
    
    query = "INSERT INTO notes (note_uuid, title, content, tags) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (note_uuid, title, content, tags_json))
    conn.commit()
    # Invalidate relevant cache entries after a write
    _cache.pop("notes:all", None)
    _cache.pop(f"notes:{note_uuid}", None)

    cursor.execute("SELECT * FROM notes WHERE note_uuid = %s", (note_uuid,))
    note = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return {"success": True, "note": note}

@mcp.tool
def update_note(note_id: str, title: str = None, content: str = None, tags: list[str] = None) -> dict:
    """Update a note in MySQL. Only provided fields are changed."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    updates = []
    params = []
    
    if title:
        updates.append("title = %s")
        params.append(title)
    if content:
        updates.append("content = %s")
        params.append(content)
    if tags:
        updates.append("tags = %s")
        params.append(json.dumps(tags))
        
    if not updates:
        return {"success": False, "error": "No updates provided"}
    
    query = f"UPDATE notes SET {', '.join(updates)} WHERE note_uuid = %s"
    params.append(note_id)
    
    cursor.execute(query, tuple(params))
    conn.commit()
    # Invalidate cache for this note and the all-notes listing
    _cache.pop("notes:all", None)
    _cache.pop(f"notes:{note_id}", None)

    cursor.execute("SELECT * FROM notes WHERE note_uuid = %s", (note_id,))
    note = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return {"success": True, "note": note}

@mcp.tool
def search_notes(query: str) -> dict:
    """Search notes in database by title, content, or tags."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT * FROM notes 
        WHERE title LIKE %s 
        OR content LIKE %s 
        OR JSON_CONTAINS(tags, JSON_QUOTE(%s))
    """
    search_term = f"%{query}%"
    cursor.execute(sql, (search_term, search_term, query))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"query": query, "count": len(results), "results": results}

@mcp.tool
def delete_note(note_id: str) -> dict:
    """Delete a note from MySQL by its UUID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM notes WHERE note_uuid = %s", (note_id,))
    conn.commit()
    affected = cursor.rowcount
    # Invalidate cache after deletion
    _cache.pop("notes:all", None)
    _cache.pop(f"notes:{note_id}", None)
    cursor.close()
    conn.close()
    return {"success": affected > 0, "deleted_id": note_id}

# ============================================
# RESOURCES - Dynamic Data
# ============================================

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """Get all notes as a JSON string from the database."""
    # Try cache first
    cached = _cache.get("notes:all")
    if cached is not None:
        return cached
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    notes_json = json.dumps(notes, default=str, indent=2)
    _cache["notes:all"] = notes_json
    return notes_json

@mcp.resource("notes://note/{note_id}")
def get_note_by_id(note_id: str) -> str:
    """Fetch a specific note from MySQL."""
    # Try cache first
    key = f"notes:{note_id}"
    cached = _cache.get(key)
    if cached is not None:
        return cached

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE note_uuid = %s", (note_id,))
    note = cursor.fetchone()
    cursor.close()
    conn.close()
    if not note:
        return "Note not found"
    note_json = json.dumps(note, default=str, indent=2)
    _cache[key] = note_json
    return note_json

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    print("Starting MySQL-Backed Notes Manager MCP Server...")
    # mcp.run(transport="http", port=8005)    
    mcp.run(transport="streamable-http", port=8005)
    print("Server is running on port 8005")
    
    