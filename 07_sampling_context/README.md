# Module 07: Sampling, Context & Notifications

## 🎯 Learning Objectives
By the end of this module, you will understand:
- **Reverse Sampling (`sampling/createMessage`)**: Enabling MCP Servers to request LLM completions back from the Host Application.
- **Progress Reporting (`notifications/progress`)**: Broadcasting real-time execution progress during long tasks.
- **Contextual Logging (`notifications/message`)**: Streaming log events to client debuggers.
- Security and human-in-the-loop consent mechanisms for sampling.

---

## 1. Understanding Reverse Sampling (`sampling/createMessage`)

In standard MCP operations, the LLM host calls tools on the server. However, complex agentic server tools often need to generate text, summarize documents, or classify content using an LLM *during* execution.

Instead of hardcoding external API keys (e.g. OpenAI/Anthropic API keys) inside the server, MCP provides **Sampling**. The server asks the Host Application's LLM to generate a completion on its behalf!

```
Client / Host Application                                 MCP Server
  |                                                           |
  |--- 1. tools/call("analyze_document") -------------------->|
  |                                                           |  (Tool requires LLM processing)
  |<-- 2. sampling/createMessage(prompt="Summarize...") ------|
  |                                                           |
  | (App checks user consent & routes to host LLM)            |
  |                                                           |
  |--- 3. Sampling Response (Generated Summary Text) -------->|
  |                                                           |  (Tool completes using summary)
  |<-- 4. Tool Execution Result ------------------------------|
```

---

## 2. Benefits of MCP Sampling

1. **No Key Management on Server**: The server does not need API keys, billing configs, or provider settings.
2. **Unified Model Choice**: Uses whichever LLM model the user has active in their Host Application (Claude 3.5 Sonnet, GPT-4o, Local Ollama).
3. **User Governance**: The host application can inspect the prompt request and ask the user for permission before allowing the server to sample tokens.

---

## 3. Progress Notifications (`notifications/progress`)

When executing long-running operations (such as processing 100 PDF files or training a local model), MCP servers send progress notifications:

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def process_large_dataset(item_count: int, ctx: Context) -> str:
    """Processes items in batch and streams real-time progress updates."""
    for i in range(item_count):
        await asyncio.sleep(0.05)
        # Report progress: (current_step, total_steps)
        await ctx.report_progress(progress=i + 1, total=item_count)
        ctx.info(f"Processed item {i + 1}/{item_count}")
        
    return f"Successfully processed {item_count} items."
```

---

## 4. Server-to-Client Contextual Logging

MCP defines standard logging levels (`debug`, `info`, `warning`, `error`). The server can send log messages using `ctx.info()`, `ctx.warn()`, or `ctx.error()`, which the host application renders in its status bar or developer console.

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will practice:
1. Long-running batch tool with `Context` progress reporting.
2. Context logging at various severities (`info`, `warning`, `error`).
3. Programmatic tracking of progress notifications.

### To Run the Hands-on Script:
```bash
python 07_sampling_context/hands_on.py
```
