from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from tref.api import ask
from tref.config import (
    CUSTOM_INDEX_ROOT,
    INDEX_ROOT,
    get_remote_settings,
    load_remote_config,
    reset_remote_config,
    save_remote_config,
)
from tref.indexer import build_indexes
from tref.kb import parse_library_version
from tref.updater import freshness_status, update_indexes

app = typer.Typer(
    add_completion=True,
    no_args_is_help=False,
    help="tref: offline-first reference retrieval for versioned developer docs.",
)
console = Console()


def _print_results(payload: dict) -> None:
    if not payload["results"]:
        console.print("[yellow]No results found.[/yellow]")
        return

    header = f"{payload['library']}@{payload['version']}  query: {payload['query']}"
    fresh = payload.get("freshness") or {}
    if fresh:
        if fresh.get("fresh", False):
            header = f"{header}\nindex freshness: fresh (age_days={fresh.get('age_days', 0)})"
        else:
            header = f"{header}\nindex freshness: stale/unverified"
    console.print(Panel(header, title="tref", border_style="cyan"))
    for warning in payload.get("warnings", []):
        console.print(f"[yellow]warning:[/yellow] {warning}")
    for idx, result in enumerate(payload["results"], start=1):
        title = f"{idx}. {result['item']}  score={result['score']:.3f}"
        body = f"[bold]Signature:[/bold] {result['signature']}\n[bold]Citation:[/bold] {result['citation']}"
        console.print(Panel(body, title=title, border_style="green"))
        console.print(Syntax(result["text"], "markdown", theme="ansi_dark", word_wrap=True))

    if payload.get("answer"):
        console.print(Panel(payload["answer"], title="LLM Answer", border_style="magenta"))


def _run_chat(
    library: str,
    version: Optional[str],
    llm: bool,
    model: str,
    index_root: Optional[Path],
    strict_fresh: bool,
) -> None:
    console.print(f"Chat mode for [bold]{library}@{version or 'latest'}[/bold]. Type 'exit' to quit.")
    while True:
        query = typer.prompt("query").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        payload = ask(
            query,
            library=library,
            version=version,
            llm=llm,
            llm_model=model,
            strict_fresh=strict_fresh,
            json_mode=True,
            index_root=index_root,
        )
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
    strict_fresh: bool = typer.Option(
        False,
        "--strict-fresh",
        help="Fail if freshness cannot be verified or local index is stale.",
    ),
    index_root: Optional[Path] = typer.Option(None, "--index-root", help="Override index root path."),
) -> None:
    if ctx.invoked_subcommand:
        return

    if not query_parts and not chat:
        console.print(ctx.get_help())
        raise typer.Exit(code=0)

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
        )
        return

    query = " ".join(query_parts).strip()
    payload = ask(
        query,
        library=library,
        version=version,
        top_k=top_k,
        json_mode=True,
        llm=llm,
        llm_model=model,
        strict_fresh=strict_fresh,
        index_root=index_root,
    )

    if json_output:
        console.print_json(json.dumps(payload))
        return
    _print_results(payload)


@app.command("update")
def update_cmd(
    strict_verify: bool = typer.Option(True, "--strict-verify/--no-strict-verify"),
) -> None:
    """Download latest prebuilt indexes from GitHub Releases."""
    update_indexes(silent=False, strict_verify=strict_verify)


@app.command("status")
def status_cmd() -> None:
    """Show index freshness state."""
    payload = {
        "freshness": freshness_status(),
        "remote": get_remote_settings(),
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
    summary = build_indexes(kb_root=kb_path, output_root=output)
    console.print_json(json.dumps(summary))


def run() -> None:
    app()
