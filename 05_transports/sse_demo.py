"""
Module 05: Transports - Server-Sent Events (SSE) Hands-on Implementation
========================================================================

Overview:
---------
In Model Context Protocol (MCP), transports define how the Client and Server 
exchange JSON-RPC messages. While Standard IO (stdio) is ideal for local CLI 
and desktop tools where the host spawns a child process, Server-Sent Events (SSE) 
over HTTP is designed for networked, distributed, or containerized architectures.

How MCP over SSE Works:
-----------------------
1. Connection Establishment (GET /sse):
   - The MCP client opens an HTTP GET request with `Accept: text/event-stream`
     to the server's `/sse` endpoint.
   - The server keeps this connection open and assigns a unique `session_id`.
   - The server immediately pushes an initial event containing the endpoint
     URI for client messages:
     e.g., `event: endpoint\ndata: /messages/?session_id=<uuid>\n\n`

2. Bi-directional Communication:
   - Server-to-Client: Delivered asynchronously as events over the open GET stream (read_stream).
   - Client-to-Server: Delivered via standard HTTP POST requests sent to `/messages/?session_id=...` (write_stream).

3. Protocol Handshake & Tool Invocation:
   - Once the two streams are paired, `ClientSession` performs the standard 
     MCP handshake (`initialize` -> `initialized`) and can invoke tools, prompts, 
     or resources across the network socket.

Usage Modes:
------------
1. Self-Contained Verification (Default):
   Runs the server in a background thread and immediately tests it with a client:
   $ python 05_transports/sse_demo.py

2. Standalone Long-Running Server:
   Runs the server indefinitely to accept external connections (e.g. Claude Desktop, Inspector):
   $ python 05_transports/sse_demo.py --serve

Example Console Output:
-----------------------
```text
Starting local SSE server in background thread...
INFO:     Started server process [21704]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
==================================================
🚀 Module 05: SSE Transport Hands-On Verification
==================================================
Connecting SSE Client to target URL: http://127.0.0.1:8001/sse...
INFO:     127.0.0.1:64137 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:64138 - "POST /messages/?session_id=921b6... HTTP/1.1" 202 Accepted
✅ Client Session Initialized successfully over SSE!

--- 1. Querying Tools over SSE ---
  Found Tool: get_server_time - Returns the current server timestamp string.
  Found Tool: remote_calculator - Performs math operations over remote HTTP SSE connection.

--- 2. Executing 'remote_calculator' over SSE ---
  Result: 48.0

--- 3. Executing 'get_server_time' over SSE ---
  Result: Server Time: 2026-09-26 07:32:45

==================================================
✅ SSE Verification Routine Finished!
==================================================
```
"""

import sys
import asyncio
import threading
import time
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. Server Configuration & Setup
# ==============================================================================
# We configure FastMCP with host and port parameters. When started with
# transport="sse", FastMCP utilizes Starlette and Uvicorn under the hood to host
# the SSE event stream and the POST message handler.
mcp = FastMCP(
    name="SSE-Transport-Server",
    host="127.0.0.1",
    port=8001,
    instructions="Operates via SSE HTTP transport streams on port 8001."
)

@mcp.tool()
def get_server_time() -> str:
    """
    Returns the current server timestamp string.

    Demonstrates a simple zero-argument tool accessible over the network.
    Returns:
        Formatted string containing current ISO-like date and time.
    """
    import datetime
    return f"Server Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.tool()
def remote_calculator(a: float, b: float, operation: str = "multiply") -> str:
    """
    Performs math operations over remote HTTP SSE connection.

    Demonstrates multi-argument validation and calculation over network RPC.

    Args:
        a: First number (operand).
        b: Second number (operand).
        operation: Calculation type - 'add', 'subtract', 'multiply', or 'divide'.

    Returns:
        String representation of the resulting numerical calculation.

    Raises:
        ValueError: If division by zero is attempted or operation is unsupported.
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

# ==============================================================================
# 2. Client Test Harness (HTTP SSE Connection)
# ==============================================================================
async def run_sse_client_verification():
    """
    Asynchronous client verification function.

    Demonstrates:
    1. Opening an SSE stream to 'http://127.0.0.1:8001/sse'.
    2. Receiving read/write stream handles via `sse_client`.
    3. Performing initialization handshake (`session.initialize()`).
    4. Querying tools (`session.list_tools()`).
    5. Executing tools remotely via HTTP POST (`session.call_tool()`).
    """
    print("==================================================")
    print("🚀 Module 05: SSE Transport Hands-On Verification")
    print("==================================================")
    
    sse_url = "http://127.0.0.1:8001/sse"
    print(f"Connecting SSE Client to target URL: {sse_url}...")
    
    try:
        # sse_client opens the HTTP GET connection and resolves the message POST endpoint
        async with sse_client(sse_url) as (read_stream, write_stream):
            # ClientSession handles the JSON-RPC framing and handshake
            async with ClientSession(read_stream, write_stream) as session:
                # Step 1: Handshake (negotiate version, exchange capabilities)
                await session.initialize()
                print("✅ Client Session Initialized successfully over SSE!")
                
                # Step 2: Query tools over the network
                print("\n--- 1. Querying Tools over SSE ---")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"  Found Tool: {tool.name} - {tool.description.strip()}")
                
                # Step 3: Execute calculator tool (sends POST request to server)
                print("\n--- 2. Executing 'remote_calculator' over SSE ---")
                calc_res = await session.call_tool("remote_calculator", {"a": 12.0, "b": 4.0, "operation": "multiply"})
                print(f"  Result: {calc_res.content[0].text}")
                
                # Step 4: Execute server time tool
                print("\n--- 3. Executing 'get_server_time' over SSE ---")
                time_res = await session.call_tool("get_server_time", {})
                print(f"  Result: {time_res.content[0].text}")
                
    except Exception as e:
        print(f"⚠️ Could not connect to SSE server directly: {e}")
        print("Note: If running as a standalone client, start the server first using: python 05_transports/sse_demo.py --serve")

    print("\n==================================================")
    print("✅ SSE Verification Routine Finished!")
    print("==================================================")

# ==============================================================================
# 3. Execution Entrypoint
# ==============================================================================
def main():
    """
    Coordinates execution between standalone server mode and self-contained test mode.

    - Standalone Server Mode (`--serve`):
      Blocks on `mcp.run("sse")` so external clients (Claude Desktop, etc.) can connect.
    - Test Mode (default):
      Spawns the SSE server in a background daemon thread, waits for it to bind,
      and runs the client verification routine in the foreground.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("Starting FastMCP SSE Server on http://127.0.0.1:8001 ...")
        # Starts Uvicorn in the main thread (blocking)
        mcp.run(transport="sse")
    else:
        print("Starting local SSE server in background thread...")
        # Start server in daemon thread so it terminates automatically when client finishes
        server_thread = threading.Thread(target=mcp.run, args=("sse",), daemon=True)
        server_thread.start()
        
        # Give Uvicorn a moment to bind to port 8001
        time.sleep(1.5)

        # Run client verification against the live local server
        asyncio.run(run_sse_client_verification())

if __name__ == "__main__":
    main()
