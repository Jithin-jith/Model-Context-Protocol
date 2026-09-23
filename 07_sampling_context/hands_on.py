"""
Module 07: Sampling, Context & Notifications - Hands-on Implementation
======================================================================
This script demonstrates:
1. Injecting `Context` into FastMCP tools.
2. Emitting real-time progress updates (`report_progress`).
3. Streaming contextual logging messages (`info`, `warning`, `error`).
4. Handling request context safely across direct test calls & client sessions.
"""

import asyncio
import sys

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP Server
mcp = FastMCP(
    name="Module07-SamplingContext-Server",
    instructions="Demonstrates real-time progress reporting, logging, and sampling context."
)

async def safe_log_info(ctx: Context, message: str):
    """Safely logs info message via ctx if session context is active."""
    try:
        await ctx.info(message)
    except Exception:
        # Fallback for direct tool invocations outside protocol session
        print(f"  [Direct Log Output]: {message}")

async def safe_report_progress(ctx: Context, progress: float, total: float):
    """Safely reports progress via ctx if session context is active."""
    try:
        await ctx.report_progress(progress, total)
    except Exception:
        pass

# --- 1. Long Running Tool with Progress & Logging ---
@mcp.tool()
async def process_batch_files(file_count: int, ctx: Context) -> str:
    """
    Simulates processing a batch of files while reporting progress to the client.

    Args:
        file_count: Number of simulated files to process (1 to 20).
    """
    if file_count < 1 or file_count > 20:
        raise ValueError("File count must be between 1 and 20.")

    await safe_log_info(ctx, f"Initializing batch job for {file_count} file(s)...")

    for i in range(1, file_count + 1):
        # Simulate work delay
        await asyncio.sleep(0.01)

        # Emit progress update (current, total)
        await safe_report_progress(ctx, float(i), float(file_count))
        
        if i % 5 == 0 or i == file_count:
            await safe_log_info(ctx, f"Progress Milestone: Processed {i}/{file_count} files.")

    await safe_log_info(ctx, "Batch processing complete.")
    return f"Completed batch processing of {file_count} files successfully."

# --- 2. Tool with Severe Warning Logs ---
@mcp.tool()
async def check_disk_health(volume: str, ctx: Context) -> str:
    """
    Checks disk health status and logs warnings if space is low.

    Args:
        volume: Drive volume letter or name (e.g. 'C:', '/dev/sda1').
    """
    await safe_log_info(ctx, f"Inspecting volume: '{volume}'...")
    
    # Simulated disk check logic
    free_gb = 4.2
    total_gb = 500.0

    if free_gb < 10.0:
        try:
            await ctx.warning(f"CRITICAL STORAGE WARNING: Low disk space on {volume}! Only {free_gb} GB remaining.")
        except Exception:
            print(f"  [Direct Warning Output]: Low disk space on {volume}! Only {free_gb} GB remaining.")

    return f"Volume {volume} check finished. Free Space: {free_gb} GB / {total_gb} GB"

# --- 3. Verification Harness ---
async def run_verification():
    print("==================================================")
    print("🚀 Module 07: Sampling & Context Hands-On Verification")
    print("==================================================")

    print("\n--- 1. Testing Batch Tool with Progress & Safe Context Handling ---")
    res1 = await mcp.call_tool("process_batch_files", {"file_count": 10})
    print(f"Result:\n  {res1[0][0].text}")

    print("\n--- 2. Testing Disk Health Tool with Context Warnings ---")
    res2 = await mcp.call_tool("check_disk_health", {"volume": "C:"})
    print(f"Result:\n  {res2[0][0].text}")

    print("\n==================================================")
    print("✅ Module 07 Verification Complete!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        mcp.run()
    else:
        asyncio.run(run_verification())
