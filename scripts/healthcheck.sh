#!/usr/bin/env bash
set -euo pipefail

echo "=== GitLab CI Multi-Stage Cloud Pipeline Healthcheck ==="
python3 scripts/lint_gitlab_ci.py
echo "[OK] Healthcheck passed."
exit 0
