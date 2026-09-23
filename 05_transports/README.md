# Module 05: Transports & Protocols - Standard I/O vs SSE

## 🎯 Learning Objectives
By the end of this module, you will understand:
- The role of the **Transport Layer** in decoupling protocol logic from communication channels.
- How **Standard I/O (`stdio`) Transport** powers local desktop extensions (Claude Desktop, Cursor).
- How **Server-Sent Events (`sse`) Transport** enables remote/cloud MCP servers over HTTP.
- Detailed architectural trade-offs between `stdio` and `sse`.
- How to launch, configure, and connect to both transport modes in Python.

---

## 1. Transport Layer Overview

MCP decouples the higher-level JSON-RPC protocol messages from the underlying transport mechanism. This means your tools, resources, and prompts remain identical regardless of whether the server runs as a local child process or in a cloud container across the internet.

```
+-----------------------------------------------------------------+
|                       JSON-RPC 2.0 Protocol                     |
|           (tools/call, resources/read, prompts/get)             |
+-----------------------------------------------------------------+
                                |
             +------------------+------------------+
             |                                     |
+--------------------------+             +--------------------------+
|  Standard I/O Transport  |             |      SSE Transport       |
|  (stdin / stdout streams)|             | (HTTP GET SSE + POST)    |
+--------------------------+             +--------------------------+
             |                                     |
      Local Process                       Remote Network / Cloud
```

---

## 2. Standard I/O (`stdio`) Transport

### How it Works:
1. The **Host Application** (e.g. Claude Desktop) launches the MCP server process as a child process (e.g., `python server.py`).
2. Communication flows via standard OS streams:
   - **`stdin`**: Host writes JSON-RPC request messages to Server.
   - **`stdout`**: Server writes JSON-RPC response messages to Host.
   - **`stderr`**: Server writes logs and diagnostic text (ignored by protocol parser).

### Key Advantages:
- **Zero Configuration**: No network ports, IP addresses, or firewall setups needed.
- **Process Isolation**: Host controls process lifecycle (starts on demand, terminates on exit).
- **Security**: Environment variables (e.g. API keys) passed securely to the subprocess without exposing open ports.

---

## 3. Server-Sent Events (`sse`) Transport

### How it Works:
1. **GET Endpoint (`/sse`)**: Client initiates an HTTP GET request to establish a persistent Server-Sent Events (SSE) stream. The server responds with a unique session endpoint URI.
2. **POST Endpoint (`/messages/`)**: Client sends JSON-RPC requests via standard HTTP POST requests targeting the session URI. Server broadcasts responses back down the open SSE stream.

```
Client                                                  Server
  |                                                        |
  |--- HTTP GET /sse ------------------------------------->| (Establishes SSE Stream)
  |<-- 200 OK (Event stream open + session ID) ------------|
  |                                                        |
  |--- HTTP POST /messages/?session_id=abc (JSON-RPC) ---->|
  |<-- 202 Accepted ---------------------------------------|
  |                                                        |
  |<-- SSE Event message (JSON-RPC Result) ----------------| (Downstream Response)
```

### Key Advantages:
- **Remote Access**: Servers can run on cloud hosts, Docker, or Kubernetes clusters.
- **Multi-Client**: Multiple client sessions can connect to a central remote MCP server.
- **Web Standards**: Built on HTTP/1.1 and HTTP/2 standards, easily fronted by reverse proxies (Nginx, Traefik, Cloudflare).

---

## 4. Stdio vs. SSE Feature Comparison Matrix

| Feature | Standard I/O (`stdio`) | Server-Sent Events (`sse`) |
| :--- | :--- | :--- |
| **Deployment** | Local Child Process | Remote HTTP Server |
| **Setup Complexity** | Very Low | Low-Medium (Port/Host routing) |
| **Authentication** | Process Env Variables | HTTP Headers, OAuth, Bearer Tokens |
| **Multi-Client Support** | Single Host Process | Multi-Client Concurrent Sessions |
| **Ideal For** | Desktop IDEs, Local Tools | Microservices, Shared Enterprise DBs |

---

## 🛠️ Hands-on Code Overview

This module provides two distinct hands-on files:
1. [`hands_on_stdio.py`](./hands_on_stdio.py): Standard IO MCP server runner.
2. [`hands_on_sse.py`](./hands_on_sse.py): Starlette/Uvicorn SSE transport server and an HTTP test client connecting over network sockets.

### To Run the Hands-on Examples:
```bash
# Test Stdio Server runner
python 05_transports/hands_on_stdio.py

# Test SSE Server & Remote Client
python 05_transports/hands_on_sse.py
```
