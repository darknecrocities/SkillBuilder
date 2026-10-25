#!/usr/bin/env bash
# ==============================================================================
# Script: verify_all_skills.sh
# Purpose: Master test runner for all 20 SkillBuilder verification suites & guardrails.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Running SkillBuilder Master 27-Suite Verification Runner ==="
echo "Repository: ${REPO_DIR}"
echo ""

# 1. 500-Line Source File Limit Policy
echo "[1/27] Checking 500-Line Source File Policy..."
python3 "${REPO_DIR}/skills/world-class-engineering/scripts/check_source_line_limits.py" --path "${REPO_DIR}"
echo "[PASS] Line limits verified across all source files."
echo ""

# 2. World-Class Engineering Tests
echo "[2/27] Running world-class-engineering tests..."
python3 "${REPO_DIR}/skills/world-class-engineering/tests/test_check_source_line_limits.py"
echo ""

# 3. Anti-AI-Slop Tests
echo "[3/27] Running anti-slop sanitizer tests..."
python3 "${REPO_DIR}/skills/anti-slop/tests/test_sanitize_ai_slop.py"
echo ""

# 4. Autonomous Research Tests
echo "[4/27] Running autonomous research & fallback tests..."
python3 "${REPO_DIR}/skills/research/tests/test_research_alternatives.py"
echo ""

# 5. Responsiveness QA Tests
echo "[5/27] Running responsiveness & viewport QA tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_verify_responsiveness_and_qa.py"
echo ""

# 6. List-an-Error QA Tests
echo "[6/27] Running QA error catalog lookup tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_lookup_error.py"
echo ""

# 7. UI Design Tokens Tests
echo "[7/27] Running UI tokens & vector icon tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_ui_tokens.py"
echo ""

# 8. UI Frontend Quality Tests
echo "[8/27] Running UI frontend quality & anti-vibe tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_frontend_quality.py"
echo ""

# 9. Frontend Architecture Tests
echo "[9/27] Running frontend architecture tests..."
python3 "${REPO_DIR}/skills/frontend/tests/test_verify_frontend_architecture.py"
echo ""

# 10. Security Defense Tests
echo "[10/27] Running security hygiene & defense tests..."
python3 "${REPO_DIR}/skills/security/tests/test_audit_security_hygiene.py"
echo ""

# 11. Fullstack Anti-Mock Tests
echo "[11/27] Running fullstack anti-mock integration tests..."
python3 "${REPO_DIR}/skills/fullstack/tests/test_verify_end_to_end_integration.py"
echo ""

# 12. Performance & Web Vitals Tests
echo "[12/27] Running performance & Web Vitals budget tests..."
python3 "${REPO_DIR}/skills/performance/tests/test_audit_performance_budgets.py"
echo ""

# 13. API Design OpenAPI Tests
echo "[13/27] Running API design OpenAPI contract tests..."
python3 "${REPO_DIR}/skills/api-design/tests/test_validate_openapi_spec.py"
echo ""

# 14. Observability Telemetry Tests
echo "[14/27] Running observability telemetry tests..."
python3 "${REPO_DIR}/skills/observability/tests/test_verify_telemetry_standards.py"
echo ""

# 15. Safe Refactoring Tests
echo "[15/27] Running safe refactoring opportunity tests..."
python3 "${REPO_DIR}/skills/refactor/tests/test_detect_refactor_opportunities.py"
echo ""

# 16. Git Workflow Commit Chunking Tests
echo "[16/27] Running git workflow commit chunking tests..."
python3 "${REPO_DIR}/skills/git-workflow/tests/test_analyze_git_commit_chunks.py"
echo ""

# 17. Continuous Learning Tests
echo "[17/27] Running continuous learning protocol tests..."
python3 "${REPO_DIR}/skills/continuous-learning/tests/test_record_learning.py"
echo ""

# 18. Backend Contracts Tests
echo "[18/27] Running backend systems API contract tests..."
python3 "${REPO_DIR}/skills/backend/tests/test_verify_api_contracts.py"
echo ""

# 19. Database Hygiene Tests
echo "[19/27] Running database hygiene & migration tests..."
python3 "${REPO_DIR}/skills/database/tests/test_verify_database_hygiene.py"
echo ""

# 20. Container DevOps Security Tests
echo "[20/27] Running container DevOps security tests..."
python3 "${REPO_DIR}/skills/devops/tests/test_verify_container_security.py"
echo ""

# 21. AI Token Budget Tests
echo "[21/27] Running AI & LLM token budget tests..."
python3 "${REPO_DIR}/skills/ai/tests/test_calculate_token_budget.py"
echo ""

# 22. Prompt Polish Tests
echo "[22/27] Running prompt refinement tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_polish_prompt.py"
echo ""

# 23. Prompt Polish Learning Tests
echo "[23/27] Running prompt polish convention tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_record_learning.py"
echo ""

# 24. Production Etiquette Project Hygiene Tests
echo "[24/27] Running production etiquette hygiene tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_scaffold_project_hygiene.py"
echo ""

# 25. Production Etiquette Commit Chunk Tests
echo "[25/27] Running production etiquette git chunk tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_analyze_git_commit_chunks.py"
echo ""

# 26. Multi-Platform Exporter Tests
echo "[26/27] Running multi-platform exporter tests (Cursor, Claude, Codex)..."
python3 "${REPO_DIR}/scripts/tests/test_export_multiplatform.py"
echo ""

# 27. 3D WebGL / Three.js Performance Tests
echo "[27/27] Running 3D WebGL / Three.js showcase performance tests..."
python3 "${REPO_DIR}/skills/3d/tests/test_verify_3d_performance.py"
echo ""

echo "=========================================================="
echo "[SUCCESS] ALL 27 SKILLBUILDER VERIFICATION SUITES PASSED!"
echo "=========================================================="
