# Module 09: Advanced Enterprise Capstone - End-to-End MCP Ecosystem

## 🎯 Learning Objectives
By the end of this module, you will:
- Architect a complete enterprise multi-primitive **MCP Server**.
- Integrate tools, resources, prompts, progress logging, and security into a single cohesive engine.
- Configure Host Applications (**Claude Desktop**, **Cursor IDE**) to connect to your custom server.
- Execute an end-to-end automated testing suite with a custom Python client.

---

## 1. Enterprise Architecture Overview

An Enterprise MCP Ecosystem integrates multiple data streams and operational capabilities into standard protocol endpoints:

```
+-------------------------------------------------------------------------------+
|                            Host Application UI                                |
|                      (Claude Desktop, Cursor, Custom Agent)                   |
+-------------------------------------------------------------------------------+
                                       |
                         Stdio or SSE Transport Connection
                                       |
+-------------------------------------------------------------------------------+
|                        Enterprise MCP Capstone Server                         |
|                                                                               |
|  [ Tools ]                  [ Resources ]              [ Prompts ]            |
|  • query_database           • system://health          • incident_triage      |
|  • generate_report          • logs://app.log           • code_review          |
|  • execute_health_check                                                       |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  |           Security Sandbox • Progress Reporting • Error Boundary         |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
```

---

## 2. Host Configuration Guides

### A. Claude Desktop Integration

To connect your custom MCP server to **Claude Desktop**:

1. Open or create the configuration file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add your server under `mcpServers`:

```json
{
  "mcpServers": {
    "enterprise-mcp": {
      "command": "F:\\Projects\\Model-Context-Protocol\\.venv\\Scripts\\python.exe",
      "args": [
        "F:\\Projects\\Model-Context-Protocol\\09_capstone\\hands_on_server.py",
        "--run-server"
      ]
    }
  }
}
```

3. Restart Claude Desktop. The hammer icon (⚙️ / 🔨) will appear showing your available tools!

---

### B. Cursor IDE Integration

1. Open **Cursor Settings** -> **Features** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. Set Name: `Enterprise-MCP`.
4. Set Type: `command`.
5. Set Command: `python F:\Projects\Model-Context-Protocol\09_capstone\hands_on_server.py --run-server`.

---

## 🛠️ Hands-on Code Overview

This module consists of two capstone scripts:
1. [`hands_on_server.py`](./hands_on_server.py): The enterprise production server.
2. [`hands_on_client.py`](./hands_on_client.py): The automated verification test suite client.

### To Run the Capstone Verification:
```bash
python 09_capstone/hands_on_client.py
```
