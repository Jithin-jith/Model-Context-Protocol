"""
Module 09: Advanced Enterprise Capstone - Test Client Suite
===========================================================
This client script automates the verification of the complete Enterprise MCP Server:
1. Spawns `hands_on_server.py` via Stdio transport.
2. Initializes protocol session handshake.
3. Tests discovery of all primitives (Tools, Resources, Prompts).
4. Executes real-time tool calls, resource reads, and prompt generation.
5. Verifies clean shutdown.
"""

import asyncio
import sys
import os

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def run_capstone_test_suite():
    print("==================================================================")
    print("🚀 Module 09: Enterprise Capstone End-to-End Test Suite Client")
    print("==================================================================")

    server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "hands_on_server.py"))
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script, "--run-server"],
        env=dict(os.environ)
    )

    print(f"Connecting to Capstone Server Subprocess:\n  {server_script}\n")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            
            # Step 1: Handshake Initialization
            print("--- Step 1: Performing Protocol Handshake ---")
            await session.initialize()
            print("  ✅ Protocol session initialized successfully!\n")

            # Step 2: Discover Capabilities
            print("--- Step 2: Capability Discovery Matrix ---")
            tools = await session.list_tools()
            print(f"  • Tools Discovered:     {len(tools.tools)} {[t.name for t in tools.tools]}")

            resources = await session.list_resources()
            print(f"  • Resources Discovered: {len(resources.resources)} {[r.uri for r in resources.resources]}")

            prompts = await session.list_prompts()
            print(f"  • Prompts Discovered:   {len(prompts.prompts)} {[p.name for p in prompts.prompts]}\n")

            # Step 3: Test Tool Execution
            print("--- Step 3: Testing Tool Execution ('query_open_incidents') ---")
            tool_res = await session.call_tool("query_open_incidents", {"severity_filter": "CRITICAL"})
            print(f"  Tool Response Output:\n{tool_res.content[0].text}\n")

            # Step 4: Test Resource Reading
            print("--- Step 4: Testing Resource Fetching ('system://health') ---")
            resource_res = await session.read_resource("system://health")
            print(f"  Resource Content:\n{resource_res.contents[0].text}\n")

            # Step 5: Test Prompt Generation
            print("--- Step 5: Testing Prompt Template Fetch ('incident_triage_prompt') ---")
            prompt_res = await session.get_prompt("incident_triage_prompt", {"incident_id": "404"})
            print(f"  Generated Prompt Message:\n{prompt_res.messages[0].content.text}\n")

    print("==================================================================")
    print("✅ ENTERPRISE CAPSTONE TEST SUITE PASSED ALL CHECKS SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    asyncio.run(run_capstone_test_suite())
