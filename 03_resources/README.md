# Module 03: MCP Resources - Data Context & Dynamic Templates

## 🎯 Learning Objectives
By the end of this module, you will understand:
- The role of **Resources** as read-only context providers in MCP.
- Designing RFC 3986 compliant **Resource URIs**.
- Static Resources vs. Dynamic Parameterized **Resource Templates**.
- MIME types, resource listing, and payload structures.
- Resource Subscriptions and Change Notifications (`resources/subscribe`, `resources/updated`).

---

## 1. What are Resources?

While **Tools** allow models to take actions (side-effects allowed), **Resources** provide passive, read-only context to models and users. Think of Resources as files, database views, system metrics, or configuration snapshots exposed over standard URI endpoints.

```
+---------------+             1. resources/list            +---------------+
|               | ---------------------------------------> |               |
|               | <--------------------------------------- |               |
|               |       2. Available Resource URIs         |               |
|  MCP Client   |                                          |  MCP Server   |
|   (or Host)   |             3. resources/read            |               |
|               | ---------------------------------------> |               |
|               | <--------------------------------------- |               |
|               |       4. Resource Content + MIME         |               |
+---------------+                                          +---------------+
```

---

## 2. Resource URIs and MIME Types

Every resource in MCP is uniquely identified by a URI string and associated with a MIME type.

### Examples of Common Resource URIs:
- `file:///var/log/application.log` (`text/plain`)
- `postgres://database/tables/customers` (`application/json`)
- `system://metrics/cpu` (`application/json`)
- `docs://api/v1/openapi.json` (`application/json`)

---

## 3. Static Resources vs. Dynamic Resource Templates

### A. Static Resources
Fixed URIs where the content is directly available at a constant address:

```python
@mcp.resource("config://app")
def get_app_config() -> str:
    """Returns static application settings JSON."""
    return json.dumps({"env": "production", "debug": False, "version": "1.4.0"})
```

### B. Dynamic Resource Templates
URI patterns containing template parameters enclosed in `{brackets}`. This allows a single handler to service infinite dynamic endpoints:

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile_resource(user_id: str) -> str:
    """
    Fetches user profile context dynamically by ID.
    
    URI Pattern: users://{user_id}/profile
    """
    # user_id is automatically extracted from the request URI!
    user_db = {"usr_101": "Alice (Admin)", "usr_102": "Bob (Developer)"}
    return user_db.get(user_id, f"User '{user_id}' not found.")
```

---

## 4. Resource Subscriptions & Live Updates

MCP allows clients to subscribe to specific resource URIs using the `resources/subscribe` request.

When underlying data changes on the server, the server broadcasts a `notifications/resources/updated` message containing the updated URI. The client can then re-fetch the latest content:

```
Client                             Server
  |                                   |
  |--- resources/subscribe(uri) ----->|
  |<-- OK ----------------------------|
  |                                   |  (Data mutates on Server)
  |<-- notifications/resources/updated|
  |                                   |
  |--- resources/read(uri) ---------->|
  |<-- updated text content ----------|
```

---

## 🛠️ Hands-on Code Overview

In [`hands_on.py`](./hands_on.py), you will build and test:
1. Static configuration resource (`config://system_settings`).
2. Dynamic SQLite user profile template (`sqlite://users/{user_id}`).
3. Dynamic system log file reader resource (`logs://application.log`).
4. In-memory reading and parameter extraction verification.

### To Run the Hands-on Script:
```bash
python 03_resources/hands_on.py
```
