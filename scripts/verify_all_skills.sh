#!/usr/bin/env bash
# ==============================================================================
# Script: verify_all_skills.sh
# Purpose: Master test runner for all SkillBuilder verification suites & guardrails.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Running SkillBuilder Master Verification Suite ==="
echo "Repository: ${REPO_DIR}"
echo ""

# 1. 500-Line Source File Limit Policy
echo "[1/11] Checking 500-Line Source File Policy..."
python3 "${REPO_DIR}/skills/world-class-engineering/scripts/check_source_line_limits.py" --path "${REPO_DIR}"
echo "[PASS] Line limits verified."
echo ""

# 2. World-Class Engineering Tests
echo "[2/11] Running world-class-engineering unit tests..."
python3 "${REPO_DIR}/skills/world-class-engineering/tests/test_check_source_line_limits.py"
echo ""

# 3. Production Etiquette Hygiene Tests
echo "[3/11] Running production-etiquette project hygiene tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_scaffold_project_hygiene.py"
echo ""

# 4. Production Etiquette Git Commit Chunking Tests
echo "[4/11] Running production-etiquette git commit chunking tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_analyze_git_commit_chunks.py"
echo ""

# 5. Prompt Refinement & Metacognition Tests
echo "[5/11] Running prompt-refinement-and-metacognition tests..."
python3 "${REPO_DIR}/skills/prompt-refinement-and-metacognition/tests/test_polish_prompt.py"
echo ""

# 6. QA Testing & Error Resolution Tests
echo "[6/11] Running qa-testing-and-error-resolution tests..."
python3 "${REPO_DIR}/skills/qa-testing-and-error-resolution/tests/test_lookup_error.py"
echo ""

# 7. UI & Frontend Quality Tests
echo "[7/11] Running ui-frontend-engineering tests..."
python3 "${REPO_DIR}/skills/ui-frontend-engineering/tests/test_verify_frontend_quality.py"
echo ""

# 8. Backend Systems Contract Tests
echo "[8/11] Running backend-systems-engineering tests..."
python3 "${REPO_DIR}/skills/backend-systems-engineering/tests/test_verify_api_contracts.py"
echo ""

# 9. Database Hygiene Tests
echo "[9/11] Running database-and-datastore-engineering tests..."
python3 "${REPO_DIR}/skills/database-and-datastore-engineering/tests/test_verify_database_hygiene.py"
echo ""

# 10. Container Security Tests
echo "[10/11] Running cloud-devops-infrastructure tests..."
python3 "${REPO_DIR}/skills/cloud-devops-infrastructure/tests/test_verify_container_security.py"
echo ""

# 11. AI Token Budget Tests
echo "[11/11] Running ai-and-llm-engineering tests..."
python3 "${REPO_DIR}/skills/ai-and-llm-engineering/tests/test_calculate_token_budget.py"
echo ""

echo "========================================================"
echo "[SUCCESS] ALL 11 SKILLBUILDER VERIFICATION SUITES PASSED!"
echo "========================================================"
