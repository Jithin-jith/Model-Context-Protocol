"""
Module 04: MCP Prompts - Hands-on Implementation
=================================================
This script demonstrates:
1. Basic single-string parameterized prompt template.
2. Advanced prompt embedding resource schema context.
3. Multi-role (`user` / `assistant`) prompt generation.
4. Programmatic evaluation of prompt templates.
"""

import asyncio
import sys
import json
from typing import List

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

# Initialize FastMCP Server
mcp = FastMCP(
    name="Module04-Prompts-Server",
    instructions="Exposes reusable prompt templates for code review, SQL generation, and tutoring."
)

# --- 1. Basic Parameterized Code Review Prompt ---
@mcp.prompt()
def code_review_template(code_snippet: str, language: str = "python") -> str:
    """
    Generates a structured prompt instructing the model to perform a code review.

    Args:
        code_snippet: The raw code text to analyze.
        language: Programming language name.
    """
    return f"""Act as a Senior Principal Engineer. Please perform a rigorous code review of the following {language} code snippet:

```{language}
{code_snippet}
```

Provide your feedback structured as:
1. **Critical Bugs & Security Risks**
2. **Performance Optimizations**
3. **Refactored Code Example**
"""

# --- 2. SQL Query Generation Prompt embedding Schema ---
@mcp.prompt()
def generate_sql_query_prompt(user_intent: str, target_table: str = "orders") -> str:
    """
    Generates a prompt for SQL query writing with embedded table schema context.

    Args:
        user_intent: Plain English description of what data to query.
        target_table: Table name to query against.
    """
    schema_map = {
        "orders": "CREATE TABLE orders (id INT, user_id INT, amount DECIMAL, status VARCHAR(20), created_at TIMESTAMP);",
        "users": "CREATE TABLE users (id INT, name VARCHAR(100), email VARCHAR(100), role VARCHAR(50));"
    }
    
    schema_ddl = schema_map.get(target_table, f"CREATE TABLE {target_table} (id INT, data TEXT);")
    
    return f"""Target Table Schema:
{schema_ddl}

User Intent:
"{user_intent}"

Please write a clean, optimized SQL query that accomplishes the user's intent. Explain any WHERE clauses or indexing considerations.
"""

# --- 3. Multi-Role Prompt Starter ---
@mcp.prompt()
def architecture_interview_starter(system_design_topic: str) -> List[PromptMessage]:
    """
    Creates an interactive 2-turn conversation starter for architecture mock interviews.

    Args:
        system_design_topic: System topic (e.g. 'URL Shortener', 'Distributed Cache').
    """
    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=f"I want to practice a System Design Interview on building a '{system_design_topic}'.")
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(
                type="text",
                text=f"Great choice! Let's work through designing a **{system_design_topic}**. "
                     f"To start, could you outline the key functional and non-functional requirements you want us to support?"
            )
        )
    ]

# --- 4. Verification Harness ---
async def run_verification():
    print("==================================================")
    print("🚀 Module 04: MCP Prompts Hands-On Verification")
    print("==================================================")

    # 1. Test Code Review Prompt
    print("\n--- 1. Testing 'code_review_template' ---")
    prompt_res1 = await mcp.get_prompt("code_review_template", {
        "code_snippet": "def add(a, b):\n    return a + b",
        "language": "python"
    })
    print(f"Generated Messages ({len(prompt_res1.messages)} message):\n")
    print(prompt_res1.messages[0].content.text)

    # 2. Test SQL Query Prompt
    print("\n--- 2. Testing 'generate_sql_query_prompt' ---")
    prompt_res2 = await mcp.get_prompt("generate_sql_query_prompt", {
        "user_intent": "Get total order amount for completed orders in the last 30 days",
        "target_table": "orders"
    })
    print(f"Generated Messages ({len(prompt_res2.messages)} message):\n")
    print(prompt_res2.messages[0].content.text)

    # 3. Test Multi-Role Prompt
    print("\n--- 3. Testing Multi-Role 'architecture_interview_starter' ---")
    prompt_res3 = await mcp.get_prompt("architecture_interview_starter", {
        "system_design_topic": "Global Rate Limiter"
    })
    print(f"Generated Message Count: {len(prompt_res3.messages)}")
    for i, msg in enumerate(prompt_res3.messages):
        print(f"  Message [{i+1}] ({msg.role}): {msg.content.text}")

    print("\n==================================================")
    print("✅ Module 04 Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_verification())
