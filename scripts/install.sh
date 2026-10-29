#!/usr/bin/env bash
# ==============================================================================
# Script: install.sh
# Purpose: Universal installer for SkillBuilder across Antigravity, Cursor, Claude, Codex, Windsurf & Cline.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GLOBAL_PLUGIN_DIR="${HOME}/.gemini/config/plugins/skill-builder"

show_help() {
  cat << EOF
SkillBuilder Multi-Platform Installer

Usage:
  ./install.sh [OPTIONS]

Antigravity Options:
  --global, -g         Install globally for all Antigravity projects (via symlink)
  --project, -p <DIR>  Install into a specific project directory (.agents/ + AGENTS.md)

Multi-Platform Export Options:
  --cursor <DIR>       Export Cursor rules (.cursor/rules/*.mdc + .cursorrules)
  --claude <DIR>       Export Anthropic Claude Code rules (CLAUDE.md)
  --codex <DIR>        Export OpenAI Codex / ChatGPT instructions (CODEX.md)
  --windsurf <DIR>     Export Windsurf Cascade rules (.windsurfrules)
  --cline <DIR>        Export Cline / Roo-Code rules (.clinerules)
  --all <DIR>          Export all platform configurations simultaneously

General:
  --help, -h           Show this help message

Examples:
  ./install.sh --global
  ./install.sh --project /path/to/my-project
  ./install.sh --cursor /path/to/cursor-repo
  ./install.sh --all /path/to/my-repo
EOF
}

install_global() {
  echo "=== Installing SkillBuilder Globally for Antigravity ==="
  echo "Source: ${REPO_DIR}"
  echo "Target: ${GLOBAL_PLUGIN_DIR}"

  mkdir -p "$(dirname "${GLOBAL_PLUGIN_DIR}")"

  if [ -d "${GLOBAL_PLUGIN_DIR}" ] && [ ! -L "${GLOBAL_PLUGIN_DIR}" ]; then
    BACKUP_DIR="${GLOBAL_PLUGIN_DIR}.bak"
    echo "[SAFEGUARD] Existing directory detected at ${GLOBAL_PLUGIN_DIR}."
    echo "Maintaining single canonical backup slot (zero duplicate backup spam): ${BACKUP_DIR}"
    rm -rf "${BACKUP_DIR}"
    mv "${GLOBAL_PLUGIN_DIR}" "${BACKUP_DIR}"
  elif [ -L "${GLOBAL_PLUGIN_DIR}" ]; then
    echo "Removing existing symlink..."
    rm -f "${GLOBAL_PLUGIN_DIR}"
  fi

  ln -s "${REPO_DIR}" "${GLOBAL_PLUGIN_DIR}"
  echo "[SUCCESS] SkillBuilder installed globally at: ${GLOBAL_PLUGIN_DIR}"
  echo "All Antigravity sessions on this workstation will now load these skills."
}

install_project() {
  TARGET_DIR="$1"
  if [ ! -d "${TARGET_DIR}" ]; then
    echo "Error: Target directory '${TARGET_DIR}' does not exist." >&2
    exit 1
  fi
  TARGET_PATH="$(cd "${TARGET_DIR}" && pwd)"

  echo "=== Installing SkillBuilder into Project: ${TARGET_PATH} ==="
  mkdir -p "${TARGET_PATH}/.agents/skills"

  # Copy skills
  cp -r "${REPO_DIR}/skills/"* "${TARGET_PATH}/.agents/skills/"

  # Copy skills.json
  mkdir -p "${TARGET_PATH}/.agents"
  cat << 'EOF' > "${TARGET_PATH}/.agents/skills.json"
{
  "entries": [
    {
      "path": "skills"
    }
  ]
}
EOF

  # Copy AGENTS.md
  cp "${REPO_DIR}/AGENTS.md" "${TARGET_PATH}/AGENTS.md"

  echo "[SUCCESS] SkillBuilder installed into project: ${TARGET_PATH}"
  echo "Remember to commit .agents/ and AGENTS.md to your Git repository."
}

export_platform() {
  PLATFORM="$1"
  TARGET_DIR="$2"
  if [ ! -d "${TARGET_DIR}" ]; then
    echo "Creating target directory: ${TARGET_DIR}"
    mkdir -p "${TARGET_DIR}"
  fi
  python3 "${REPO_DIR}/scripts/export_multiplatform.py" --repo "${REPO_DIR}" --target "${TARGET_DIR}" --platform "${PLATFORM}"
}

# Parse flags
if [ $# -eq 0 ]; then
  install_global
  exit 0
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --global|-g)
      install_global
      shift
      ;;
    --project|-p)
      if [ -z "${2:-}" ]; then
        echo "Error: --project requires a directory path argument." >&2
        exit 1
      fi
      install_project "$2"
      shift 2
      ;;
    --cursor)
      if [ -z "${2:-}" ]; then
        echo "Error: --cursor requires a directory path argument." >&2
        exit 1
      fi
      export_platform "cursor" "$2"
      shift 2
      ;;
    --claude)
      if [ -z "${2:-}" ]; then
        echo "Error: --claude requires a directory path argument." >&2
        exit 1
      fi
      export_platform "claude" "$2"
      shift 2
      ;;
    --codex)
      if [ -z "${2:-}" ]; then
        echo "Error: --codex requires a directory path argument." >&2
        exit 1
      fi
      export_platform "codex" "$2"
      shift 2
      ;;
    --windsurf)
      if [ -z "${2:-}" ]; then
        echo "Error: --windsurf requires a directory path argument." >&2
        exit 1
      fi
      export_platform "windsurf" "$2"
      shift 2
      ;;
    --cline)
      if [ -z "${2:-}" ]; then
        echo "Error: --cline requires a directory path argument." >&2
        exit 1
      fi
      export_platform "cline" "$2"
      shift 2
      ;;
    --all)
      if [ -z "${2:-}" ]; then
        echo "Error: --all requires a directory path argument." >&2
        exit 1
      fi
      export_platform "all" "$2"
      shift 2
      ;;
    --help|-h)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      show_help
      exit 1
      ;;
  esac
done
