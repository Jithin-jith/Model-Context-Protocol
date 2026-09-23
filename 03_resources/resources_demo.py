"""
Module 03: MCP Resources - Demo Implementation
==============================================
This script demonstrates:
1. Static resource definition (`config://app_settings`).
2. Dynamic resource template URI matching (`sqlite://users/{user_id}`).
3. File-backed resource reading (`logs://system.log`).
4. Programmatic verification of resource content reading.
"""

import asyncio
import sys
import json
import sqlite3
import os

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="Module03-Resources-Server",
    instructions="Exposes static data, dynamic SQLite query templates, and log file resources."
)

# In-memory database setup for hands-on demonstration
def setup_in_memory_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT)")
    cursor.executemany(
        "INSERT INTO users (id, name, email, role) VALUES (?, ?, ?, ?)",
        [
            (101, "Alice Smith", "alice@example.com", "Administrator"),
            (102, "Bob Jones", "bob@example.com", "Software Engineer"),
            (103, "Charlie Brown", "charlie@example.com", "Data Analyst")
        ]
    )
    conn.commit()
    return conn

db_conn = setup_in_memory_db()

# --- 1. Static Resource ---
@mcp.resource("config://app_settings")
def get_app_settings() -> str:
    """Exposes current runtime configuration settings as JSON."""
    settings = {
        "app_name": "MCP Master Class Enterprise",
        "environment": "staging",
        "max_connections": 50,
        "feature_flags": {
            "enable_telemetry": True,
            "enable_sampling": True
        }
    }
    return json.dumps(settings, indent=2)

# --- 2. Dynamic Resource Template ---
@mcp.resource("sqlite://users/{user_id}")
def get_user_by_id_resource(user_id: str) -> str:
    """
    Exposes user details dynamically based on user ID.
    
    URI Template: sqlite://users/{user_id}
    """
    try:
        uid = int(user_id)
        cursor = db_conn.cursor()
        cursor.execute("SELECT id, name, email, role FROM users WHERE id = ?", (uid,))
        row = cursor.fetchone()
        
        if row:
            data = {"id": row[0], "name": row[1], "email": row[2], "role": row[3]}
            return json.dumps(data, indent=2)
        else:
            return json.dumps({"error": f"User ID {user_id} not found"}, indent=2)
    except ValueError:
        return json.dumps({"error": f"Invalid User ID format: '{user_id}'"}, indent=2)

# --- 3. Dynamic Log File Resource ---
@mcp.resource("logs://system.log")
def get_system_log() -> str:
    """Exposes system diagnostic log lines."""
    log_content = (
        "[2026-09-22 10:00:01] INFO  [Server] FastMCP initialization completed.\n"
        "[2026-09-22 10:01:15] WARN  [DB] In-memory cache hit ratio high.\n"
        "[2026-09-22 10:05:42] INFO  [Auth] Client session connected via Stdio transport.\n"
    )
    return log_content

# --- 4. Verification Harness ---
async def run_verification():
    print("==================================================")
    print("🚀 Module 03: MCP Resources Verification")
    print("==================================================")

    # 1. Test Static Resource
    print("\n--- 1. Testing Static Resource ('config://app_settings') ---")
    config_res = await mcp.read_resource("config://app_settings")
    print(f"Content:\n{config_res[0].content}")

    # 2. Test Dynamic Resource Template (Found User)
    print("\n--- 2. Testing Dynamic Resource Template ('sqlite://users/101') ---")
    user_res_101 = await mcp.read_resource("sqlite://users/101")
    print(f"Content:\n{user_res_101[0].content}")

    # 3. Test Dynamic Resource Template ('sqlite://users/999') ---
    print("\n--- 3. Testing Dynamic Resource Template ('sqlite://users/999') ---")
    user_res_999 = await mcp.read_resource("sqlite://users/999")
    print(f"Content:\n{user_res_999[0].content}")

    # 4. Test Log Resource
    print("\n--- 4. Testing System Log Resource ('logs://system.log') ---")
    log_res = await mcp.read_resource("logs://system.log")
    print(f"Content:\n{log_res[0].content}")

    print("\n==================================================")
    print("✅ Module 03 Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-server":
        mcp.run()
    else:
        asyncio.run(run_verification())
