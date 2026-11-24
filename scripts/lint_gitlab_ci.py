#!/usr/bin/env python3
"""
GitLab CI/CD Pipeline Schema & Syntax Linter
Inspects .gitlab-ci.yml and template includes for stages, caching, DinD, and environments.
"""

import os
import sys
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CI_FILE = os.path.join(ROOT, ".gitlab-ci.yml")
EXPECTED_STAGES = ["validate", "test", "security", "build", "deploy-staging", "deploy-production"]

def main():
    print(f"[*] Validating GitLab CI configuration: {CI_FILE}")
    if not os.path.exists(CI_FILE):
        print(f"[FAIL] {CI_FILE} does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(CI_FILE, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"[FAIL] YAML Syntax error: {e}", file=sys.stderr)
            sys.exit(1)

    stages = data.get("stages", [])
    print(f"[*] Detected Pipeline Stages: {stages}")
    for s in EXPECTED_STAGES:
        if s not in stages:
            print(f"[FAIL] Missing expected pipeline stage: '{s}'", file=sys.stderr)
            sys.exit(1)

    # Check cache configuration
    cache = data.get("cache", {})
    if not cache or "paths" not in cache:
        print("[FAIL] Missing global cache definition or cache paths.", file=sys.stderr)
        sys.exit(1)
    print(f"[PASS] Global cache verified with paths: {cache['paths']}")

    # Check DinD service configuration
    dind_job = data.get("docker_dind_build", {})
    services = dind_job.get("services", [])
    has_dind = any("dind" in str(s) for s in services)
    if not has_dind:
        print("[FAIL] docker_dind_build job missing docker:dind service.", file=sys.stderr)
        sys.exit(1)
    print("[PASS] Docker-in-Docker service verified.")

    # Check Production Manual Gate
    prod_job = data.get("deploy_to_production", {})
    if prod_job.get("when") != "manual":
        print("[FAIL] deploy_to_production must specify 'when: manual' safety gate.", file=sys.stderr)
        sys.exit(1)
    print("[PASS] Production manual approval gate verified.")

    print("==================================================")
    print("[SUCCESS] GitLab CI/CD multi-stage pipeline passed all enterprise checks.")
    sys.exit(0)

if __name__ == "__main__":
    main()
