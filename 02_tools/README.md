# Module 02: MCP Tools - Dynamic Capabilities & Function Calling

## 🎯 Learning Objectives
By the end of this module, you will understand:
- The role of **Tools** as model-driven actions in MCP.
- How FastMCP extracts **JSON Schemas** from Python type annotations and docstrings.
- Synchronous (`def`) vs Asynchronous (`async def`) tool definitions.
- Returning structured objects, strings, and media content.
- Handling exceptions defensively and understanding how MCP packages errors.

---

## 1. Understanding Tools in MCP

Tools in MCP represent executable functions exposed by the server that an LLM can choose to invoke. Unlike Resources (which are passive data sources), **Tools can perform actions, mutate state, call external APIs, query databases, or execute computation**.

```
+---------------+              1. tools/list              +---------------+
|               | --------------------------------------> |               |
|               | <-------------------------------------- |               |
|               |      2. Tools List & JSON Schemas       |               |
|  MCP Client   |                                         |  MCP Server   |
|   (or LLM)    |              3. tools/call              |               |
|               | --------------------------------------> |               |
|               | <-------------------------------------- |               |
|               |    4. Call Result (Text/Image/Error)    |               |
+---------------+                                         +---------------+
```

---

## 2. Tool Registration & Schema Generation

When you register a function with `@mcp.tool()`, FastMCP automatically inspects:
1. **Function Name**: Becomes the tool name in `tools/list`.
2. **Docstring**: Becomes the tool's `description` field sent to the LLM.
3. **Type Annotations**: Converted into JSON Schema `inputSchema` for strict model parameter generation.

### Example: FastMCP Tool Definition
```python
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Tool-Server")

@mcp.tool()
def search_database(query: str, limit: int = 10) -> str:
    """
    Search the database for matching user records.

    Args:
        query: Search keyword or SQL filter term.
        limit: Maximum number of records to return (default 10).
    """
    return f"Found results for {query} with limit {limit}"
```

### Corresponding JSON Schema sent to Client/LLM:
```json
{
  "name": "search_database",
  "description": "Search the database for matching user records.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Search keyword or SQL filter term." },
      "limit": { "type": "integer", "default": 10, "description": "Maximum number of records to return (default 10)." }
    },
    "required": ["query"]
  }
}
```

---

## 3. Synchronous vs Asynchronous Tools

FastMCP supports both sync (`def`) and async (`async def`) functions seamlessly:
- **Sync Tools (`def`)**: Ideal for lightweight CPU computations or synchronous library calls. Run in an internal threadpool to prevent blocking the event loop.
- **Async Tools (`async def`)**: Ideal for network requests (`httpx`), database access (`aiosqlite`, `asyncpg`), and file I/O (`aiofiles`).

---

## 4. Return Formats & Content Types

Tools can return:
- **`str`**: Raw string or JSON string content.
- **`dict` / `list`**: Automatically serialized to JSON.
- **`Pydantic Model`**: Serialized into JSON schema representation.
- **List of `Content` objects**: `TextContent`, `ImageContent`, or `EmbeddedResource` for rich media support.

---

## 5. Error Handling in Tools

When a tool raises an unhandled exception (e.g., `ValueError`, `KeyError`), FastMCP catches it and formats the response as a JSON-RPC result with `isError: true`:

```json
{
  "content": [
    {
      "type": "text",
      "text": "ValueError: Invalid query syntax. Only SELECT statements allowed."
    }
  ],
  "isError": true
}
```

This prevents server crashes and allows the LLM to inspect the error message and retry with corrected parameters!

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will practice:
1. Defining multi-parameter tools with Pydantic validation.
2. Building an asynchronous weather API mock tool.
3. Batch data processing tool returning formatted statistics.
4. Testing defensive exception handling when invalid input is provided.

### To Run the Hands-on Script:
```bash
python 02_tools/hands_on.py
```
