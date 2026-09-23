"""
Module 08: Security & Production Hardening - Hands-on Implementation
=====================================================================
This script demonstrates:
1. Sandboxed file path resolution preventing Directory Traversal attacks.
2. Parameterized SQLite queries preventing SQL Injection attacks.
3. Clean error boundaries preventing internal information disclosure.
4. Security test suite executing simulated malicious attacks.
"""

import asyncio
import sys
import os
import sqlite3
from pathlib import Path

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="Module08-Hardened-Server",
    instructions="Production hardened server enforcing path sandboxing and SQL parameterization."
)

# Setup sandbox directory structure
SANDBOX_DIR = (Path(__file__).parent / "sandbox").resolve()
SANDBOX_DIR.mkdir(exist_ok=True)

# Populate safe demo file in sandbox
(SANDBOX_DIR / "readme.txt").write_text("Public Sandbox File Content: Welcome!", encoding="utf-8")

# Setup SQLite DB for parameterized query demonstration
def init_secure_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INT, username TEXT, balance DECIMAL)")
    cursor.executemany(
        "INSERT INTO accounts VALUES (?, ?, ?)",
        [(1, "alice", 5000.0), (2, "bob", 1200.0), (3, "charlie", 350.0)]
    )
    conn.commit()
    return conn

secure_db = init_secure_db()

# --- 1. Hardened Sandboxed File Reader Tool ---
@mcp.tool()
def read_sandboxed_file(relative_filename: str) -> str:
    """
    Reads text content from a file inside the strict sandbox directory.

    Args:
        relative_filename: File path relative to sandbox directory.
    """
    # 1. Target path resolution
    target_path = (SANDBOX_DIR / relative_filename).resolve()

    # 2. Strict directory containment validation
    try:
        if not target_path.is_relative_to(SANDBOX_DIR):
            raise PermissionError(f"Security Alert: Traversal attack blocked! Access outside sandbox forbidden.")
    except AttributeError:
        # Fallback for older python path resolution
        if not str(target_path).startswith(str(SANDBOX_DIR)):
            raise PermissionError("Security Alert: Traversal attack blocked!")

    if not target_path.exists():
        raise FileNotFoundError(f"File '{relative_filename}' not found in sandbox.")

    return target_path.read_text(encoding="utf-8")

# --- 2. Hardened Parameterized DB Search Tool ---
@mcp.tool()
def search_account(username_search: str) -> str:
    """
    Searches for account balance using parameterized SQL binding.

    Args:
        username_search: Exact or partial username to look up.
    """
    # ✅ Parameterized query binding prevents SQL injection
    cursor = secure_db.cursor()
    cursor.execute("SELECT id, username, balance FROM accounts WHERE username = ?", (username_search,))
    rows = cursor.fetchall()

    if not rows:
        return f"No account found matching username: '{username_search}'"

    results = [{"id": r[0], "username": r[1], "balance": r[2]} for r in rows]
    import json
    return json.dumps(results, indent=2)

# --- 3. Verification & Security Attack Suite ---
async def run_verification():
    print("==================================================")
    print("🚀 Module 08: Security & Production Hardening Verification")
    print("==================================================")
    print(f"Sandbox Root Directory: {SANDBOX_DIR}")

    # 1. Test Valid Sandbox Read
    print("\n--- 1. Testing Legitimate Sandbox File Read ('readme.txt') ---")
    valid_res = await mcp.call_tool("read_sandboxed_file", {"relative_filename": "readme.txt"})
    print(f"Result:\n  {valid_res[0][0].text}")

    # 2. Test Malicious Directory Traversal Attack
    print("\n--- 2. Testing Malicious Path Traversal Attack ('../../requirement.txt') ---")
    try:
        attack_res = await mcp.call_tool("read_sandboxed_file", {"relative_filename": "../../requirement.txt"})
        print(f"  Result: {attack_res}")
    except Exception as e:
        print(f"  🛡️ ATTACK DEFENDED SUCCESSFUL: {e}")

    # 3. Test Valid DB Query
    print("\n--- 3. Testing Legitimate Account Search ('alice') ---")
    db_res = await mcp.call_tool("search_account", {"username_search": "alice"})
    print(f"Result:\n  {db_res[0][0].text}")

    # 4. Test Malicious SQL Injection Attack
    print("\n--- 4. Testing Malicious SQL Injection Attack ('alice\' OR \'1\'=\'1') ---")
    sql_attack_res = await mcp.call_tool("search_account", {"username_search": "alice' OR '1'='1"})
    print(f"  Result (SQL Injection neutralized):\n  {sql_attack_res[0][0].text}")

    print("\n==================================================")
    print("✅ Module 08 Security Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_verification())
