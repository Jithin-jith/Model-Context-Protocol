# Module 04: MCP Prompts - Reusable Prompt Engineering Templates

## 🎯 Learning Objectives
By the end of this module, you will understand:
- The role of **Prompts** as user-triggered workflow templates in MCP.
- Defining **Prompt Arguments** and generating parameterized prompt templates.
- Structuring multi-role messages (`user`, `assistant`).
- Embedding **Resource Context** into Prompts.
- How Host Applications (Claude Desktop / Cursor) expose Prompts to end users.

---

## 1. What are Prompts in MCP?

While **Tools** are actions for the model to take, and **Resources** are data for the model to inspect, **Prompts** are pre-designed templates that assist the *user* in initiating standard workflows with the LLM.

In client UIs like Claude Desktop or Cursor, MCP Prompts show up as searchable workflow commands or template selectors:

```
+---------------+              1. prompts/list             +---------------+
|               | ---------------------------------------> |               |
|               | <--------------------------------------- |               |
|               |       2. Available Prompts List          |               |
|  MCP Client   |                                          |  MCP Server   |
|  (User UI)    |              3. prompts/get              |               |
|               | ---------------------------------------> |               |
|               | <--------------------------------------- |               |
|               |     4. Prepared Prompt Message List      |               |
+---------------+                                          +---------------+
```

---

## 2. Anatomy of an MCP Prompt

When an MCP Client calls `prompts/get(name="review_code", arguments={"language": "python"})`, the server returns a list of pre-configured message objects containing role definitions and template text.

### Example: FastMCP Prompt Registration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prompt-Server")

@mcp.prompt()
def review_code_prompt(code: str, language: str = "python") -> str:
    """
    Generates a code review instruction for the model.

    Args:
        code: Source code snippet to review.
        language: Programming language name (default 'python').
    """
    return f"""Please perform a thorough code review for the following {language} code snippet:

```
{code}
```

Focus your evaluation on:
1. Potential security vulnerabilities.
2. Performance bottlenecks.
3. Code readability and modern conventions.
"""
```

---

## 3. Multi-Role & Advanced Message Structures

Prompts can return more than just a single string! FastMCP allows returning lists of prompt messages representing entire starter conversations:

```python
from mcp.types import PromptMessage, TextContent

@mcp.prompt()
def interactive_tutor(topic: str):
    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=f"I want to learn about {topic}.")
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(type="text", text=f"I'd love to help! What is your current experience level with {topic}?")
        )
    ]
```

---

## 4. Injecting Resource Context into Prompts

One of the most powerful features of MCP Prompts is attaching **Embedded Resources**. This allows a prompt to automatically include dynamic data (such as live log files, database schemas, or API docs) directly alongside the user prompt!

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will build and test:
1. `code_review_prompt`: Generates structured code analysis prompts.
2. `sql_query_assistant`: Generates SQL query creation prompts with attached schema definitions.
3. Multi-role conversation starter prompt.
4. Programmatic execution and verification of generated prompt messages.

### To Run the Hands-on Script:
```bash
python 04_prompts/hands_on.py
```
