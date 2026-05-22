# AI-Powered Task & Knowledge Management System (MVP)

## What Is Built
This project is a full-stack application that provides:
- JWT authentication with Admin and User roles
- Task creation, assignment, dynamic filtering, and status management
- Document ingestion for plain-text files with chunking and embeddings
- Production-grade semantic search backed by FAISS vector similarity
- Activity logging for user and system events
- Analytics for task and search usage
 
## Short Explanation
An AI-assisted task and knowledge management system combining a FastAPI backend and a React (Vite) frontend. Administrators can ingest documents which are chunked, embedded, and indexed for semantic search; users can create, filter, and manage tasks tied to the knowledge base.

## Tech Stack
- **Backend:** Python 3.10+ with FastAPI, Uvicorn
- **ORM / Migrations:** SQLAlchemy 2.x, Alembic
- **Database:** MySQL (primary)
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
- Frontend uses `VITE_API_BASE` to communicate with the FastAPI backend.
- Authentication is handled via JWTs; the frontend stores the access token client-side and attaches it to API requests.

## AI Workflow
1. Admin uploads a .txt file.
2. Backend chunks the text and generates embeddings.
3. Embeddings are stored in FAISS with metadata on disk.
4. Search queries are embedded and matched via FAISS similarity search.

## Setup
### Backend
1. Create a MySQL database (e.g. `ai_task_db`).
2. Set `DATABASE_URL=mysql+pymysql://root:root123@localhost:3306/ai_task_db` in `.env`.
4. Install Python dependencies:
   - `pip install -r backend/requirements.txt`
5. Run Alembic migrations (preferred):
   - `cd backend`
   - `alembic upgrade head`

   The repository includes `backend/init_db.py` to create database tables and seed default accounts when run directly. Use Alembic migrations for production environments.
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

## Features
- JWT Authentication
- Role-Based Access Control (RBAC)
- Semantic Search (embeddings)
- FAISS Vector Search
- Task Assignment and Management
- Analytics and Reporting
- Activity Logging
- Dynamic Filtering APIs

## Requirement Checklist
- [x] JWT auth + RBAC (Admin/User)
- [x] MySQL schema with PK/FK and relations
- [x] Document upload (.txt) + metadata
- [x] Chunking + embeddings + FAISS indexing
- [x] Semantic search endpoint
- [x] Task management + filtering
- [x] Activity logging
- [x] Analytics
- [x] Professional React frontend (Vite)

## Default Demo Accounts

### Admin
Email: admin@example.com
Password: admin123

### User
Email: user@example.com
Password: user123

## Future Improvements
Examples:
- PDF support and richer document formats (DOCX, HTML)
- Docker-based deployment and orchestration (Docker Compose / Kubernetes)
- Background embedding jobs (worker + queue) for asynchronous processing
- Advanced analytics and reporting dashboards

## Screenshots
_Placeholder - add screenshots for the following views:_
- Dashboard
- Semantic Search
- Task Management
- Document Upload
- Analytics

## Contributing
Contributions are welcome. Please open issues or pull requests and follow repository coding conventions. Ensure tests and linters pass before submitting a PR.

## License
This repository contains a prototype implementation. Add an appropriate open-source license file before public distribution.



