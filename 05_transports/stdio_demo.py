"""
Module 05: Transports - Standard I/O (stdio) Hands-on Implementation
=====================================================================
This script demonstrates running a FastMCP server over standard OS I/O streams.
When executed directly with verification mode, it verifies stdio tool execution.
"""

import sys
import asyncio

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

# Initialize Stdio FastMCP Server
mcp = FastMCP(
    name="Stdio-Transport-Server",
    instructions="Operates via stdin/stdout streams for local host integration."
)

@mcp.tool()
def echo_message(message: str) -> str:
    """Echos back input text with stdio prefix."""
    return f"[Stdio Server Echo]: {message}"

@mcp.resource("system://stdio_info")
def stdio_info() -> str:
    """Exposes transport details."""
    return "Transport: Standard I/O (stdin/stdout) | Mode: Process Subprocess"

async def run_verification():
    print("==================================================")
    print("🚀 Module 05: Stdio Transport Hands-On Verification")
    print("==================================================")
    
    echo_res = await mcp.call_tool("echo_message", {"message": "Hello via Stdio!"})
    print(f"Tool Echo Result:\n  {echo_res[0][0].text}")
    
    info_res = await mcp.read_resource("system://stdio_info")
    print(f"Resource Info Result:\n  {info_res[0].content}")

    print("\n==================================================")
    print("✅ Stdio Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        # Launch standard stdio server loop for client connections
        mcp.run(transport="stdio")
    else:
        asyncio.run(run_verification())
