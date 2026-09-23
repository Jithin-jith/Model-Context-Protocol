"""
Module 06: Building Custom MCP Clients - Hands-on Implementation
==================================================================
This script demonstrates:
1. Spawning an MCP server process via `StdioServerParameters`.
2. Initializing a `ClientSession`.
3. Performing capability discovery (`list_tools`, `list_resources`).
4. Programmatically executing tool calls and resource reads.
5. Managing clean context lifecycle shutdown.
"""

import asyncio
import sys
import os

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def run_custom_mcp_client():
    print("==================================================")
    print("🚀 Module 06: Custom MCP Client Verification")
    print("==================================================")

    # Path to target server script
    server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_introduction", "hands_on.py"))
    
    print(f"Target Server Script: {server_script}")
    print(f"Python Executable:    {sys.executable}")

    # 1. Configure Subprocess Parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script, "--run-server"],
        env=dict(os.environ)
    )

    # 2. Establish Transport Stream & Session
    print("\n--- 1. Launching Subprocess & Connecting Session ---")
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            
            # Step 1: Handshake Initialization
            await session.initialize()
            print("✅ Protocol Handshake Complete. Session initialized successfully!")

            # Step 2: Capability Discovery
            print("\n--- 2. Discovering Server Capabilities ---")
            tools_result = await session.list_tools()
            print(f"Discovered {len(tools_result.tools)} Tool(s):")
            for tool in tools_result.tools:
                print(f"  • Tool: [{tool.name}] - {tool.description}")

            resources_result = await session.list_resources()
            print(f"\nDiscovered {len(resources_result.resources)} Resource(s):")
            for res in resources_result.resources:
                print(f"  • Resource URI: [{res.uri}] - {res.name}")

            # Step 3: Call Server Tools Programmatically
            print("\n--- 3. Invoking Server Tool ('calculate_sum') ---")
            tool_call_res = await session.call_tool("calculate_sum", {"a": 120.0, "b": 380.0})
            print(f"Tool Execution Output:\n  {tool_call_res.content[0].text}")

            print("\n--- 4. Reading Server Resource ('system://info') ---")
            resource_read_res = await session.read_resource("system://info")
            print(f"Resource Read Output:\n  {resource_read_res.contents[0].text}")

    print("\n==================================================")
    print("✅ Module 06 Custom Client Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_custom_mcp_client())
