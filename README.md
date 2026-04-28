# BookForge

BookForge is a web product that packages the private Cowork book-production pipeline into a browser-based experience for indie authors.

This repository is intentionally isolated from the live `D:\Cowork\KDP` production workflow. It follows the structure described in `D:\Cowork\KDP\Startup\BookForge_Architecture_Spec.md`.

## Layout

- `frontend/` - Next.js app router frontend
- `backend/` - FastAPI backend and worker logic
- `shared/` - shared stage constants and schema references

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn main:app --reload
```

### Infra

```bash
docker compose up -d
```

## Notes

- This is a scaffold, not the finished product.
- Python is pinned in `pyproject.toml` to avoid accidental dependency drift.
- Environment variables are documented in `.env.example` files.
