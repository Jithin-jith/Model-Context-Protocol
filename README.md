# Model Context Protocol (MCP) - Master Class Course

Welcome to the **Model Context Protocol (MCP) Master Class**—a comprehensive, hands-on curriculum designed to take you from absolute beginner to advanced production engineer building custom MCP servers and clients in Python.

---

## 📚 Course Overview

The **Model Context Protocol (MCP)** is an open standard developed by Anthropic that enables AI models (like Claude) to securely interact with local and remote resources, tools, database context, and dynamic prompts.

This course is structured into **9 progressive modules**. Each module contains:
1. **Theoretical Deep Dive (`README.md`)**: In-depth explanations of core concepts, architecture diagrams, JSON-RPC primitives, and best practices.
2. **Runnable Hands-on Python Script (`hands_on.py`)**: Self-contained code examples demonstrating real-world usage, server implementations, and client callers.

---

## 🗺️ Curriculum Map

| Module | Topic | Core Focus | Files |
| :--- | :--- | :--- | :--- |
| **Module 01** | [Introduction & Fundamentals](./01_introduction/README.md) | Architecture, Host/Client/Server roles, JSON-RPC 2.0 basis, FastMCP | [`01_introduction/`](./01_introduction/) |
| **Module 02** | [MCP Tools](./02_tools/README.md) | Tool registration, parameter validation, Pydantic, async tools | [`02_tools/`](./02_tools/) |
| **Module 03** | [MCP Resources](./03_resources/README.md) | Static vs dynamic resources, URI templates, MIME types, subscriptions | [`03_resources/`](./03_resources/) |
| **Module 04** | [MCP Prompts](./04_prompts/README.md) | Reusable prompt engineering, dynamic arguments, message roles | [`04_prompts/`](./04_prompts/) |
| **Module 05** | [Transports & Protocols](./05_transports/README.md) | Stdio vs SSE (Server-Sent Events), HTTP streaming, process isolation | [`05_transports/`](./05_transports/) |
| **Module 06** | [Building Custom MCP Clients](./06_clients/README.md) | `ClientSession`, programmatic tool/resource discovery and execution | [`06_clients/`](./06_clients/) |
| **Module 07** | [Sampling, Context & Notifications](./07_sampling_context/README.md) | `sampling/createMessage`, progress reporting, server-triggered LLM | [`07_sampling_context/`](./07_sampling_context/) |
| **Module 08** | [Security & Production Hardening](./08_security/README.md) | Path traversal protection, SQL injection prevention, input sanitization | [`08_security/`](./08_security/) |
| **Module 09** | [Advanced Enterprise Capstone](./09_capstone/README.md) | Multi-tool ecosystem, Claude Desktop / Cursor integration, testing suite | [`09_capstone/`](./09_capstone/) |

---

## ⚡ Quickstart & Setup

### Prerequisites
- Python 3.10 or higher
- `pip` or virtual environment manager (`venv`)

### Installation
1. Clone or open this repository directory:
   ```bash
   cd f:\Projects\Model-Context-Protocol
   ```
2. Activate your virtual environment (if using `.venv`):
   ```powershell
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   ```
3. Install required packages:
   ```bash
   pip install -r requirement.txt
   ```

### Running Hands-on Examples
Navigate to any module folder and run the hands-on Python scripts:
```bash
# Example: Module 1
python 01_introduction/hands_on.py

# Example: Module 6 (Client demonstration)
python 06_clients/hands_on.py
```

---

## 💡 Key Architectural Takeaways

- **Decoupled Integration**: Applications expose capabilities standardly without hardcoding LLM prompt logic.
- **Three Core Primitives**:
  - **Tools**: Model-controlled actions (side-effects allowed).
  - **Resources**: Application-controlled context/data (read-only state).
  - **Prompts**: User-controlled templates (reusable workflow guides).
- **Transport Flexibility**: Run locally over `stdio` or remotely over `SSE` (Server-Sent Events).

Happy Learning! Proceed to [Module 01: Introduction & Fundamentals](./01_introduction/README.md) to get started.