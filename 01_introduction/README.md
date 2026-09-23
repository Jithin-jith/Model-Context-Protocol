# Module 01: Introduction & Fundamentals of MCP

## 🎯 Learning Objectives
By the end of this module, you will understand:
- What the **Model Context Protocol (MCP)** is and why it exists.
- The 3-tier architecture: **Host Application**, **MCP Client**, and **MCP Server**.
- How MCP standardizes AI-to-system integrations over **JSON-RPC 2.0**.
- The difference between the **Low-level SDK (`mcp`)** and **High-level Framework (`FastMCP`)**.
- How to build, initialize, and test your first MCP Server in Python.

---

## 1. What is Model Context Protocol (MCP)?

Before MCP, connecting AI models (such as Claude, GPT-4, or custom LLMs) to external data sources (databases, APIs, local files, developer tools) required custom glue code for every tool and every client application. 

**Model Context Protocol (MCP)** is an open standard that decouples LLM applications from data/tool providers:

```
+-----------------------------------------------------------------------+
|                           Host Application                            |
|             (Claude Desktop, Cursor, Custom Python Agent)            |
|                                                                       |
|   +---------------------------------------------------------------+   |
|   |                          MCP Client                           |   |
|   +-------------------------------+-------------------------------+   |
+-----------------------------------|-----------------------------------+
                                    | Standardized JSON-RPC 2.0
                                    | (stdio or SSE Transport)
+-----------------------------------|-----------------------------------+
|   +-------------------------------+-------------------------------+   |
|   |                          MCP Server                           |   |
|   |                      (Python / TypeScript)                    |   |
|   +---------------------------------------------------------------+   |
|                                                                       |
|      [ Tools ]               [ Resources ]             [ Prompts ]    |
|   (Execute Actions)       (Expose Data/State)      (Reusable Templates)|
+-----------------------------------------------------------------------+
```

---

## 2. Core Architecture Roles

1. **Host Application**: The end-user application containing the LLM environment (e.g., Claude Desktop, Cursor IDE, VSCode extension, or a custom Python agent framework).
2. **MCP Client**: Maintained inside the host application. Establishes a 1-to-1 connection session with an MCP Server, performs capability negotiation, handles request routing, and enforces user consent.
3. **MCP Server**: A lightweight executable program or remote service exposing specific capabilities (Tools, Resources, and Prompts) via standard protocols.

---

## 3. The Three Core MCP Primitives

MCP divides server capabilities into three standardized primitives:

| Primitive | Primary Purpose | Initiated By | Side Effects? | Analogy |
| :--- | :--- | :--- | :--- | :--- |
| **Tools** | Execute functions/actions | Model / LLM | Yes (Can mutate state) | REST POST/PUT API |
| **Resources** | Attach passive context/data | Client / User | No (Read-only) | REST GET Endpoint |
| **Prompts** | Pre-designed workflow templates | User / Host | No | Slash Command / Macro |

---

## 4. Under the Hood: JSON-RPC 2.0 Protocol

All communication between MCP Clients and Servers takes place via **JSON-RPC 2.0**. 

### Example: Tool Discovery Request (`tools/list`)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### Example: Server Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_server_status",
        "description": "Returns health check details for the server.",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      }
    ]
  }
}
```

---

## 5. Low-Level SDK vs. High-Level FastMCP

In Python, the official `mcp` library provides two abstraction levels:

1. **Low-level SDK (`mcp.server.lowlevel.Server`)**: Full manual control over JSON-RPC handlers, request routing, raw schema definitions, and transport streams.
2. **High-level Framework (`FastMCP`)**: FastAPI-like developer experience using Python decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) with automatic schema generation from type hints and docstrings.

In this course, we utilize **FastMCP** for rapid implementation while diving into low-level concepts when appropriate.

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will find:
- A complete FastMCP server initialization.
- Tool and Resource registration.
- An in-memory testing routine using a client session simulator to verify server response without needing external UIs.

### To Run the Hands-on Script:
```bash
python 01_introduction/hands_on.py
```
