# AI-Powered Task & Knowledge Management System (MVP)

## What Is Built
This project is a full-stack MVP that provides:
- JWT authentication with Admin/User roles
- Task creation, assignment, filtering, and status updates
- Document upload for .txt files with chunking + embeddings
- Local semantic search using sentence-transformers + FAISS
- Activity logging for login, task updates, document uploads, and search
- Analytics for task stats and most searched queries
 
## Short Explanation
A lightweight AI-assisted task and knowledge management MVP combining a FastAPI backend and a React (Vite) frontend. Admins upload text documents which are chunked, embedded, and indexed locally for semantic search; users can create and manage tasks tied to that knowledge base.

## Tech Stack
- **Backend:** Python 3.10+ with FastAPI, Uvicorn
- **ORM / Migrations:** SQLAlchemy 2.x, Alembic
- **Database:** MySQL (primary) with optional SQLite fallback for local dev
- **Auth / Security:** JWT via python-jose
- **Embeddings / Vector DB:** sentence-transformers (`all-MiniLM-L6-v2`) and FAISS (faiss-cpu)
- **Frontend:** React, Vite, Axios
- **Dev / Tooling:** Node.js / npm, pip

## Folder Structure
```
backend/
  app/
    ai/
    config/
    database/
    middleware/
    models/
    repositories/
    routers/
    schemas/
    services/
    utils/
  alembic/
frontend/
  src/
    components/
    context/
    hooks/
    layouts/
    pages/
    services/
```

## API Flow
- `/api/auth/login` issues a JWT.
- Protected endpoints require `Authorization: Bearer <token>`.
- Admin-only actions: create tasks, upload documents, analytics.
- Users can view their tasks and update their status.

## Frontend/Backend Connection
- Frontend uses `VITE_API_BASE` to talk to the FastAPI backend.
- The JWT is stored in localStorage and added to each request.
- The frontend also supports a demo mode by default, so the UI can open even when no SQL data exists.
- Set `VITE_DEMO_MODE=false` if you want the frontend to require a real backend login again.

## AI Workflow
1. Admin uploads a .txt file.
2. Backend chunks the text and generates embeddings.
3. Embeddings are stored in FAISS with metadata on disk.
4. Search queries are embedded and matched via FAISS similarity search.

## Setup
### Backend
1. Create a MySQL database (e.g. `ai_task_db`).
2. Set `DATABASE_URL=mysql+pymysql://root:root%20123@localhost:3306/ai_task_db` in `.env`.
3. If you need local-only fallback, set `ALLOW_SQLITE_FALLBACK=true`.
4. Install Python dependencies:
   - `pip install -r backend/requirements.txt`
5. Run Alembic migrations (preferred):
   - `cd backend`
   - `alembic upgrade head`

   If you don't have a running MySQL instance or Alembic setup locally, you can use the provided init script which will create tables and seed a default admin user (falls back to SQLite if MySQL is unreachable):

   - From repo root run:

```bash
python backend/init_db.py
```
6. Start the API:
   - `uvicorn app.main:app --reload`

### Frontend
1. Install dependencies:
   - `cd frontend`
   - `npm install`
2. Start the dev server:
   - `npm run dev`

## Required APIs
- `POST /api/auth/login`
- `GET/POST /api/tasks`
- `PATCH /api/tasks/{id}`
- `POST /api/documents`
- `POST /api/search`
- `GET /api/analytics`

## Requirement Checklist
- [x] JWT auth + RBAC (Admin/User)
- [x] MySQL schema with PK/FK and relations
- [x] Document upload (.txt) + metadata
- [x] Chunking + embeddings + FAISS indexing
- [x] Semantic search endpoint
- [x] Task management + filtering
- [x] Activity logging
- [x] Analytics
- [x] Simple React UI pages



