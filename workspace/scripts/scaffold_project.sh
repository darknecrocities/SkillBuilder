#!/usr/bin/env bash
# ==============================================================================
# Script: scaffold_project.sh
# Purpose: Initialize a project with SkillBuilder standards & Antigravity skills.
# ==============================================================================

set -euo pipefail

TARGET_DIR="${1:-.}"
TARGET_PATH="$(cd "${TARGET_DIR}" && pwd)"

echo "=== Scaffolding SkillBuilder Engineering Standards into: ${TARGET_PATH} ==="

mkdir -p "${TARGET_PATH}/.agents"
mkdir -p "${TARGET_PATH}/.github/workflows"

# 1. Project-level .agents/skills.json
cat << 'EOF' > "${TARGET_PATH}/.agents/skills.json"
{
  "entries": [
    {
      "path": "skills"
    }
  ]
}
EOF

# 2. Project AGENTS.md rulebook
cat << 'EOF' > "${TARGET_PATH}/AGENTS.md"
# Mandatory Engineering Discipline & Production Etiquette

All work in this repository must strictly adhere to SkillBuilder engineering standards:

1. **Prompt Polishing**: Clarify requirements, constraints, and test criteria before writing code.
2. **Anti-Mock Mandate**: Use real schemas and real persistence. Never mock data with static arrays.
3. **Secret Hygiene**: Maintain .env.example, never commit raw credentials.
4. **Resilience**: Enforce explicit connection/read timeouts, caching with invalidation, and retry with jitter.
5. **Quality Verification**: Execute automated unit/integration tests before declaring tasks complete.
6. **500-Line Rule**: Maintain a 500-line physical limit on all source files.
EOF

# 3. .gitignore additions
if [ ! -f "${TARGET_PATH}/.gitignore" ]; then
  cat << 'EOF' > "${TARGET_PATH}/.gitignore"
# Environment & Secrets
.env
.env.local
*.key
*.pem

# Dependencies
node_modules/
venv/
.venv/
__pycache__/

# OS & Build Artifacts
.DS_Store
dist/
build/
coverage/
EOF
else
  grep -qxF ".env" "${TARGET_PATH}/.gitignore" || echo ".env" >> "${TARGET_PATH}/.gitignore"
  grep -qxF ".env.local" "${TARGET_PATH}/.gitignore" || echo ".env.local" >> "${TARGET_PATH}/.gitignore"
fi

# 4. .env.example
if [ ! -f "${TARGET_PATH}/.env.example" ]; then
  cat << 'EOF' > "${TARGET_PATH}/.env.example"
# Application Configuration
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/appdb
LOG_LEVEL=info
EOF
fi

echo "[SUCCESS] Project scaffolded with SkillBuilder standards at: ${TARGET_PATH}"
