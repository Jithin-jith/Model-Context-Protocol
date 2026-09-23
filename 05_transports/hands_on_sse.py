"""
Module 05: Transports - Server-Sent Events (SSE) Hands-on Implementation
========================================================================
This script demonstrates:
1. Configuring a FastMCP server for SSE HTTP transport.
2. Launching an SSE server on a local port.
3. Connecting an asynchronous HTTP SSE client using `mcp.client.sse`.
4. Invoking tools over network sockets.
"""

import sys
import asyncio
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize FastMCP Server configured for SSE
mcp = FastMCP(
    name="SSE-Transport-Server",
    host="127.0.0.1",
    port=8001,
    instructions="Operates via SSE HTTP transport streams on port 8001."
)

@mcp.tool()
def get_server_time() -> str:
    """Returns the current server timestamp string."""
    import datetime
    return f"Server Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.tool()
def remote_calculator(a: float, b: float, operation: str = "multiply") -> str:
    """
    Performs math operations over remote HTTP SSE connection.

    Args:
        a: First number
        b: Second number
        operation: 'add', 'subtract', 'multiply', or 'divide'
    """
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero is forbidden.")
        return str(a / b)
    else:
        raise ValueError(f"Unknown operation: '{operation}'")

# --- Client Test Harness connecting over HTTP SSE ---
async def run_sse_client_verification():
    print("==================================================")
    print("🚀 Module 05: SSE Transport Hands-On Verification")
    print("==================================================")
    
    sse_url = "http://127.0.0.1:8001/sse"
    print(f"Connecting SSE Client to target URL: {sse_url}...")
    
    try:
        async with sse_client(sse_url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ Client Session Initialized successfully over SSE!")
                
                # 1. List Server Tools over HTTP
                print("\n--- 1. Querying Tools over SSE ---")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"  Found Tool: {tool.name} - {tool.description}")
                
                # 2. Execute Remote Tool Call over HTTP
                print("\n--- 2. Executing 'remote_calculator' over SSE ---")
                calc_res = await session.call_tool("remote_calculator", {"a": 12.0, "b": 4.0, "operation": "multiply"})
                print(f"  Result: {calc_res.content[0].text}")
                
                # 3. Execute Time Tool over HTTP
                print("\n--- 3. Executing 'get_server_time' over SSE ---")
                time_res = await session.call_tool("get_server_time", {})
                print(f"  Result: {time_res.content[0].text}")
                
    except Exception as e:
        print(f"⚠️ Could not connect to SSE server directly: {e}")
        print("Note: Start the SSE server first using: python 05_transports/hands_on_sse.py --serve")

    print("\n==================================================")
    print("✅ SSE Verification Routine Finished!")
    print("==================================================")

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("Starting FastMCP SSE Server on http://127.0.0.1:8001 ...")
        mcp.run(transport="sse")
    else:
        # Run server in background task and client in foreground task for self-contained testing
        import socket
        # Quick server task setup using FastMCP internal SSE app
        server_task = asyncio.create_task(asyncio.to_thread(mcp.run, "sse"))
        await asyncio.sleep(1.5)  # Wait for server startup
        
        try:
            await run_sse_client_verification()
        finally:
            server_task.cancel()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        mcp.run(transport="sse")
    else:
        # Execute direct verification
        asyncio.run(run_sse_client_verification())
