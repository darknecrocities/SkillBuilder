#!/usr/bin/env bash
# ==============================================================================
# Script: verify_all_skills.sh
# Purpose: Master test runner for all 36 SkillBuilder verification suites & guardrails.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Running SkillBuilder Master 48-Suite Verification Runner ==="
echo "Repository: ${REPO_DIR}"
echo ""

# 1. 500-Line Source File Limit Policy
echo "[1/48] Checking 500-Line Source File Policy..."
python3 "${REPO_DIR}/skills/world-class-engineering/scripts/check_source_line_limits.py" --path "${REPO_DIR}"
echo "[PASS] Line limits verified across all source files."
echo ""

# 2. World-Class Engineering Tests
echo "[2/48] Running world-class-engineering tests..."
python3 "${REPO_DIR}/skills/world-class-engineering/tests/test_check_source_line_limits.py"
echo ""

# 3. Anti-AI-Slop Tests
echo "[3/48] Running anti-slop sanitizer tests..."
python3 "${REPO_DIR}/skills/anti-slop/tests/test_sanitize_ai_slop.py"
echo ""

# 4. Autonomous Research Tests
echo "[4/48] Running autonomous research & fallback tests..."
python3 "${REPO_DIR}/skills/research/tests/test_research_alternatives.py"
echo ""

# 5. Responsiveness QA Tests (UI Tier)
echo "[5/48] Running responsiveness & viewport UI QA tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_verify_responsiveness_and_qa.py"
echo ""

# 6. List-an-Error QA Tests
echo "[6/48] Running QA error catalog lookup tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_lookup_error.py"
echo ""

# 7. App Functionality QA Tests (App Tier)
echo "[7/48] Running app functionality & resilience QA tests..."
python3 "${REPO_DIR}/skills/qa/tests/test_verify_app_functionality.py"
echo ""

# 8. UI Design Tokens Tests
echo "[8/48] Running UI tokens & vector icon tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_ui_tokens.py"
echo ""

# 9. UI Frontend Quality Tests
echo "[9/48] Running UI frontend quality & anti-vibe tests..."
python3 "${REPO_DIR}/skills/ui/tests/test_verify_frontend_quality.py"
echo ""

# 10. Frontend Architecture Tests
echo "[10/48] Running frontend architecture tests..."
python3 "${REPO_DIR}/skills/frontend/tests/test_verify_frontend_architecture.py"
echo ""

# 11. Security Defense Tests
echo "[11/48] Running security hygiene & defense tests..."
python3 "${REPO_DIR}/skills/security/tests/test_audit_security_hygiene.py"
echo ""

# 12. Fullstack Anti-Mock Tests
echo "[12/48] Running fullstack anti-mock integration tests..."
python3 "${REPO_DIR}/skills/fullstack/tests/test_verify_end_to_end_integration.py"
echo ""

# 13. Performance & Web Vitals Tests
echo "[13/48] Running performance & Web Vitals budget tests..."
python3 "${REPO_DIR}/skills/performance/tests/test_audit_performance_budgets.py"
echo ""

# 14. API Design OpenAPI Tests
echo "[14/48] Running API design OpenAPI contract tests..."
python3 "${REPO_DIR}/skills/api-design/tests/test_validate_openapi_spec.py"
echo ""

# 15. Observability Telemetry Tests
echo "[15/48] Running observability telemetry tests..."
python3 "${REPO_DIR}/skills/observability/tests/test_verify_telemetry_standards.py"
echo ""

# 16. Safe Refactoring Tests
echo "[16/48] Running safe refactoring opportunity tests..."
python3 "${REPO_DIR}/skills/refactor/tests/test_detect_refactor_opportunities.py"
echo ""

# 17. Git Workflow Commit Chunking Tests
echo "[17/48] Running git workflow commit chunking tests..."
python3 "${REPO_DIR}/skills/git-workflow/tests/test_analyze_git_commit_chunks.py"
echo ""

# 18. Git Delivery Etiquette Tests
echo "[18/48] Running git delivery etiquette & PR verification tests..."
python3 "${REPO_DIR}/skills/git-workflow/tests/test_verify_git_delivery_etiquette.py"
echo ""

# 19. Continuous Learning Tests
echo "[19/48] Running continuous learning protocol tests..."
python3 "${REPO_DIR}/skills/continuous-learning/tests/test_record_learning.py"
echo ""

# 20. Backend Contracts Tests
echo "[20/48] Running backend systems API contract tests..."
python3 "${REPO_DIR}/skills/backend/tests/test_verify_api_contracts.py"
echo ""

# 21. Database Hygiene Tests
echo "[21/48] Running database hygiene & migration tests..."
python3 "${REPO_DIR}/skills/database/tests/test_verify_database_hygiene.py"
echo ""

# 22. Container DevOps Security Tests
echo "[22/48] Running container DevOps security tests..."
python3 "${REPO_DIR}/skills/devops/tests/test_verify_container_security.py"
echo ""

# 23. AI Token Budget Tests
echo "[23/48] Running AI & LLM token budget tests..."
python3 "${REPO_DIR}/skills/ai/tests/test_calculate_token_budget.py"
echo ""

# 24. Prompt Polish Tests
echo "[24/48] Running prompt refinement tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_polish_prompt.py"
echo ""

# 25. Prompt Polish Learning Tests
echo "[25/48] Running prompt polish convention tests..."
python3 "${REPO_DIR}/skills/prompt-polish/tests/test_record_learning.py"
echo ""

# 26. Production Etiquette Project Hygiene Tests
echo "[26/48] Running production etiquette hygiene tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_scaffold_project_hygiene.py"
echo ""

# 27. Production Etiquette Commit Chunk Tests
echo "[27/48] Running production etiquette git chunk tests..."
python3 "${REPO_DIR}/skills/production-etiquette/tests/test_analyze_git_commit_chunks.py"
echo ""

# 28. Multi-Platform Exporter Tests
echo "[28/48] Running multi-platform exporter tests (Cursor, Claude, Codex)..."
python3 "${REPO_DIR}/scripts/tests/test_export_multiplatform.py"
echo ""

# 29. 3D WebGL / Three.js Performance Tests
echo "[29/48] Running 3D WebGL / Three.js showcase performance tests..."
python3 "${REPO_DIR}/skills/3d/tests/test_verify_3d_performance.py"
echo ""

# 30. Full-Scale Mode Orchestration Tests
echo "[30/48] Running Full-Scale Mode orchestration & token budget tests..."
python3 "${REPO_DIR}/skills/full-scale-mode/tests/test_verify_full_scale_orchestration.py"
echo ""

# 31. GCP Cloud Architecture Hygiene Tests
echo "[31/48] Running GCP Cloud Run & infrastructure hygiene tests..."
python3 "${REPO_DIR}/skills/gcp/tests/test_verify_gcp_hygiene.py"
echo ""

# 32. AWS Resilient Architecture Hygiene Tests
echo "[32/48] Running AWS resilience & S3 bucket security tests..."
python3 "${REPO_DIR}/skills/aws/tests/test_verify_aws_hygiene.py"
echo ""

# 33. Firebase Security Rules Tests
echo "[33/48] Running Firebase Firestore rules & security tests..."
python3 "${REPO_DIR}/skills/firebase/tests/test_verify_firebase_rules.py"
echo ""

# 34. Supabase RLS & Architecture Tests
echo "[34/48] Running Supabase PostgreSQL RLS & architecture tests..."
python3 "${REPO_DIR}/skills/supabase/tests/test_verify_supabase_rls.py"
echo ""

# 35. File-Based Routing Architecture Tests
echo "[35/48] Running file-based routing architecture tests..."
python3 "${REPO_DIR}/skills/routing/tests/test_verify_routing_architecture.py"
echo ""

# 36. State Management Hygiene Tests
echo "[36/48] Running state management & selector memoization tests..."
python3 "${REPO_DIR}/skills/state-management/tests/test_verify_state_hygiene.py"
echo ""

# 37. Project Skill Synthesis & Minting Tests
echo "[37/48] Running Project Skill Minting & SSP tests..."
python3 "${REPO_DIR}/skills/project-skills/tests/test_synthesize_project_skill.py"
echo ""

# 38. Testing Discipline & Playwright Hygiene Tests
echo "[38/48] Running testing discipline & E2E locator hygiene tests..."
python3 "${REPO_DIR}/skills/testing/tests/test_verify_testing_hygiene.py"
echo ""

# 39. Internationalization & RTL Hygiene Tests
echo "[39/48] Running internationalization & RTL mirroring tests..."
python3 "${REPO_DIR}/skills/i18n/tests/test_verify_i18n_hygiene.py"
echo ""

# 40. Data Pipeline Integrity Tests
echo "[40/48] Running data pipeline streaming & DLQ integrity tests..."
python3 "${REPO_DIR}/skills/data-pipelines/tests/test_verify_pipeline_integrity.py"
echo ""

# 41. Mobile UI Native Craftsmanship Tests
echo "[41/48] Running mobile-ui native craftsmanship & safe area tests..."
python3 "${REPO_DIR}/skills/mobile-ui/tests/test_verify_mobile_ui_hygiene.py"
echo ""

# 42. Web UI Container Queries & Modern Styling Tests
echo "[42/48] Running web-ui container queries & fluid typography tests..."
python3 "${REPO_DIR}/skills/web-ui/tests/test_verify_web_ui_hygiene.py"
echo ""

# 43. Local LLM Quantized Inference & Routing Tests
echo "[43/48] Running local-llm quantized inference & hybrid routing tests..."
python3 "${REPO_DIR}/skills/local-llm/tests/test_verify_local_llm_hygiene.py"
echo ""

# 44. Deduplicated Single-Slot Backup & Sensitive Deletion Gate Tests
echo "[44/48] Running deduplicated backup & sensitive deletion guardrail tests..."
python3 "${REPO_DIR}/skills/database/tests/test_manage_deduplicated_backup.py"
echo ""

# 45. Antigravity Automation & Scheduled Execution Tests
echo "[45/48] Running Antigravity Automation & sidecar tests..."
python3 "${REPO_DIR}/skills/antigravity-automation/tests/test_antigravity_automation.py"
echo ""

# 46. SkillBuilder Quality & Token Efficiency Linter Tests
echo "[46/48] Running SkillBuilder quality & token efficiency linter tests..."
python3 "${REPO_DIR}/scripts/tests/test_skill_linter.py"
echo ""

# 47. Orchestration Memory Subsystem Tests
echo "[47/48] Running Orchestration Memory Subsystem tests..."
python3 "${REPO_DIR}/skills/full-scale-mode/tests/test_manage_orchestration_memory.py"
echo ""

# 48. Orchestration Multi-Tier Evaluation Harness Tests
echo "[48/48] Running Orchestration Evaluation Harness & Self-Healing Loop tests..."
python3 "${REPO_DIR}/skills/full-scale-mode/tests/test_orchestration_harness.py"
echo ""

echo "=========================================================="
echo "[SUCCESS] ALL 48 SKILLBUILDER VERIFICATION SUITES PASSED!"
echo "=========================================================="
