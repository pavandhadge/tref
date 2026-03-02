from __future__ import annotations

import json
import statistics
import time
import tracemalloc
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from tref.api import ask
from tref.config import (
    CUSTOM_INDEX_ROOT,
    DEFAULT_FRESHNESS_POLICY,
    INDEX_ROOT,
    get_remote_settings,
    load_remote_config,
    reset_remote_config,
    save_remote_config,
)
from tref.errors import TrefError
from tref.indexer import build_indexes
from tref.kb import parse_library_version
from tref.updater import freshness_status, update_indexes

app = typer.Typer(
    add_completion=True,
    no_args_is_help=False,
    help="tref: offline-first reference retrieval for versioned developer docs.",
)
console = Console()


class ExitCodes:
    OK = 0
    ERROR = 1
    VALIDATION = 2
    UPDATE = 3
    DETECTION = 4


def _print_results(payload: dict) -> None:
    if not payload["results"]:
        console.print("[yellow]No results found.[/yellow]")
        return

    fresh = payload.get("freshness") or {}
    status_str = "fresh" if fresh.get("fresh", False) else "stale/unverified"
    header = f"{payload['library']}@{payload['version']}  query: {payload['query']}\nindex freshness: {status_str}"
    console.print(Panel(header, title="tref", border_style="cyan"))

    prov = payload.get("provenance") or {}
    if prov:
        prov_line = (
            f"build_hash={prov.get('build_hash')} kb_commit={prov.get('kb_commit')} "
            f"model={prov.get('embedding_model')} policy={prov.get('freshness_policy')}"
        )
        console.print(f"[blue]provenance:[/blue] {prov_line}")

    for warning in payload.get("warnings", []):
        console.print(f"[yellow]warning:[/yellow] {warning}")

    for idx, result in enumerate(payload["results"], start=1):
        title = f"{idx}. {result['item']}  score={result['score']:.3f}"
        body = f"[bold]Signature:[/bold] {result['signature']}\n[bold]Citation:[/bold] {result['citation']}"
        console.print(Panel(body, title=title, border_style="green"))
        console.print(Syntax(result["text"], "markdown", theme="ansi_dark", word_wrap=True))

    if payload.get("answer"):
        console.print(Panel(payload["answer"], title="LLM Answer", border_style="magenta"))


def _exit_for_error(exc: Exception) -> None:
    if isinstance(exc, TrefError):
        console.print(f"[red]{exc.code}[/red]: {exc.message}")
        if exc.code.startswith("UPDATE"):
            raise typer.Exit(code=ExitCodes.UPDATE)
        if exc.code.startswith("DETECT"):
            raise typer.Exit(code=ExitCodes.DETECTION)
        raise typer.Exit(code=ExitCodes.VALIDATION)
    console.print(f"[red]ERROR[/red]: {exc}")
    raise typer.Exit(code=ExitCodes.ERROR)


def _run_chat(
    library: str,
    version: Optional[str],
    llm: bool,
    model: str,
    index_root: Optional[Path],
    strict_fresh: bool,
    freshness_policy: str,
) -> None:
    console.print(f"Chat mode for [bold]{library}@{version or 'latest'}[/bold]. Type 'exit' to quit.")
    while True:
        query = typer.prompt("query").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        try:
            payload = ask(
                query,
                library=library,
                version=version,
                llm=llm,
                llm_model=model,
                strict_fresh=strict_fresh,
                freshness_policy=freshness_policy,
                json_mode=True,
                index_root=index_root,
            )
        except Exception as exc:
            _exit_for_error(exc)
        _print_results(payload)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    query_parts: list[str] = typer.Argument(None, metavar="[LIB@VER] QUERY"),
    library: Optional[str] = typer.Option(None, "--library", "-l"),
    version: Optional[str] = typer.Option(None, "--version", "-v"),
    json_output: bool = typer.Option(False, "--json", help="Return JSON output for agents."),
    top_k: int = typer.Option(5, "--top-k", min=1, max=20),
    llm: bool = typer.Option(False, "--llm", help="Generate final answer via Ollama."),
    chat: bool = typer.Option(False, "--chat", help="Interactive multi-query mode."),
    model: str = typer.Option("llama3.1:8b-instruct", "--model"),
    strict_fresh: bool = typer.Option(False, "--strict-fresh", help="Fail when freshness cannot be ensured."),
    freshness_policy: str = typer.Option(
        DEFAULT_FRESHNESS_POLICY,
        "--freshness-policy",
        help="strict|warn|offline-only",
    ),
    no_autodetect: bool = typer.Option(False, "--no-autodetect", help="Disable query-based library detection."),
    index_root: Optional[Path] = typer.Option(None, "--index-root", help="Override index root path."),
) -> None:
    if ctx.invoked_subcommand:
        return

    if not query_parts and not chat:
        console.print(ctx.get_help())
        raise typer.Exit(code=ExitCodes.OK)

    if query_parts and not library:
        parsed_library, parsed_version = parse_library_version(query_parts[0])
        if parsed_library:
            library = parsed_library
            version = version or parsed_version
            query_parts = query_parts[1:]

    if chat:
        if not library:
            raise typer.BadParameter("chat mode requires --library or LIB@VER prefix")
        _run_chat(
            library=library,
            version=version,
            llm=llm,
            model=model,
            index_root=index_root,
            strict_fresh=strict_fresh,
            freshness_policy=freshness_policy,
        )
        return

    query = " ".join(query_parts).strip()
    try:
        payload = ask(
            query,
            library=library,
            version=version,
            top_k=top_k,
            json_mode=True,
            llm=llm,
            llm_model=model,
            strict_fresh=strict_fresh,
            freshness_policy=freshness_policy,
            no_autodetect=no_autodetect,
            index_root=index_root,
        )
    except Exception as exc:
        _exit_for_error(exc)

    if json_output:
        console.print_json(json.dumps(payload))
        return
    _print_results(payload)


@app.command("update")
def update_cmd(
    strict_verify: bool = typer.Option(True, "--strict-verify/--no-strict-verify"),
) -> None:
    """Download latest prebuilt indexes from GitHub Releases."""
    try:
        update_indexes(silent=False, strict_verify=strict_verify)
    except Exception as exc:
        _exit_for_error(exc)


@app.command("status")
def status_cmd() -> None:
    """Show index freshness and remote state."""
    payload = {
        "freshness": freshness_status(),
        "remote": get_remote_settings(),
    }
    console.print_json(json.dumps(payload, indent=2))


@app.command("doctor")
def doctor_cmd() -> None:
    """Run local diagnostics for trust/readiness."""
    status = freshness_status()
    remote = get_remote_settings()
    table = Table(title="tref doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Details")

    table.add_row("Freshness", "OK" if status.get("fresh") else "WARN", json.dumps(status))
    table.add_row("Verification", "OK" if status.get("verified") else "WARN", "verified flag from last update")
    table.add_row("Remote", "OK", json.dumps(remote))
    console.print(table)


@app.command("bench")
def bench_cmd(
    query: str = typer.Argument(..., help="Benchmark query text"),
    library: Optional[str] = typer.Option(None, "--library", "-l"),
    version: Optional[str] = typer.Option(None, "--version", "-v"),
    runs: int = typer.Option(20, "--runs", min=5, max=500),
    index_root: Optional[Path] = typer.Option(None, "--index-root"),
) -> None:
    """Benchmark query latency and peak memory usage."""
    latencies_ms: list[float] = []
    tracemalloc.start()

    for _ in range(runs):
        start = time.perf_counter()
        ask(
            query,
            library=library,
            version=version,
            json_mode=True,
            freshness_policy="offline-only",
            index_root=index_root,
        )
        elapsed = (time.perf_counter() - start) * 1000
        latencies_ms.append(elapsed)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    payload = {
        "runs": runs,
        "p50_ms": round(statistics.median(latencies_ms), 2),
        "p95_ms": round(sorted(latencies_ms)[int(runs * 0.95) - 1], 2),
        "min_ms": round(min(latencies_ms), 2),
        "max_ms": round(max(latencies_ms), 2),
        "mem_current_mb": round(current / (1024 * 1024), 3),
        "mem_peak_mb": round(peak / (1024 * 1024), 3),
    }
    console.print_json(json.dumps(payload, indent=2))


remote_app = typer.Typer(help="Manage remote KB/release endpoints.")
app.add_typer(remote_app, name="remote")


@remote_app.command("show")
def remote_show() -> None:
    console.print_json(json.dumps(get_remote_settings(), indent=2))


@remote_app.command("set")
def remote_set(
    releases_api_url: Optional[str] = typer.Option(None, "--releases-api-url"),
    kb_manifest_url: Optional[str] = typer.Option(None, "--kb-manifest-url"),
    release_asset_name: Optional[str] = typer.Option(None, "--release-asset-name"),
    release_checksum_asset_name: Optional[str] = typer.Option(None, "--release-checksum-asset-name"),
    release_signature_asset_name: Optional[str] = typer.Option(None, "--release-signature-asset-name"),
) -> None:
    current = load_remote_config()
    updates = {}
    if releases_api_url:
        updates["releases_api_url"] = releases_api_url
    if kb_manifest_url:
        updates["kb_manifest_url"] = kb_manifest_url
    if release_asset_name:
        updates["release_asset_name"] = release_asset_name
    if release_checksum_asset_name:
        updates["release_checksum_asset_name"] = release_checksum_asset_name
    if release_signature_asset_name:
        updates["release_signature_asset_name"] = release_signature_asset_name
    if not updates:
        raise typer.BadParameter("No values provided to set.")
    current.update(updates)
    save_remote_config(current)
    console.print("[green]Remote configuration updated.[/green]")
    console.print_json(json.dumps(get_remote_settings(), indent=2))


@remote_app.command("reset")
def remote_reset() -> None:
    reset_remote_config()
    console.print("[green]Remote configuration reset to defaults/env.[/green]")
    console.print_json(json.dumps(get_remote_settings(), indent=2))


@app.command("build-index")
def build_index_cmd(
    kb_path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    output: Path = typer.Option(CUSTOM_INDEX_ROOT, "--output", "-o"),
) -> None:
    """Build FAISS indexes from KB markdown files."""
    try:
        summary = build_indexes(kb_root=kb_path, output_root=output)
    except Exception as exc:
        _exit_for_error(exc)
    console.print_json(json.dumps(summary))


def run() -> None:
    app()
