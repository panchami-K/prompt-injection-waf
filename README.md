---
title: Prompt Injection WAF
emoji: 🛡️
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
---

# Prompt Injection Red-Team WAF Environment

An OpenEnv reinforcement learning environment where an AI attacker attempts
prompt injection attacks to bypass an AI Web Application Firewall (WAF) defender.

## Tasks

- **direct_injection** — Bypass an easy WAF in a single attempt
- **multi_turn** — Bypass a medium WAF across up to 5 attempts  
- **jailbreak_chain** — Bypass a hard WAF using chained jailbreak across 7 attempts

## API Endpoints

- `GET /health` — Health check
- `POST /reset` — Reset episode
- `POST /step` — Take an action
- `GET /state` — Get episode state