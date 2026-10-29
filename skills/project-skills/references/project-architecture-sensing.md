# Project Architecture Sensing & Dependency Fingerprinting

---

## 1. Fingerprint Detection Matrix

Manifest File | Detected Technology | Minted Skill Target
:--- | :--- | :---
`Cargo.toml` | Rust systems service | `rust-production`
`go.mod` | Go microservice | `go-microservices`
`pubspec.yaml` | Flutter application | `flutter-architecture`
`hardhat.config.js` | Ethereum smart contracts | `solidity-security`
`dbt_project.yml` | Data transformation pipeline | `dbt-analytics`

---

## 2. CLI Execution

Use `scripts/synthesize_project_skill.py`:
```bash
python3 skills/project-skills/scripts/synthesize_project_skill.py \
    --name "stripe-billing-flow" \
    --description "Handles webhook signature verification and subscription invoice lifecycle."
```
