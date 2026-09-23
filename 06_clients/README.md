# Module 06: Building Custom MCP Clients in Python

## 🎯 Learning Objectives
By the end of this module, you will understand:
- Why and when to build a custom **MCP Client**.
- The `ClientSession` architecture in `mcp.client`.
- Launching and connecting to local MCP server subprocesses via `StdioServerParameters`.
- Performing protocol initialization handshakes.
- Programmatically discovering and executing **Tools**, **Resources**, and **Prompts**.

---

## 1. Why Build a Custom MCP Client?

While Host Applications like Claude Desktop or Cursor come with built-in MCP clients, software engineers frequently need to build custom MCP clients to:
1. **Build Custom Autonomous AI Agents**: Integrate MCP capabilities into LangChain, LlamaIndex, AutoGen, or custom agent loops.
2. **Automated Testing & CI/CD**: Run integration test suites against custom MCP servers.
3. **Gateway Proxies**: Aggregate capabilities from multiple MCP servers into a single unified endpoint.

---

## 2. Client Architecture & Connection Lifecycle

Connecting an MCP client to a server involves a 4-step lifecycle:

```
Step 1: Transport Creation      Step 2: Stream Handshake       Step 3: Protocol Session      Step 4: Execution
+-----------------------+     +------------------------+     +-----------------------+     +--------------------+
| StdioServerParameters | --> | stdio_client(params)   | --> | ClientSession(r, w)   | --> | session.list_tools |
| (Command, Args, Env)  |     | (Establishes Subprocess|     | await session.init()  |     | session.call_tool  |
+-----------------------+     +------------------------+     +-----------------------+     +--------------------+
```

---

## 3. Step-by-Step Code Walkthrough

### A. Define Stdio Parameters
```python
from mcp.client.stdio import StdioServerParameters

server_params = StdioServerParameters(
    command="python",
    args=["02_tools/hands_on.py", "--run-server"],
    env={"PYTHONUNBUFFERED": "1"}
)
```

### B. Connect & Initialize Session
```python
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

async with stdio_client(server_params) as (read_stream, write_stream):
    async with ClientSession(read_stream, write_stream) as session:
        # Step 1: Mandatory Protocol Handshake
        await session.initialize()
        
        # Step 2: Capability Discovery
        tools = await session.list_tools()
        resources = await session.list_resources()
        prompts = await session.list_prompts()
        
        # Step 3: Invoke Capabilities
        result = await session.call_tool("create_user_profile", {
            "username": "client_dev",
            "email": "dev@mcp.org",
            "age": 30,
            "roles": ["engineer"]
        })
        print("Tool Output:", result.content[0].text)
```

---

## 4. Handling Client Sessions Safely

- **Async Context Managers**: Always use `async with` blocks to guarantee subprocess cleanup and avoid orphan zombie processes on exit.
- **Error Handling**: Wrap tool execution calls in try/except blocks to gracefully catch `mcp.types.McpError` exceptions.

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will execute a fully functional custom MCP client that:
1. Spawns an MCP server subprocess (`02_tools/hands_on.py`).
2. Performs protocol initialization handshake.
3. Discovers all tools exposed by the server.
4. Programmatically calls tools and inspects returns.
5. Gracefully closes the session.

### To Run the Hands-on Script:
```bash
python 06_clients/hands_on.py
```
