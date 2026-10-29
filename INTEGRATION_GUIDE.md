# Universal Google Antigravity Integration Guide

This guide provides instructions for integrating **SkillBuilder** into **Google Antigravity** on any machine. It enables software teams and individual developers to equip their AI coding agents with production engineering discipline, token-saving mechanisms, prompt polishing workflows, full-stack architectures, and automated QA verification.

---

## 1. Integration Methods Overview

Antigravity discovers skills and plugins hierarchically. Choose the method that best matches your workflow:

| Method | Target Scope | Installation Path | Best For |
| :--- | :--- | :--- | :--- |
| **Method 1: Global Plugin** *(Recommended)* | Machine-wide (All Projects) | `~/.gemini/config/plugins/skill-builder/` | Solo developers and local machines wanting automatic standards across every repo. |
| **Method 2: Project-Level** | Single Repository | `<project-root>/.agents/` | Engineering teams sharing skills via version control (Git). |
| **Method 3: Turnkey Installer** | Automated Script | Run `scripts/install.sh` | Fast, one-command setup for macOS and Linux. |

---

## 2. Method 1: Global Plugin Setup (Recommended)

Installing SkillBuilder as a global plugin ensures that **any** Antigravity session on your workstation automatically inherits all 35 skills without requiring project-by-project setup.

### Step 1: Clone or Copy SkillBuilder
```bash
# Clone SkillBuilder to your preferred development directory
git clone https://github.com/darknecrocities/SkillBuilder.git ~/SkillBuilder
```

### Step 2: Symlink to Antigravity Global Plugins
```bash
# Ensure target plugin directory exists
mkdir -p ~/.gemini/config/plugins

# Create a live symbolic link
ln -s ~/SkillBuilder ~/.gemini/config/plugins/skill-builder
```

*(Note: If a directory already exists at `~/.gemini/config/plugins/skill-builder`, back it up first: `mv ~/.gemini/config/plugins/skill-builder ~/.gemini/config/plugins/skill-builder.bak`)*

### Step 3: Verify Plugin Discovery
In Antigravity CLI or chat:
```bash
agy plugin list
```
You should see:
```text
skill-builder [ENABLED] - Global engineering discipline enforcing world-class software engineering...
```

---

## 3. Method 2: Project-Level Setup (Team Git Sharing)

To enforce SkillBuilder across an engineering team working on a shared repository:

### Step 1: Initialize `.agents/` Directory
In your target repository root:
```bash
mkdir -p .agents/skills
```

### Step 2: Copy or Submodule SkillBuilder Skills
```bash
# Option A: Git Submodule
git submodule add https://github.com/darknecrocities/SkillBuilder.git .agents/plugins/skill-builder

# Option B: Direct Copy
cp -r ~/SkillBuilder/skills/* .agents/skills/
```

### Step 3: Configure `.agents/skills.json`
Create or update `.agents/skills.json` in your repository root:
```json
{
  "entries": [
    {
      "path": "skills"
    }
  ]
}
```

### Step 4: Add Team Rulebook (`AGENTS.md`)
Copy `AGENTS.md` to your repository root:
```bash
cp ~/SkillBuilder/AGENTS.md ./AGENTS.md
git add .agents/ AGENTS.md
git commit -m "chore: integrate SkillBuilder engineering standards"
```

---

## 4. Method 3: One-Command Turnkey Installer

SkillBuilder includes an automated setup script that configures your machine in seconds:

```bash
# Navigate to SkillBuilder directory
cd ~/SkillBuilder

# Install globally (Machine-wide)
bash scripts/install.sh --global

# Or install into a specific project repository
bash scripts/install.sh --project /path/to/my-project
```

---

## 5. How Antigravity Agents Use These Skills

Once installed, Antigravity leverages **Progressive Disclosure** to prevent context window bloat:

1. **Lightweight Skill Discovery**: Antigravity initially injects only the skill name and 1-line description into the agent's context.
2. **On-Demand Activation & Autonomous Skill Resonance (ASR)**: When you ask for frontend UI, backend APIs, database schemas, cloud deployments, or debugging, the agent automatically activates the relevant skill (e.g. `/web-ui`, `/mobile-ui`, `/backend`, `/database`, `/firebase`, `/supabase`, `/aws`, `/gcp`, `/full-scale-mode`).
3. **Prompt Polishing First**: The agent will parse, polish, and structure your raw prompt before modifying source code.
4. **Deduplicated Backups & Sensitive Deletion Disclosures**: Before migrating schemas or mutating cloud storage, the agent verifies a single SHA-256 content-hashed backup (`.backups/backup_manifest.json`) without creating duplicate backup spam, and always warns you first before deleting sensitive tables, buckets, or files.
5. **Mandatory Verification**: Before reporting completion, the agent will run tests, linters, and the 500-line source check.

---

## 6. Verification & Troubleshooting

### How to Confirm Skills are Active in Chat
Open any conversation in Antigravity and type:
> *"What skills do you have available for database, cloud storage, and full-scale orchestration?"*

The agent should confirm awareness of the **35 synchronized skills**, including:
- `/full-scale-mode` & `/world-class-engineering`
- `/prompt-polish` & `/anti-slop`
- `/ui`, `/web-ui`, `/mobile-ui`, `/3d`, `/frontend`, `/routing`, `/state-management`, `/i18n`
- `/backend`, `/fullstack`, `/api-design`, `/database`, `/firebase`, `/supabase`, `/aws`, `/gcp`, `/data-pipelines`, `/devops`
- `/security`, `/ai`, `/local-llm`, `/research`
- `/testing`, `/qa`, `/performance`, `/observability`, `/production-etiquette`, `/refactor`, `/git-workflow`, `/continuous-learning`, `/project-skills`

### Troubleshooting Common Issues

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `Plugin not found in agy plugin list` | Symlink broken or misplaced directory | Verify that `~/.gemini/config/plugins/skill-builder/plugin.json` exists and is readable. |
| `Plugin disabled in settings` | Marked disabled in `~/.gemini/antigravity/config.json` | Run `agy plugin enable skill-builder` or remove `"enabled": false` from config. |
| `Agent ignores 500-line limit` | Project lacks `AGENTS.md` rulebook | Ensure `AGENTS.md` is present in repository root. |
| `Error lookup script not executable` | Missing execute permissions | Run `chmod +x skills/*/scripts/*.py scripts/*.sh`. |
