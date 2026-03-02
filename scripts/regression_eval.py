from __future__ import annotations

import argparse
import json
from pathlib import Path

from tref import ask


def _contains_any(haystack: list[str], needles: list[str]) -> bool:
    h = "\n".join(haystack).lower()
    return all(n.lower() in h for n in needles)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run tref golden-query regression suite")
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--index-root", type=Path, default=Path("/tmp/tref-indexes-upgrade"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    cases = suite.get("cases", [])
    report: dict[str, object] = {"total": len(cases), "passed": 0, "failed": 0, "results": []}

    for case in cases:
      payload = ask(
          case["query"],
          library=case.get("library"),
          version=case.get("version"),
          json_mode=True,
          index_root=args.index_root,
          freshness_policy="offline-only",
      )
      guidance = payload.get("guidance") or {}
      top_item = guidance.get("command_or_function") or (payload.get("results") or [{}])[0].get("item")
      ok = top_item == case.get("expected_top_item")
      failures: list[str] = []
      if not ok:
          failures.append(f"top_item expected={case.get('expected_top_item')} got={top_item}")

      expect_alts = case.get("expected_alternatives_contains") or []
      if expect_alts:
          alts = guidance.get("alternatives") or []
          alt_names = [str(alt.get("name", "")) for alt in alts]
          if not _contains_any(alt_names, list(expect_alts)):
              failures.append("alternatives missing expected entries")

      if failures:
          report["failed"] = int(report["failed"]) + 1
          status = "failed"
      else:
          report["passed"] = int(report["passed"]) + 1
          status = "passed"

      report["results"].append(
          {
              "id": case.get("id"),
              "status": status,
              "top_item": top_item,
              "expected_top_item": case.get("expected_top_item"),
              "failures": failures,
              "confidence": guidance.get("confidence"),
          }
      )

    out = json.dumps(report, indent=2)
    print(out)
    if args.output:
        args.output.write_text(out + "\n", encoding="utf-8")

    return 0 if int(report["failed"]) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
