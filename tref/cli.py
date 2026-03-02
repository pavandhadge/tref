from __future__ import annotations

import json
import re
import shlex
import subprocess
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from tref.api import ask
from tref.config import (
    CUSTOM_INDEX_ROOT,
    DEFAULT_FRESHNESS_POLICY,
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


def _one_line(text: str, max_len: int = 120) -> str:
    s = " ".join(text.split())
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _short_block(text: str, max_lines: int = 6) -> str:
    lines = [ln.rstrip() for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines]) + "\n..."


def _extract_code_block(text: str) -> tuple[str, str] | None:
    lines = text.splitlines()
    start = None
    lang = ""
    for i, ln in enumerate(lines):
        if ln.strip().startswith("```"):
            start = i
            fence = ln.strip()
            lang = fence[3:].strip().split()[0] if len(fence) > 3 else ""
            break
    if start is None:
        return None
    end = None
    for j in range(start + 1, len(lines)):
        if lines[j].strip().startswith("```"):
            end = j
            break
    if end is None:
        return None
    body = "\n".join(lines[start + 1 : end]).strip()
    if not body:
        return None
    return (lang or "text", body)


def _clean_bullet_line(text: str) -> str:
    s = " ".join(text.replace("\n", " ").split())
    while s.startswith("- "):
        s = s[2:].strip()
    return s


def _two_line_info(text: str) -> str:
    cleaned = []
    in_code = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line:
            continue
        if line.startswith("#"):
            continue
        cleaned.append(_clean_bullet_line(line))
    return _short_block("\n".join(cleaned), max_lines=2)


def _print_section(title: str) -> None:
    console.print("")
    console.print(f"[bold]{title}[/bold]")
    console.print("─" * 44)


def _kv(label: str, value: str) -> None:
    console.print(f"[bold]{label}[/bold]  {value}")


def _parse_alternative_text(name: str, why: str) -> tuple[str, str]:
    option = (name or "").strip()
    reason = (why or "").strip()
    m = re.match(r"^`([^`]+)`\s*(.*)$", option)
    if m:
        option = m.group(1).strip()
        tail = m.group(2).strip()
        if tail and not reason:
            reason = tail
    if not reason:
        if ". " in option:
            left, right = option.split(". ", 1)
            if "(" in left or "." in left or " " not in left:
                option = left.strip()
                reason = right.strip()
    return option, reason


def _print_code_block(code: str) -> None:
    console.print("```")
    console.print(code)
    console.print("```")


def _print_example_code(lang: str, code: str) -> None:
    syntax_lang = lang if lang and lang != "text" else "text"
    console.print(Syntax(code, syntax_lang, theme="ansi_dark", word_wrap=True))


def _print_results(payload: dict, verbose: bool = False) -> None:
    if not payload["results"]:
        console.print("[yellow]No results found.[/yellow]")
        return

    guidance = payload.get("guidance") or {}
    item_name = str(guidance.get("command_or_function") or payload["results"][0].get("item") or "")
    console.print(f"[bold]{payload['library']}@{payload['version']}[/bold] • [bold]{item_name}[/bold]")

    if payload.get("version_mismatch"):
        req = payload.get("version_requested")
        got = payload.get("version")
        reason = ((payload.get("version_resolution") or {}).get("reason") or "").strip()
        if reason:
            console.print(f"[yellow]Version Notice:[/yellow] Requested '{req}', using '{got}' ({reason}).")
        else:
            console.print(f"[yellow]Version Notice:[/yellow] Requested '{req}', using '{got}'.")

    if guidance:
        _print_section("Description")
        description = str(guidance.get("description") or "").strip()
        if not description:
            preview = guidance.get("preview") or {}
            preview_text = str(preview.get("text") or "").strip()
            description = _two_line_info(preview_text) if preview_text else ""
        if description:
            console.print(description)

        _print_section("Signature")
        console.print(f"[italic]{str(guidance.get('signature') or 'not available')}[/italic]")

        params = guidance.get("parameters") or []
        if params:
            _print_section("Parameters")
            for param in params:
                name = str(param.get("name") or "").strip()
                detail = str(param.get("detail") or "").strip()
                if name and detail:
                    console.print(f"• [bold]{name:<12}[/bold]  {detail}")
                elif name:
                    console.print(f"• [bold]{name}[/bold]")

        returns_text = str(guidance.get("returns_text") or "").strip()
        if not returns_text and guidance.get("returns"):
            r = guidance["returns"]
            returns_text = str(r.get("doc_title") or "").strip()
        if returns_text:
            _print_section("Returns")
            console.print(returns_text)

        cautions = guidance.get("cautions", [])
        if cautions:
            _print_section(f"Gotchas & Version Notes ({payload['version']})")
            caution_limit = len(cautions) if verbose else 5
            for caution in cautions[:caution_limit]:
                ref = caution.get("doc_url")
                suffix = f" [{ref}]" if ref else ""
                console.print(f"• {_one_line(_clean_bullet_line(caution['text']), 220)}")
                if suffix:
                    console.print(f"  [bright_black]ref: {ref}[/bright_black]")

        examples = guidance.get("examples", [])
        if examples:
            _print_section("Examples")
            for idx, example in enumerate(examples[:2], start=1):
                if idx > 1:
                    console.print("")
                ref = example.get("doc_url")
                suffix = f" [{ref}]" if ref else ""
                parsed = _extract_code_block(example["text"])
                console.print(f"[bold]Example {idx}[/bold]")
                if parsed:
                    lang, code = parsed
                    _kv("Language", lang.lower())
                    _print_example_code(lang.lower(), code)
                    if suffix:
                        console.print(f"Source  {ref}")
                else:
                    console.print(f"- {_one_line(example['text'], 180)}{suffix}")

        refs = guidance.get("citations", [])
        if refs:
            _print_section("References")
            refs_limit = len(refs) if verbose else 3
            for ref in refs[:refs_limit]:
                console.print(f"• {ref.get('title')}")
                console.print(f"  {ref.get('url')}")

        source = guidance.get("source") or {}
        source_url = source.get("url")
        if source_url:
            _print_section("Source (local KB)")
            if source.get("title"):
                console.print(str(source.get("title")))
            console.print(str(source_url))
            if source.get("last_updated"):
                console.print(f"(last updated: {source.get('last_updated')})")

        alternatives = guidance.get("alternatives", [])
        if alternatives:
            _print_section(f"Other Good Options In {payload['library']}@{payload['version']}")
            alt_limit = len(alternatives) if verbose else 3
            for alt in alternatives[:alt_limit]:
                name = alt.get("name") or "alternative"
                why = alt.get("why") or ""
                option, reason = _parse_alternative_text(str(name), str(why))
                if reason and "Alternative approach from official docs context." in reason:
                    reason = ""
                if reason:
                    console.print(f"• {option}  ->  {reason}")
                else:
                    console.print(f"• {option}")

    if verbose:
        _print_section("Preview")
        for idx, result in enumerate(payload["results"][:3], start=1):
            console.print(
                f"{idx}. {result['item']} ({result.get('section', '')}) confidence={result['confidence']:.3f}"
            )
            if result.get("doc_url"):
                console.print(f"source: {result.get('doc_url')}")
            console.print(result["text"])

    if payload.get("answer"):
        _print_section("LLM Answer")
        console.print(payload["answer"])

    notices = payload.get("warnings") or []
    if notices:
        _print_section("Notices")
        for msg in notices:
            console.print(f"• {msg}")

    full_doc = payload.get("full_document")
    if full_doc:
        _print_section("Documentation Dump")
        _kv("Item", str(full_doc.get("item") or ""))
        sections = full_doc.get("sections") or []
        for sec in sections:
            sec_name = sec.get("section", "")
            console.print(f"\n[bold]{sec_name}[/bold]")
            text = sec.get("text", "")
            parsed = _extract_code_block(text)
            if parsed:
                lang, code = parsed
                _kv("Language", lang)
                _print_code_block(code)
            else:
                console.print(_short_block(text, max_lines=16 if verbose else 8))


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


def _execute_query(
    query_tokens: list[str],
    library: Optional[str],
    version: Optional[str],
    json_output: bool,
    top_k: int,
    llm: bool,
    model: str,
    strict_fresh: bool,
    freshness_policy: str,
    no_autodetect: bool,
    verbose: bool,
    full_doc: bool,
    lang: Optional[str],
    index_root: Optional[Path],
) -> None:
    query_text = " ".join(query_tokens).strip()
    if not query_text:
        console.print(app.get_help(typer.Context(app)))
        raise typer.Exit(code=ExitCodes.OK)

    if query_tokens and not library:
        parsed_library, parsed_version = parse_library_version(query_tokens[0])
        if parsed_library:
            library = parsed_library
            version = version or parsed_version
            query_tokens = query_tokens[1:]
            query_text = " ".join(query_tokens).strip()

    try:
        payload = ask(
            query_text,
            library=library,
            version=version,
            top_k=top_k,
            json_mode=True,
            llm=llm,
            llm_model=model,
            strict_fresh=strict_fresh,
            freshness_policy=freshness_policy,
            no_autodetect=no_autodetect,
            include_full_doc=full_doc,
            preferred_language=lang,
            index_root=index_root,
        )
    except Exception as exc:
        _exit_for_error(exc)

    if json_output:
        console.print_json(json.dumps(payload))
        return
    _print_results(payload, verbose=verbose)


def _run_chat(
    library: str,
    version: Optional[str],
    llm: bool,
    model: str,
    index_root: Optional[Path],
    strict_fresh: bool,
    freshness_policy: str,
    verbose: bool,
    full_doc: bool,
    lang: Optional[str],
) -> None:
    console.print(f"Chat mode for [bold]{library}@{version or 'latest'}[/bold]. Type 'exit' to quit.")
    while True:
        query = typer.prompt("query").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        _execute_query(
            [query],
            library,
            version,
            json_output=False,
            top_k=5,
            llm=llm,
            model=model,
            strict_fresh=strict_fresh,
            freshness_policy=freshness_policy,
            no_autodetect=False,
            verbose=verbose,
            full_doc=full_doc,
            lang=lang,
            index_root=index_root,
        )


def _parse_on_off(value: str) -> bool:
    v = value.strip().lower()
    if v in {"on", "true", "1", "yes"}:
        return True
    if v in {"off", "false", "0", "no"}:
        return False
    raise ValueError("expected on/off")


def _run_live(
    library: Optional[str],
    version: Optional[str],
    llm: bool,
    model: str,
    index_root: Optional[Path],
    strict_fresh: bool,
    freshness_policy: str,
    verbose: bool,
    full_doc: bool,
    lang: Optional[str],
    top_k: int,
) -> None:
    state = {
        "library": library,
        "version": version,
        "llm": llm,
        "model": model,
        "strict_fresh": strict_fresh,
        "freshness_policy": freshness_policy,
        "verbose": verbose,
        "full_doc": full_doc,
        "lang": lang,
        "top_k": top_k,
    }

    console.print("[bold]tref live[/bold] active. Type ':help' for commands, ':exit' to quit.")
    while True:
        prompt = "tref[live]"
        line = typer.prompt(prompt, prompt_suffix=" > ").strip()
        if not line:
            continue

        if line in {":exit", ":quit", "exit", "quit", "q"}:
            break

        if line == ":help":
            console.print(
                "\n".join(
                    [
                        "Live commands:",
                        "  :help",
                        "  :exit",
                        "  :context                       # show current session settings",
                        "  :set llm <on|off>",
                        "  :set model <ollama-model>",
                        "  :set lang <name|auto>",
                        "  :set topk <1-20>",
                        "  :set verbose <on|off>",
                        "  :set full-doc <on|off>",
                        "  :set policy <strict|warn|offline-only>",
                        "",
                        "Query format examples:",
                        "  git@2.44 create a new branch and switch",
                        "  git@2.44 create a new branch --lang bash",
                        "  pandas@2.2 groupby multiple columns --top-k 8 --verbose",
                    ]
                )
            )
            continue

        if line == ":context":
            console.print_json(json.dumps(state, indent=2))
            continue

        if line.startswith(":set "):
            try:
                parts = shlex.split(line[len(":set ") :].strip())
            except Exception as exc:
                console.print(f"[red]Invalid set command:[/red] {exc}")
                continue
            if len(parts) < 2:
                console.print("[red]Usage:[/red] :set <key> <value>")
                continue
            key, value = parts[0].lower(), " ".join(parts[1:])
            try:
                if key == "llm":
                    state["llm"] = _parse_on_off(value)
                elif key == "model":
                    state["model"] = value
                elif key == "lang":
                    state["lang"] = None if value.lower() == "auto" else value
                elif key == "topk":
                    iv = int(value)
                    if iv < 1 or iv > 20:
                        raise ValueError("topk must be between 1 and 20")
                    state["top_k"] = iv
                elif key == "verbose":
                    state["verbose"] = _parse_on_off(value)
                elif key in {"full-doc", "fulldoc"}:
                    state["full_doc"] = _parse_on_off(value)
                elif key == "policy":
                    policy = value.lower().strip()
                    if policy not in {"strict", "warn", "offline-only"}:
                        raise ValueError("policy must be strict|warn|offline-only")
                    state["freshness_policy"] = policy
                else:
                    raise ValueError(f"unknown key '{key}'")
                console.print("[green]Updated.[/green]")
            except Exception as exc:
                console.print(f"[red]Set failed:[/red] {exc}")
            continue

        try:
            parts = shlex.split(line)
        except Exception as exc:
            console.print(f"[red]Invalid query input:[/red] {exc}")
            continue
        if not parts:
            continue

        q_library = state["library"]
        q_version = state["version"]
        q_llm = bool(state["llm"])
        q_model = str(state["model"])
        q_verbose = bool(state["verbose"])
        q_full_doc = bool(state["full_doc"])
        q_lang = state["lang"]
        q_top_k = int(state["top_k"])

        # Inline overrides: allow suffix flags in query line.
        filtered: list[str] = []
        i = 0
        while i < len(parts):
            token = parts[i]
            if token == "--lang" and (i + 1) < len(parts):
                q_lang = parts[i + 1]
                i += 2
                continue
            if token == "--model" and (i + 1) < len(parts):
                q_model = parts[i + 1]
                i += 2
                continue
            if token == "--top-k" and (i + 1) < len(parts):
                try:
                    v = int(parts[i + 1])
                    if 1 <= v <= 20:
                        q_top_k = v
                except Exception:
                    pass
                i += 2
                continue
            if token == "--llm":
                q_llm = True
                i += 1
                continue
            if token == "--no-llm":
                q_llm = False
                i += 1
                continue
            if token == "--verbose":
                q_verbose = True
                i += 1
                continue
            if token == "--no-verbose":
                q_verbose = False
                i += 1
                continue
            if token == "--full-doc":
                q_full_doc = True
                i += 1
                continue
            if token == "--no-full-doc":
                q_full_doc = False
                i += 1
                continue
            filtered.append(token)
            i += 1

        query_tokens = filtered
        if query_tokens:
            parsed_library, parsed_version = parse_library_version(query_tokens[0])
            if parsed_library:
                q_library = parsed_library
                q_version = parsed_version or q_version
                query_tokens = query_tokens[1:]
                if not query_tokens:
                    console.print("[red]Query text missing after library@version prefix.[/red]")
                    continue

        _execute_query(
            query_tokens,
            q_library,
            q_version,
            json_output=False,
            top_k=q_top_k,
            llm=q_llm,
            model=q_model,
            strict_fresh=bool(state["strict_fresh"]),
            freshness_policy=str(state["freshness_policy"]),
            no_autodetect=False,
            verbose=q_verbose,
            full_doc=q_full_doc,
            lang=q_lang,
            index_root=index_root,
        )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if not ctx.invoked_subcommand and len(sys.argv) == 1:
        console.print(ctx.get_help())
        raise typer.Exit(code=ExitCodes.OK)


@app.command("query")
def query_cmd(
    query_parts: list[str] = typer.Argument(..., metavar="[LIB@VER] QUERY"),
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
    verbose: bool = typer.Option(False, "--verbose", help="Show full retrieved chunks."),
    full_doc: bool = typer.Option(False, "--full-doc", help="Dump the full document for the best match."),
    lang: Optional[str] = typer.Option(None, "--lang", help="Prefer examples in this language (python|bash|jsx|... )."),
    index_root: Optional[Path] = typer.Option(None, "--index-root", help="Override index root path."),
) -> None:
    if chat:
        if not library:
            raise typer.BadParameter("chat mode requires --library")
        _run_chat(
            library=library,
            version=version,
            llm=llm,
            model=model,
            index_root=index_root,
            strict_fresh=strict_fresh,
            freshness_policy=freshness_policy,
            verbose=verbose,
            full_doc=full_doc,
            lang=lang,
        )
        return

    _execute_query(
        query_parts,
        library,
        version,
        json_output,
        top_k,
        llm,
        model,
        strict_fresh,
        freshness_policy,
        no_autodetect,
        verbose,
        full_doc,
        lang,
        index_root,
    )


@app.command("live")
def live_cmd(
    library: Optional[str] = typer.Option(None, "--library", "-l"),
    version: Optional[str] = typer.Option(None, "--version", "-v"),
    llm: bool = typer.Option(False, "--llm", help="Generate final answer via Ollama."),
    model: str = typer.Option("llama3.1:8b-instruct", "--model"),
    top_k: int = typer.Option(5, "--top-k", min=1, max=20),
    strict_fresh: bool = typer.Option(False, "--strict-fresh", help="Fail when freshness cannot be ensured."),
    freshness_policy: str = typer.Option(
        DEFAULT_FRESHNESS_POLICY,
        "--freshness-policy",
        help="strict|warn|offline-only",
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Show full retrieved chunks."),
    full_doc: bool = typer.Option(False, "--full-doc", help="Dump the full document for the best match."),
    lang: Optional[str] = typer.Option(None, "--lang", help="Prefer examples in this language."),
    index_root: Optional[Path] = typer.Option(None, "--index-root", help="Override index root path."),
) -> None:
    """Persistent interactive mode for continuous tref queries."""
    _run_live(
        library=library,
        version=version,
        llm=llm,
        model=model,
        index_root=index_root,
        strict_fresh=strict_fresh,
        freshness_policy=freshness_policy,
        verbose=verbose,
        full_doc=full_doc,
        lang=lang,
        top_k=top_k,
    )


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
    known = {
        "query",
        "live",
        "update",
        "status",
        "doctor",
        "bench",
        "remote",
        "build-index",
        "eval",
        "--help",
        "-h",
        "--install-completion",
        "--show-completion",
    }
    if len(sys.argv) > 1 and sys.argv[1] not in known:
        sys.argv.insert(1, "query")
    app()


@app.command("eval")
def eval_cmd(
    suite: Path = typer.Option(Path("scripts/golden_queries.json"), "--suite", exists=True, dir_okay=False),
    index_root: Optional[Path] = typer.Option(None, "--index-root"),
    min_pass_rate: float = typer.Option(1.0, "--min-pass-rate", min=0.0, max=1.0),
    output: Optional[Path] = typer.Option(None, "--output", help="Optional path to write JSON report."),
) -> None:
    """Run golden-query regression suite for ranking accuracy."""
    cmd = [sys.executable, "scripts/regression_eval.py", "--suite", str(suite)]
    if index_root:
        cmd.extend(["--index-root", str(index_root)])
    cmd.extend(["--min-pass-rate", str(min_pass_rate)])
    if output:
        cmd.extend(["--output", str(output)])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    if stdout:
        console.print(stdout)
    if stderr:
        console.print(f"[yellow]{stderr}[/yellow]")
    if proc.returncode != 0:
        raise typer.Exit(code=ExitCodes.ERROR)
