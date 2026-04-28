# BookForge

**AI book production studio for indie Kindle authors.**

BookForge takes an indie author from "I have a book idea" to "Kindle-ready manuscript" through a visual pipeline. Two interaction modes (chat + form), one Factorio-style dashboard, 30+ specialized agents running writing, continuity gates, editing, and assembly.

This repo is the public scaffold. The proprietary continuity engine (canon ledger + raw-text continuity scanner) and Voice DNA tuning live in a private repo, validated against 50+ KDP-published manuscripts shipped under five pen names.

## Status

Pre-seed. Applying to **a16z Speedrun SR007** (Summer/Fall 2026).

- **50+ books** shipped via the underlying pipeline (Sep 2025 – Apr 2026)
- **35,000+ units sold** on Amazon KDP
- **71% net margin**
- **3.5x ROAS** at 28.5% ACoS on Amazon Ads
- **Time-to-publication compressed 60%** vs. indie author baseline (~3 weeks → 5–7 days)
- **Cost per book: $15–$40** of model spend

## Stack

- **Frontend:** Next.js 14 (App Router) + Tailwind + Supabase Auth
- **Backend:** FastAPI (Python 3.12) + async workers
- **Data:** Supabase Postgres + Redis (BullMQ) + Supabase Storage
- **Models:** Claude Sonnet 4 (pipeline work) + Claude Haiku 4 (classification + gating)
- **Infra:** Vercel (frontend) + Railway (backend) + Supabase (data)

## Layout

- `frontend/` — Next.js app (chat UI, form wizard, Factorio pipeline view)
- `backend/` — FastAPI orchestrator, prompt engine, worker pool
- `shared/` — stage constants and schema references

## Local development

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local   # fill in Supabase keys
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
cp .env.example .env         # fill in Anthropic + Supabase keys
uvicorn main:app --reload
```

### Infra (optional, local Postgres + Redis)

```bash
docker compose up -d
```

## Founder

[Serhii Komar](https://www.linkedin.com/in/serhii-komar) — 16 years in mobile games. Most recently Sr PM at AppLovin (scaled Merge Sticker Playbook from $30K to $600K MRR in 4 months; grew Found It! revenue +137%). Founded Komar Games, Mizar Games, Play Cute. Building BookForge solo, hiring CTO co-founder with Speedrun's first dollar.

## License

Proprietary. All rights reserved. The scaffold is public for review; commercial use requires written permission.
