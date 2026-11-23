# Playbook: Categorized Multi-Skill Combos (`combo-stacks`)

Invoke a categorized multi-skill combo when a project spans multiple layers (e.g., Frontend + Backend + AI/CV/VLM + Testing) while pruning unrelated platform skills to preserve context tokens.

## 1. Fullstack & Web Product Combos
- **`combo-fullstack-web`**: `/architect` + `/fullstack` + `/backend` + `/api-design` + `/database` + `/frontend` + `/web-ui` + `/routing` + `/state-management` + `/testing` + `/security` *(prunes `/mobile-ui`, `/3d`)*
- **`combo-landing-brand`**: `/anti-slop` + `/ui` + `/web-ui` + `/brand-assets` + `/2d-mascot-motion` + `/3d` + `/performance` *(prunes `/mobile-ui`, `/database`)*

## 2. AI, Computer Vision, VLM & Local LLM Combos
- **`combo-cv-vlm-edge`**: `/computer-vision` + `/vlm-multimodal` + `/local-llm` + `/ai-integration` + `/performance` + `/testing` *(prunes `/web-ui`, `/mobile-ui` unless UI flagged)*
- **`combo-hybrid-ai-app`**: `/ai` + `/local-llm` + `/ai-integration` + `/backend` + `/frontend` + `/web-ui` + `/security` + `/testing` *(prunes `/mobile-ui`)*

## 3. Mobile & Offline-First Combos
- **`combo-mobile-offline`**: `/mobile-ui` + `/frontend` + `/routing` + `/state-management` + `/local-first-data` + `/qa` + `/testing` *(prunes `/web-ui`)*

## 4. Cloud, Serverless & Data Pipeline Combos
- **`combo-cloud-data`**: `/gcp` + `/aws` + `/firebase` + `/supabase` + `/devops` + `/database` + `/data-pipelines` + `/observability` + `/security` *(prunes client UI skills)*

## 5. MCP, Browser Media & Desktop Combos
- **`combo-mcp-media`**: `/mcp-engineering` + `/browser-media-wasm` + `/local-first-data` + `/security` + `/testing` *(prunes cloud infra unless flagged)*

## 6. Audit, A/B Testing, Refactor & Release Combos
- **`combo-ab-ship`**: `/code-archaeology` + `/testing` (A/B + TDD/E2E) + `/qa` + `/interrogate` + `/prove-it-works` + `/git-workflow`
- **`combo-safe-refactor`**: `/code-archaeology` + `/refactor` + `/testing` + `/interrogate` + `/prove-it-works`

## Usage
```bash
python3 skills/darknecrostack/scripts/route_task.py --combo combo-cv-vlm-edge --path .
```
