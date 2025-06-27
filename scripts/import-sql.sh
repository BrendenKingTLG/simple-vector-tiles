#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# Export default PG connection variables
export PGHOST="${POSTGRES_HOST:-${PGHOST:-postgres}}"
export PGDATABASE="${POSTGRES_DB:-${PGDATABASE:-openmaptiles}}"
export PGUSER="${POSTGRES_USER:-${PGUSER:-openmaptiles}}"
export PGPASSWORD="${POSTGRES_PASSWORD:-${PGPASSWORD:-openmaptiles}}"
export PGPORT="${POSTGRES_PORT:-${PGPORT:-5432}}"

# Handle single file execution mode (used in xargs)
if [[ $# -eq 1 && -f "$1" ]]; then
  echo ">> Importing $1 ($(wc -l < "$1") lines)"
  psql -v ON_ERROR_STOP=1 -c '\timing on' -f "$1"
  exit 0
fi

# Normal multi-directory mode
if [[ -z "${SQL_TOOLS_DIR:-}" || -z "${SQL_DIR:-}" ]]; then
  echo "ERROR: Missing SQL_TOOLS_DIR or SQL_DIR environment variable"
  exit 1
fi

echo ">> Importing postgis-vt-util files from $SQL_TOOLS_DIR"
for f in "$SQL_TOOLS_DIR"/*.sql; do
  echo ">> Importing $f ($(wc -l < "$f") lines)"
  psql -v ON_ERROR_STOP=1 -c '\timing on' -f "$f"
done

echo ">> Importing run_first.sql (if exists)"
[[ -f "$SQL_DIR/run_first.sql" ]] && psql -v ON_ERROR_STOP=1 -c '\timing on' -f "$SQL_DIR/run_first.sql"

if [[ -d "$SQL_DIR/parallel" ]]; then
  echo ">> Importing SQL in parallel from $SQL_DIR/parallel"
  find "$SQL_DIR/parallel" -name '*.sql' -print0 | xargs -0 -P 4 -n 1 "$0"
fi

echo ">> Importing run_last.sql (if exists)"
[[ -f "$SQL_DIR/run_last.sql" ]] && psql -v ON_ERROR_STOP=1 -c '\timing on' -f "$SQL_DIR/run_last.sql"
