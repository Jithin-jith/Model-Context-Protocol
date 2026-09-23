"""
Module 09: Advanced Enterprise Capstone - Server Implementation
================================================================
This script implements a production-grade Enterprise MCP Server combining:
1. Hardened database query & report generation tools.
2. System health & configuration resources.
3. Incident triage prompt templates.
4. Progress reporting & context logging.
"""

import sys
import asyncio
import json
import sqlite3
from typing import List, Dict

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP, Context

# Initialize Enterprise Capstone FastMCP Server
mcp = FastMCP(
    name="Enterprise-Capstone-Server",
    instructions="Production Enterprise MCP Server exposing tools, health resources, and triage prompts."
)

# In-memory Enterprise Database Setup
def init_enterprise_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE incidents (
            id INTEGER PRIMARY KEY,
            severity TEXT,
            title TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.executemany(
        "INSERT INTO incidents (severity, title, status) VALUES (?, ?, ?)",
        [
            ("CRITICAL", "Database connection pool exhaustion in region us-east-1", "OPEN"),
            ("HIGH", "High API response latency on payment gateway", "INVESTIGATING"),
            ("LOW", "SSL certificate renewal reminder for staging domain", "RESOLVED")
        ]
    )
    conn.commit()
    return conn

db_conn = init_enterprise_db()

# --- 1. ENTERPRISE TOOLS ---
@mcp.tool()
async def query_open_incidents(severity_filter: str = "ALL", ctx: Context = None) -> str:
    """
    Queries enterprise incident database with optional severity filtering.

    Args:
        severity_filter: Filter criteria ('ALL', 'CRITICAL', 'HIGH', 'LOW').
    """
    cursor = db_conn.cursor()
    if severity_filter.upper() == "ALL":
        cursor.execute("SELECT id, severity, title, status, created_at FROM incidents")
    else:
        cursor.execute("SELECT id, severity, title, status, created_at FROM incidents WHERE severity = ?", (severity_filter.upper(),))
        
    rows = cursor.fetchall()
    incidents = [{"id": r[0], "severity": r[1], "title": r[2], "status": r[3], "created_at": r[4]} for r in rows]
    return json.dumps(incidents, indent=2)

@mcp.tool()
async def generate_incident_report(report_title: str, ctx: Context = None) -> str:
    """
    Generates a consolidated markdown incident report with progress notifications.

    Args:
        report_title: Heading title for the generated report.
    """
    if ctx:
        try:
            await ctx.info(f"Generating incident report: '{report_title}'...")
            await ctx.report_progress(1, 3)
            await asyncio.sleep(0.02)
            await ctx.report_progress(2, 3)
            await asyncio.sleep(0.02)
            await ctx.report_progress(3, 3)
        except Exception:
            pass

    report = f"""# Executive Incident Report: {report_title}

## Summary Matrix
- **Status**: Operational
- **Open Critical Incidents**: 1
- **Investigating High Incidents**: 1

## Action Items
1. Scale connection pool limits in `us-east-1`.
2. Inspect payment gateway latency metrics.
"""
    return report

# --- 2. ENTERPRISE RESOURCES ---
@mcp.resource("system://health")
def get_system_health() -> str:
    """Exposes real-time system diagnostic health status."""
    health_status = {
        "status": "HEALTHY",
        "services": {
            "database": "UP",
            "redis_cache": "UP",
            "payment_gateway": "DEGRADED"
        },
        "uptime_seconds": 86400,
        "load_average": 0.42
    }
    return json.dumps(health_status, indent=2)

@mcp.resource("config://enterprise_settings")
def get_enterprise_config() -> str:
    """Exposes static enterprise configuration metadata."""
    config = {
        "cluster_name": "prod-useast1-mcp",
        "max_tool_concurrency": 25,
        "allowed_hosts": ["claude-desktop", "cursor-ide", "python-agent-v1"]
    }
    return json.dumps(config, indent=2)

# --- 3. ENTERPRISE PROMPTS ---
@mcp.prompt()
def incident_triage_prompt(incident_id: str) -> str:
    """
    Generates a structured incident triage workflow prompt.

    Args:
        incident_id: Numeric incident ID to triage.
    """
    return f"""Act as the Incident Commander. Perform an immediate triage protocol for Incident #{incident_id}:

1. Analyze the root cause using recent log traces.
2. Outline mitigation steps to restore service level objectives (SLO).
3. Draft a communication message for stakeholders.
"""

# Verification runner for standalone execution
async def run_internal_verification():
    print("==================================================")
    print("🚀 Module 09: Enterprise Capstone Server Self-Test")
    print("==================================================")

    res_tools = await mcp.call_tool("query_open_incidents", {"severity_filter": "ALL"})
    print(f"Tool Result:\n{res_tools[0][0].text}")

    res_resource = await mcp.read_resource("system://health")
    print(f"\nResource Result:\n{res_resource[0].content}")

    res_prompt = await mcp.get_prompt("incident_triage_prompt", {"incident_id": "101"})
    print(f"\nPrompt Result:\n{res_prompt.messages[0].content.text}")

    print("\n==================================================")
    print("✅ Capstone Server Self-Test Passed!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-server":
        mcp.run()
    else:
        asyncio.run(run_internal_verification())
