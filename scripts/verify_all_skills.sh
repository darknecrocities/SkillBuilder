#!/usr/bin/env bash
# ==============================================================================
# Script: verify_all_skills.sh
# Purpose: Master test runner for all 22 SkillBuilder verification suites & guardrails.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Running SkillBuilder Master 29-Suite Verification Runner ==="
echo "Repository: ${REPO_DIR}"
echo ""

# 1. 500-Line Source File Limit Policy
echo "[1/29] Checking 500-Line Source File Policy..."
python3 "${REPO_DIR}/skills/world-class-engineering/scripts/check_source_line_limits.py" --path "${REPO_DIR}"
echo "[PASS] Line limits verified across all source files."
echo ""

# 2. World-Class Engineering Tests
echo "[2/29] Running world-class-engineering tests..."
python3 "${REPO_DIR}/skills/world-class-engineering/tests/test_check_source_line_limits.py"
echo ""

# 3. Anti-AI-Slop Tests
echo "[3/29] Running anti-slop sanitizer tests..."
python3 "${REPO_DIR}/skills/anti-slop/tests/test_sanitize_ai_slop.py"
echo ""

# 4. Autonomous Research Tests
echo "[4/29] Running autonomous research & fallback tests..."
python3 "${REPO_DIR}/skills/research/tests/test_research_alternatives.py"
echo ""

# 5. Responsiveness QA Tests (UI Tier)
echo "[5/29] Running responsiveness & viewport UI QA tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_verify_responsiveness_and_qa.py"
echo ""

# 6. List-an-Error QA Tests
echo "[6/29] Running QA error catalog lookup tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_lookup_error.py"
echo ""

# 7. App Functionality QA Tests (App Tier)
echo "[7/29] Running app functionality & resilience QA tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_verify_app_functionality.py"
echo ""

# 8. UI Design Tokens Tests
echo "[8/29] Running UI tokens & vector icon tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_ui_tokens.py"
echo ""

# 9. UI Frontend Quality Tests
echo "[9/29] Running UI frontend quality & anti-vibe tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_frontend_quality.py"
echo ""

# 10. Frontend Architecture Tests
echo "[10/29] Running frontend architecture tests..."
python3 "${REPO_DIR}/skills/frontend/tests/test_verify_frontend_architecture.py"
echo ""

# 11. Security Defense Tests
echo "[11/29] Running security hygiene & defense tests..."
python3 "${REPO_DIR}/skills/security/tests/test_audit_security_hygiene.py"
echo ""

# 12. Fullstack Anti-Mock Tests
echo "[12/29] Running fullstack anti-mock integration tests..."
python3 "${REPO_DIR}/skills/fullstack/tests/test_verify_end_to_end_integration.py"
echo ""

# 13. Performance & Web Vitals Tests
echo "[13/29] Running performance & Web Vitals budget tests..."
python3 "${REPO_DIR}/skills/performance/tests/test_audit_performance_budgets.py"
echo ""

# 14. API Design OpenAPI Tests
echo "[14/29] Running API design OpenAPI contract tests..."
python3 "${REPO_DIR}/skills/api-design/tests/test_validate_openapi_spec.py"
echo ""

# 15. Observability Telemetry Tests
echo "[15/29] Running observability telemetry tests..."
python3 "${REPO_DIR}/skills/observability/tests/test_verify_telemetry_standards.py"
echo ""

# 16. Safe Refactoring Tests
echo "[16/29] Running safe refactoring opportunity tests..."
python3 "${REPO_DIR}/skills/refactor/tests/test_detect_refactor_opportunities.py"
echo ""

# 17. Git Workflow Commit Chunking Tests
echo "[17/29] Running git workflow commit chunking tests..."
python3 "${REPO_DIR}/skills/git-workflow/tests/test_analyze_git_commit_chunks.py"
echo ""

# 18. Continuous Learning Tests
echo "[18/29] Running continuous learning protocol tests..."
python3 "${REPO_DIR}/skills/continuous-learning/tests/test_record_learning.py"
echo ""

# 19. Backend Contracts Tests
echo "[19/29] Running backend systems API contract tests..."
python3 "${REPO_DIR}/skills/backend/tests/test_verify_api_contracts.py"
echo ""

# 20. Database Hygiene Tests
echo "[20/29] Running database hygiene & migration tests..."
python3 "${REPO_DIR}/skills/database/tests/test_verify_database_hygiene.py"
echo ""

# 21. Container DevOps Security Tests
echo "[21/29] Running container DevOps security tests..."
python3 "${REPO_DIR}/skills/devops/tests/test_verify_container_security.py"
echo ""

# 22. AI Token Budget Tests
echo "[22/29] Running AI & LLM token budget tests..."
python3 "${REPO_DIR}/skills/ai/tests/test_calculate_token_budget.py"
echo ""

# 23. Prompt Polish Tests
echo "[23/29] Running prompt refinement tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_polish_prompt.py"
echo ""

# 24. Prompt Polish Learning Tests
echo "[24/29] Running prompt polish convention tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_record_learning.py"
echo ""

# 25. Production Etiquette Project Hygiene Tests
echo "[25/29] Running production etiquette hygiene tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_scaffold_project_hygiene.py"
echo ""

# 26. Production Etiquette Commit Chunk Tests
echo "[26/29] Running production etiquette git chunk tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_analyze_git_commit_chunks.py"
echo ""

# 27. Multi-Platform Exporter Tests
echo "[27/29] Running multi-platform exporter tests (Cursor, Claude, Codex)..."
python3 "${REPO_DIR}/scripts/tests/test_export_multiplatform.py"
echo ""

# 28. 3D WebGL / Three.js Performance Tests
echo "[28/29] Running 3D WebGL / Three.js showcase performance tests..."
python3 "${REPO_DIR}/skills/3d/tests/test_verify_3d_performance.py"
echo ""

# 29. Full-Scale Mode Orchestration Tests
echo "[29/29] Running Full-Scale Mode orchestration & token budget tests..."
python3 "${REPO_DIR}/skills/full-scale-mode/tests/test_verify_full_scale_orchestration.py"
echo ""

echo "=========================================================="
echo "[SUCCESS] ALL 29 SKILLBUILDER VERIFICATION SUITES PASSED!"
echo "=========================================================="
