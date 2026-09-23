"""
Module 01: Introduction & Fundamentals of MCP - Demo
=====================================================
This script demonstrates:
1. Creating a FastMCP server.
2. Registering a simple Tool and Resource.
3. Programmatically testing the server using FastMCP internal call engine.
"""

import asyncio
import sys
import io

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

# 1. Initialize the FastMCP Server
mcp = FastMCP(
    name="Intro-Demo-Server",
    instructions="A simple introductory MCP server demonstrating tool and resource registration."
)

# 2. Register a Tool using decoratored function
@mcp.tool()
def get_server_status() -> str:
    """Returns the current operational status of the server."""
    return "OK - Intro MCP Server is running smoothly!"

@mcp.tool()
def calculate_sum(a: float, b: float) -> float:
    """
    Calculates the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
    """
    return a + b

# 3. Register a Static Resource
@mcp.resource("system://info")
def get_system_info() -> str:
    """Exposes static system information context."""
    return "System: MCP Python Masterclass | Module: 01 | Status: Active"


# 4. Programmatic Verification Routine
async def run_verification():
    print("==================================================")
    print("🚀 Starting Module 01 Hands-On Verification...")
    print("==================================================")
    
    # We test the tools directly via FastMCP internal execution engine
    print("\n--- 1. Testing Registered Tools ---")
    status_result = await mcp.call_tool("get_server_status", {})
    print(f"Tool 'get_server_status' response:\n  {status_result}")
    
    sum_result = await mcp.call_tool("calculate_sum", {"a": 15.5, "b": 24.5})
    print(f"Tool 'calculate_sum(15.5, 24.5)' response:\n  {sum_result}")
    
    print("\n--- 2. Testing Registered Resource ---")
    resource_result = await mcp.read_resource("system://info")
    print(f"Resource 'system://info' content:\n  {resource_result}")
    
    print("\n==================================================")
    print("✅ Module 01 Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    # If invoked directly with '--run-server', run the standard IO server loop
    if len(sys.argv) > 1 and sys.argv[1] == "--run-server":
        mcp.run()
    else:
        # Default behavior: run verification harness
        asyncio.run(run_verification())
