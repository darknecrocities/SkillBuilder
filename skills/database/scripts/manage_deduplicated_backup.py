#!/usr/bin/env python3
"""
manage_deduplicated_backup.py - Content-addressable, single-slot deduplicated backup
and sensitive deletion gate for multi-agent database and cloud storage operations.

Eliminates spammy backup duplication (*.bak.1, *.bak.2) across concurrent agents by
tracking SHA-256 state digests in a shared .backups/backup_manifest.json registry.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Database & Storage Engineering
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

MANIFEST_FILENAME = "backup_manifest.json"

SENSITIVE_KEYWORDS = (
    "user", "auth", "account", "credential", "secret", "token", "payment",
    "invoice", "wallet", "tenant", "customer", "order", "bucket", "storage",
    "firestore", "supabase", "prod", ".env", "key"
)


def compute_target_sha256(target_path: Path) -> str:
    """Computes a deterministic SHA-256 digest for a file or directory."""
    hasher = hashlib.sha256()
    if target_path.is_file():
        with open(target_path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    for root, dirs, files in os.walk(target_path):
        dirs[:] = sorted(d for d in dirs if d not in {".git", ".backups", "node_modules", "__pycache__"})
        for fname in sorted(files):
            fpath = Path(root) / fname
            rel = str(fpath.relative_to(target_path)).encode("utf-8")
            hasher.update(rel)
            if fpath.is_file():
                with open(fpath, "rb") as fh:
                    for chunk in iter(lambda: fh.read(65536), b""):
                        hasher.update(chunk)
    return hasher.hexdigest()


def load_manifest(backup_dir: Path) -> Dict[str, Any]:
    """Loads the shared multi-agent backup manifest or initializes a clean structure."""
    manifest_path = backup_dir / MANIFEST_FILENAME
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": "1.0", "resources": {}}


def save_manifest(backup_dir: Path, manifest: Dict[str, Any]) -> None:
    """Atomically writes the shared backup manifest via a temporary file rename."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = backup_dir / MANIFEST_FILENAME
    tmp_path = backup_dir / f"{MANIFEST_FILENAME}.tmp.{os.getpid()}"
    tmp_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp_path, manifest_path)


def copy_to_canonical_slot(source: Path, dest_slot: Path) -> None:
    """Writes the resource into a single canonical backup slot without duplicate numbering."""
    if dest_slot.exists():
        if dest_slot.is_dir():
            shutil.rmtree(dest_slot)
        else:
            dest_slot.unlink()
    if source.is_dir():
        shutil.copytree(source, dest_slot)
    else:
        shutil.copy2(source, dest_slot)


def ensure_deduplicated_backup(
    target_path: str,
    backup_dir: str = ".backups",
    agent_id: str = "primary-agent",
    resource_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Creates or reuses a single canonical backup keyed by SHA-256 content hash."""
    src = Path(target_path).resolve()
    if not src.exists():
        raise FileNotFoundError(f"Target resource not found: {src}")

    bdir = Path(backup_dir).resolve()
    bdir.mkdir(parents=True, exist_ok=True)

    key = resource_key or src.name
    current_hash = compute_target_sha256(src)
    manifest = load_manifest(bdir)
    existing = manifest.get("resources", {}).get(key)
    slot_path = bdir / f"{key}.canonical.bak"

    if existing and existing.get("state_sha256") == current_hash and slot_path.exists():
        return {
            "status": "SKIPPED_DUPLICATE_HASH",
            "resource_key": key,
            "state_sha256": current_hash,
            "canonical_slot": str(slot_path),
            "last_agent_id": existing.get("agent_id", agent_id),
            "deduplicated": True,
            "message": "State SHA-256 unchanged; reused existing canonical backup without duplication."
        }

    copy_to_canonical_slot(src, slot_path)
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "resource_key": key,
        "source_path": str(src),
        "canonical_slot": str(slot_path),
        "state_sha256": current_hash,
        "agent_id": agent_id,
        "updated_at": timestamp,
    }
    manifest.setdefault("resources", {})[key] = record
    save_manifest(bdir, manifest)

    return {
        "status": "CREATED_CANONICAL_BACKUP",
        "resource_key": key,
        "state_sha256": current_hash,
        "canonical_slot": str(slot_path),
        "last_agent_id": agent_id,
        "deduplicated": False,
        "message": "Updated single canonical backup slot with new state SHA-256."
    }


def classify_sensitivity(resource_name: str) -> str:
    """Classifies resource sensitivity tier for human-in-the-loop deletion warnings."""
    lower = resource_name.lower()
    if any(k in lower for k in (".env", "secret", "credential", "token", "key", "auth")):
        return "Tier 1 (Critical Security / Identity / Credentials)"
    if any(k in lower for k in SENSITIVE_KEYWORDS):
        return "Tier 2 (Sensitive Tenant / Financial / Persistent Storage)"
    return "Tier 3 (Stateful Schema / Application Resource)"


def evaluate_deletion_safety(
    target_path: str,
    backup_dir: str = ".backups",
    user_confirmed: bool = False,
) -> Dict[str, Any]:
    """Evaluates whether a resource can be safely deleted and builds user disclosure."""
    src = Path(target_path).resolve()
    bdir = Path(backup_dir).resolve()
    key = src.name
    sensitivity = classify_sensitivity(str(src))

    manifest = load_manifest(bdir)
    entry = manifest.get("resources", {}).get(key)
    current_hash = compute_target_sha256(src) if src.exists() else None
    slot_exists = bool(entry and Path(entry.get("canonical_slot", "")).exists())
    hash_verified = bool(entry and current_hash and entry.get("state_sha256") == current_hash and slot_exists)

    allowed = bool(hash_verified and user_confirmed)
    disclosure = (
        f"[SENSITIVE DELETION DISCLOSURE] Target '{key}' ({sensitivity}): "
        f"Backup verified={hash_verified} (SHA-256: {current_hash or 'N/A'}). "
        f"User confirmed={user_confirmed}. "
        "Agents MUST notify the user and obtain explicit confirmation before deleting."
    )
    return {
        "allowed": allowed,
        "resource_key": key,
        "sensitivity_tier": sensitivity,
        "backup_verified": hash_verified,
        "state_sha256": current_hash,
        "user_confirmed": user_confirmed,
        "disclosure": disclosure,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage single-slot deduplicated backups and deletion safety.")
    parser.add_argument("--target", "-t", required=True, help="Target file or directory path")
    parser.add_argument("--backup-dir", "-b", default=".backups", help="Directory storing canonical backups")
    parser.add_argument("--agent-id", default="primary-agent", help="Identifier of the active agent/subagent")
    parser.add_argument("--check-deletion", action="store_true", help="Evaluate pre-deletion safety gate")
    parser.add_argument("--user-confirmed", action="store_true", help="Flag indicating explicit user approval")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    if args.check_deletion:
        res = evaluate_deletion_safety(args.target, args.backup_dir, args.user_confirmed)
        print(json.dumps(res, indent=2) if args.json else res["disclosure"])
        return 0 if res["allowed"] else 1

    res = ensure_deduplicated_backup(args.target, args.backup_dir, args.agent_id)
    print(json.dumps(res, indent=2) if args.json else f"[{res['status']}] {res['message']} ({res['state_sha256'][:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
