# Module 08: Security & Production Hardening

## 🎯 Learning Objectives
By the end of this module, you will understand:
- Top security vectors in MCP server implementations.
- Mitigating **Path Traversal** attack vectors in file resources and tools.
- Preventing **SQL Injection** and **Command Injection**.
- Enforcing **Execution Timeouts** and resource caps.
- Designing clean **Error Boundaries** to prevent credential or internal stack leaks.

---

## 1. Security Vectors in MCP Architecture

Because MCP servers act as bridges connecting LLMs (which operate on untrusted text inputs) to internal system infrastructure, security boundaries are paramount!

```
+----------------+      Untrusted Parameter      +----------------+     Danger Zone
|                |  (e.g., "../../etc/passwd")  |                |  (File System / DB)
|   LLM / Client | ---------------------------> |   MCP Server   | --------------------> [!!!]
|                |                              |  (Must Validate|
+----------------+                              +----------------+
```

### Top Threat Vectors:
1. **Path Traversal**: LLM passes relative path sequences (`../`) to access host OS files outside the intended folder.
2. **SQL Injection**: Concatenating user inputs into raw SQL strings.
3. **Unsanitized Subprocess Execution**: Running shell commands with untrusted arguments.
4. **Information Disclosure via Exceptions**: Returning raw Python traceback dumps that expose database connection URIs or internal server paths.

---

## 2. Hardening Pattern 1: Safe Sandboxed File Paths

Never pass raw user file paths directly to `open()`. Always resolve and verify that the target path remains inside a strict base directory:

```python
from pathlib import Path

BASE_DIR = Path("/app/safe_storage").resolve()

def get_safe_path(user_input_path: str) -> Path:
    # Resolve target path relative to base directory
    target = (BASE_DIR / user_input_path).resolve()
    
    # Check if target path stays strictly inside BASE_DIR
    if not target.is_relative_to(BASE_DIR):
        raise SecurityError(f"Access Denied: Path '{user_input_path}' attempts directory traversal outside sandbox!")
        
    return target
```

---

## 3. Hardening Pattern 2: Parameterized Database Queries

Never use string formatting (`f"SELECT * FROM users WHERE name = '{input}'"`) for SQL queries in tools. Always use parameterized positional placeholders:

```python
# ❌ VULNERABLE TO SQL INJECTION:
# cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ HARDENED PARAMETERIZED QUERY:
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

---

## 4. Hardening Pattern 3: Exception Boundaries

When an unexpected exception occurs inside a tool handler, catch internal exceptions and return clean, user-friendly error messages that do not expose sensitive infrastructure details:

```python
@mcp.tool()
def safe_database_search(query_term: str) -> str:
    try:
        # Internal DB execution...
        return perform_query(query_term)
    except Exception as internal_err:
        # Log internal stack trace to server logs silently
        logger.error(f"Internal DB failure: {internal_err}", exc_info=True)
        # Return sanitized error to MCP client
        raise RuntimeError("Database query failed due to invalid search parameters.")
```

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will test:
1. `read_sandboxed_file`: Sandboxed file reader rejecting `../` traversal attacks.
2. `search_user_records`: Parameterized SQLite search neutralizing `' OR '1'='1` injection.
3. Interactive attack suite verifying security rejections.

### To Run the Hands-on Script:
```bash
python 08_security/hands_on.py
```
