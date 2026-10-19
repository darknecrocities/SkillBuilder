#!/usr/bin/env bash
# ==============================================================================
# Script: sync_to_global.sh
# Purpose: Synchronize SkillBuilder repository to global Antigravity plugins directory.
# Author: Arron Kian Parejas (@darknecrocities)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GLOBAL_PLUGIN_DIR="${HOME}/.gemini/config/plugins/skill-builder"

echo "=== SkillBuilder Global Synchronization ==="
echo "Source: ${REPO_DIR}"
echo "Target: ${GLOBAL_PLUGIN_DIR}"

mkdir -p "$(dirname "${GLOBAL_PLUGIN_DIR}")"

# Backup existing global plugin directory if it's a real directory and not a symlink
if [ -d "${GLOBAL_PLUGIN_DIR}" ] && [ ! -L "${GLOBAL_PLUGIN_DIR}" ]; then
  BACKUP_DIR="${GLOBAL_PLUGIN_DIR}.backup.$(date +%s)"
  echo "Backing up existing directory to ${BACKUP_DIR}..."
  mv "${GLOBAL_PLUGIN_DIR}" "${BACKUP_DIR}"
elif [ -L "${GLOBAL_PLUGIN_DIR}" ]; then
  echo "Removing existing symlink..."
  rm -f "${GLOBAL_PLUGIN_DIR}"
fi

# Create atomic symlink
ln -s "${REPO_DIR}" "${GLOBAL_PLUGIN_DIR}"

echo "[SUCCESS] SkillBuilder symlinked to ${GLOBAL_PLUGIN_DIR}"
echo "Antigravity will now load the live repository changes globally!"
