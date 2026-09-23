"""
Module 02: MCP Tools - Demo Implementation
===========================================
This script demonstrates:
1. Multi-parameter tool with type hints & docstrings.
2. Async tool execution using asyncio.
3. Complex return structures (dicts & lists).
4. Defensive error handling in tools.
5. In-memory verification of tool calls.
"""

import asyncio
import sys
import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="Module02-Tools-Server",
    instructions="Demonstrates advanced tool definitions, parameter schemas, and error boundaries."
)

# --- 1. Multi-parameter Tool ---
@mcp.tool()
def create_user_profile(username: str, email: str, age: int, roles: List[str]) -> Dict:
    """
    Creates a new user profile record.

    Args:
        username: Unique display handle for the user.
        email: Valid user contact email address.
        age: User age in years (must be positive).
        roles: List of assigned permission roles (e.g. ['admin', 'developer']).
    """
    if age < 0 or age > 120:
        raise ValueError(f"Invalid age: {age}. Must be between 0 and 120.")
    if "@" not in email:
        raise ValueError(f"Invalid email address format: '{email}'.")
        
    return {
        "user_id": f"usr_{hash(username) & 0xffffff}",
        "username": username,
        "email": email,
        "age": age,
        "roles": roles,
        "status": "ACTIVE"
    }

# --- 2. Async Tool ---
@mcp.tool()
async def fetch_weather_forecast(city: str, days: int = 3) -> Dict:
    """
    Simulates fetching an async weather forecast for a target location.

    Args:
        city: City name to query forecast for.
        days: Number of forecast days (1 to 7).
    """
    # Simulate async network latency
    await asyncio.sleep(0.1)
    
    if days < 1 or days > 7:
        raise ValueError("Forecast length 'days' must be between 1 and 7.")
        
    forecasts = [
        {"day": i + 1, "temp_c": 20 + i, "condition": "Sunny" if i % 2 == 0 else "Partly Cloudy"}
        for i in range(days)
    ]
    
    return {
        "location": city,
        "forecast_days": days,
        "results": forecasts
    }

# --- 3. Batch Data Processing Tool ---
@mcp.tool()
def analyze_numeric_series(numbers: List[float]) -> Dict[str, float]:
    """
    Calculates summary statistics (min, max, mean, sum) for a list of numbers.

    Args:
        numbers: Non-empty list of numerical values.
    """
    if not numbers:
        raise ValueError("Cannot analyze an empty list of numbers.")
        
    return {
        "count": float(len(numbers)),
        "sum": float(sum(numbers)),
        "mean": float(sum(numbers) / len(numbers)),
        "min": float(min(numbers)),
        "max": float(max(numbers))
    }

# --- 4. Verification Harness ---
async def run_verification():
    print("==================================================")
    print("🚀 Module 02: MCP Tools Verification")
    print("==================================================")
    
    # 1. Test User Profile Creation
    print("\n--- 1. Testing 'create_user_profile' Tool ---")
    user_res = await mcp.call_tool("create_user_profile", {
        "username": "jithin_dev",
        "email": "jithin@example.com",
        "age": 28,
        "roles": ["admin", "architect"]
    })
    print(f"Result:\n  {user_res[0][0].text}")

    # 2. Test Async Weather Tool
    print("\n--- 2. Testing Async 'fetch_weather_forecast' Tool ---")
    weather_res = await mcp.call_tool("fetch_weather_forecast", {
        "city": "San Francisco",
        "days": 2
    })
    print(f"Result:\n  {weather_res[0][0].text}")

    # 3. Test Batch Analysis Tool
    print("\n--- 3. Testing 'analyze_numeric_series' Tool ---")
    stats_res = await mcp.call_tool("analyze_numeric_series", {
        "numbers": [10.5, 20.0, 35.5, 4.0, 50.0]
    })
    print(f"Result:\n  {stats_res[0][0].text}")

    # 4. Test Error Handling (Defensive Validation)
    print("\n--- 4. Testing Error Boundary (Invalid Email & Negative Age) ---")
    try:
        err_res = await mcp.call_tool("create_user_profile", {
            "username": "bad_user",
            "email": "invalid-email-address",
            "age": -5,
            "roles": []
        })
        print(f"Caught formatted error response from FastMCP:\n  {err_res}")
    except Exception as e:
        print(f"Direct Exception Caught: {e}")

    print("\n==================================================")
    print("✅ Module 02 Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-server":
        mcp.run()
    else:
        asyncio.run(run_verification())
