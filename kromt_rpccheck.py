#!/usr/bin/env python3
"""
KROMT RPC Health Checker
------------------------
Measure latency and basic health of public Ethereum JSON-RPC endpoints.
Local client-side tool. No credentials.

https://kromt.xyz  |  https://github.com/kromtxyz
"""

from __future__ import annotations

import time
from typing import List, Optional

import click
import requests
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_ENDPOINTS = [
    ("Robinhood Chain", "https://rpc.mainnet.chain.robinhood.com"),
    ("Ethereum (Llama)", "https://eth.llamarpc.com"),
    ("Base", "https://mainnet.base.org"),
    ("Arbitrum", "https://arb1.arbitrum.io/rpc"),
    ("Optimism", "https://mainnet.optimism.io"),
]


def check_endpoint(url: str, timeout: float = 8.0) -> dict:
    payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
    start = time.perf_counter()
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        elapsed = (time.perf_counter() - start) * 1000
        if r.status_code != 200:
            return {"ok": False, "latency_ms": elapsed, "error": f"HTTP {r.status_code}"}
        data = r.json()
        if "error" in data:
            return {"ok": False, "latency_ms": elapsed, "error": str(data["error"])}
        block_hex = data.get("result", "0x0")
        block = int(block_hex, 16)
        return {"ok": True, "latency_ms": elapsed, "block": block}
    except requests.Timeout:
        return {"ok": False, "latency_ms": timeout * 1000, "error": "timeout"}
    except Exception as exc:
        return {"ok": False, "latency_ms": 0, "error": str(exc)}


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--rpc", multiple=True, help="Additional RPC URL to check")
@click.option("--timeout", default=8.0, show_default=True, help="Request timeout in seconds")
@click.option("--only-defaults/--no-defaults", default=True, help="Include built-in public endpoints")
def main(rpc: tuple[str, ...], timeout: float, only_defaults: bool) -> None:
    """
    Check latency and health of public JSON-RPC endpoints.
    """
    endpoints: List[tuple[str, str]] = []
    if only_defaults:
        endpoints.extend(DEFAULT_ENDPOINTS)
    for u in rpc:
        endpoints.append((u, u))

    if not endpoints:
        console.print("[red]No endpoints to check[/red]")
        return

    console.print("\n[bold cyan]KROMT RPC Health Checker[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name / URL", style="cyan", overflow="fold")
    table.add_column("Status", justify="center")
    table.add_column("Latency", justify="right")
    table.add_column("Block", justify="right")

    for name, url in endpoints:
        result = check_endpoint(url, timeout=timeout)
        if result["ok"]:
            status = "[green]OK[/green]"
            latency = f"{result['latency_ms']:.0f} ms"
            block = str(result["block"])
        else:
            status = "[red]FAIL[/red]"
            latency = f"{result.get('latency_ms', 0):.0f} ms"
            block = result.get("error", "error")
        table.add_row(name if name != url else url, status, latency, block)

    console.print(table)
    console.print(
        "\n[dim]Local client-side tool. Public endpoints only. No credentials.[/dim]\n"
        "[dim]KROMT · https://kromt.xyz · https://github.com/kromtxyz[/dim]\n"
    )


if __name__ == "__main__":
    main()
