#!/usr/bin/env bash
set -u

ROOT="/home/pavan/Programming/tref"
cd "$ROOT"

TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$ROOT/reports/$TS"
CMD_LOG="$OUT_DIR/commands.log"
SUMMARY_JSON="$OUT_DIR/summary.json"
mkdir -p "$OUT_DIR"

echo "tref full evaluation" > "$CMD_LOG"
echo "timestamp: $TS" >> "$CMD_LOG"

run_cmd() {
  local name="$1"
  local cmd="$2"

  echo "" >> "$CMD_LOG"
  echo "===== $name =====" >> "$CMD_LOG"
  echo "CMD: $cmd" >> "$CMD_LOG"

  /usr/bin/time -v -o "$OUT_DIR/${name}.time" bash -lc "$cmd" >> "$CMD_LOG" 2>&1
  local ec=$?
  echo "EXIT_CODE: $ec" >> "$CMD_LOG"
  return 0
}

parse_time_file() {
  local f="$1"
  local elapsed user system cpu rss
  elapsed=$(awk -F': ' '/Elapsed \(wall clock\) time/{print $2}' "$f" | tail -n1)
  user=$(awk -F': ' '/User time \(seconds\)/{print $2}' "$f" | tail -n1)
  system=$(awk -F': ' '/System time \(seconds\)/{print $2}' "$f" | tail -n1)
  cpu=$(awk -F': ' '/Percent of CPU this job got/{print $2}' "$f" | tail -n1)
  rss=$(awk -F': ' '/Maximum resident set size \(kbytes\)/{print $2}' "$f" | tail -n1)
  printf '{"elapsed":"%s","user_sec":"%s","system_sec":"%s","cpu_percent":"%s","max_rss_kb":"%s"}' "$elapsed" "$user" "$system" "$cpu" "$rss"
}

# Environment + build
run_cmd env_info ". .venv/bin/activate && python -V && pip -V && uname -a"
run_cmd compile ". .venv/bin/activate && python -m compileall tref scripts"
run_cmd validate_kb ". .venv/bin/activate && python scripts/validate_kb.py kb"
run_cmd build_indexes ". .venv/bin/activate && python scripts/build_index.py kb --output /tmp/tref-indexes-eval"

# Build package artifacts
run_cmd install_build_tool ". .venv/bin/activate && pip install build"
run_cmd package_build ". .venv/bin/activate && python -m build"
run_cmd dist_sizes "du -sh dist || true && ls -lah dist || true"

# Command suite
run_cmd help ". .venv/bin/activate && python -m tref --help"
run_cmd status ". .venv/bin/activate && python -m tref status"
run_cmd doctor ". .venv/bin/activate && python -m tref doctor"
run_cmd remote_show ". .venv/bin/activate && python -m tref remote show"
run_cmd query_explicit_json ". .venv/bin/activate && python -m tref --index-root /tmp/tref-indexes-eval --freshness-policy offline-only --json pandas@2.2 'groupby multiple columns agg mean'"
run_cmd query_autodetect ". .venv/bin/activate && python -m tref --index-root /tmp/tref-indexes-eval --freshness-policy offline-only 'how to rebase current branch safely'"
run_cmd query_no_autodetect_expected_fail ". .venv/bin/activate && python -m tref --index-root /tmp/tref-indexes-eval --freshness-policy offline-only --no-autodetect 'how to rebase current branch safely'"
run_cmd query_command_form ". .venv/bin/activate && python -m tref query --index-root /tmp/tref-indexes-eval --freshness-policy offline-only --json pandas@2.2 'groupby multiple columns agg mean'"
run_cmd bench ". .venv/bin/activate && python -m tref bench --index-root /tmp/tref-indexes-eval 'groupby multiple columns agg mean' --library pandas --version 2.2 --runs 25"
run_cmd api_python ". .venv/bin/activate && python - << 'PY'
from pathlib import Path
from tref import ask
r = ask('groupby multiple columns agg mean', library='pandas', version='2.2', json_mode=True, index_root=Path('/tmp/tref-indexes-eval'), freshness_policy='offline-only')
print({'library': r['library'], 'version': r['version'], 'results': len(r['results']), 'top_confidence': r['results'][0]['confidence'] if r['results'] else 0})
PY"
run_cmd update_strict_verify ". .venv/bin/activate && python -m tref update --strict-verify"

# Aggregate summary
{
  echo "{";
  echo "  \"report_dir\": \"$OUT_DIR\",";
  echo "  \"generated_at\": \"$(date -Iseconds)\",";
  echo "  \"metrics\": {";

  first=1
  for f in "$OUT_DIR"/*.time; do
    name=$(basename "$f" .time)
    metrics=$(parse_time_file "$f")
    if [ $first -eq 0 ]; then
      echo ","
    fi
    first=0
    echo -n "    \"$name\": $metrics"
  done

  echo "";
  echo "  }";
  echo "}";
} > "$SUMMARY_JSON"

echo "Report dir: $OUT_DIR"
echo "Commands log: $CMD_LOG"
echo "Summary JSON: $SUMMARY_JSON"
