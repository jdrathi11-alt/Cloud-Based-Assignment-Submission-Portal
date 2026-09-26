# Cloud-Based Student Assignment Submission & Feedback Portal

A full-stack cloud-computing project for assignment creation, secure file submission, grading, feedback, role-based access control, cloud database/object storage integration, and deployment.

## Overview
Teachers create assignments and deadlines. Students authenticate, view assignments, upload files, resubmit where permitted, and see grades/feedback. Submission metadata belongs in a relational database while files belong in object storage.

## Architecture
```text
Student / Teacher
       |
       v
 React + Vite frontend
       |
       v
 FastAPI REST API
   |           |
   v           v
Auth       PostgreSQL/Supabase
               |
               v
        Supabase Storage
               |
               v
         Logs / Monitoring
```

Cloud deployment can place the React static site behind a CDN and the FastAPI service behind a managed HTTPS endpoint/API gateway.

## Technology Stack
- Frontend: React + Vite
- Backend: Python FastAPI
- Local database: SQLite + SQLAlchemy
- Cloud database: PostgreSQL through Supabase
- Cloud authentication: Supabase Auth in `AUTH_MODE=supabase`
- Object storage: Supabase Storage in `STORAGE_MODE=supabase`
- Local storage fallback: `backend/uploads/`
- Testing: pytest + FastAPI TestClient
- Deployment: Render or equivalent free-tier student hosting

## Local Setup
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
uvicorn app.main:app --reload
```

In a second terminal:
```bash
cd frontend
npm install
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
npm run dev
```

Open the Vite URL shown by the terminal, normally `http://localhost:5173`.

## Cloud Setup
1. Create a Supabase project.
2. Create a Storage bucket named `assignment-submissions` and keep it private.
3. Run `cloud/supabase_schema.sql` in the SQL editor.
4. For a classroom demo, configure Supabase Auth email/password and disable email confirmation if you want immediate demo logins.
5. Set backend `AUTH_MODE=supabase`, `STORAGE_MODE=supabase`, a Supabase Postgres `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY`.
6. Deploy `backend` as a web service.
7. Set `VITE_API_URL` to the deployed API URL and deploy `frontend` as a static site.

Never put the Supabase service-role key in the frontend or GitHub.

## Core REST API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register` | Register user |
| POST | `/api/login` | Login |
| POST | `/api/logout` | Logout acknowledgement |
| GET | `/api/courses` | List courses |
| POST | `/api/courses` | Create teacher course |
| GET | `/api/assignments` | List assignments |
| GET | `/api/assignments/{id}` | Assignment details |
| POST | `/api/assignments` | Create assignment |
| PUT | `/api/assignments/{id}` | Update assignment |
| DELETE | `/api/assignments/{id}` | Delete assignment |
| POST | `/api/assignments/{id}/submit` | Upload submission |
| GET | `/api/submissions/me` | Student submissions |
| GET | `/api/assignments/{id}/submissions` | Teacher review list |
| GET | `/api/submissions/{id}` | Authorized submission details |
| POST | `/api/submissions/{id}/grade` | Grade + feedback |
| GET | `/api/submissions/{id}/feedback` | Student feedback |
| GET | `/api/submissions/{id}/download` | Secure file download |
| GET | `/api/dashboard` | Role-specific dashboard metrics |

## Security
- Authentication tokens protect API routes.
- Role checks stop students from grading or accessing teacher-only data.
- Students can only retrieve their own private submissions.
- Teacher access is restricted to assignments they created.
- File extension and size are validated server-side.
- Storage paths use assignment/student IDs plus a random UUID.
- Secrets are environment variables.
- HTTPS should be used in cloud deployment.
- Production systems should add malware scanning, rate limiting, centralized audit logs, backups, stronger RLS, and managed secrets.

## Cloud Concepts Demonstrated
Cloud computing, SaaS, PaaS, managed database, object storage, authentication, authorization, RBAC, REST, client-server architecture, serverless mapping, scalability, elasticity, availability, load balancing, CDN, API gateway, environment variables, secrets management, logging, monitoring, backup, CI/CD, and cloud deployment.

## Testing
```bash
cd backend
pytest ../tests -q
```

## GitHub
Suggested repository: `Cloud-Based-Assignment-Submission-Portal`

Suggested commits:
- Initialize cloud assignment portal
- Create frontend and backend architecture
- Implement authentication and role management
- Add assignment management module
- Integrate cloud database
- Implement cloud file storage
- Add student assignment submission workflow
- Implement deadline validation
- Add teacher grading and feedback
- Build student and teacher dashboards
- Add security and authorization
- Add automated tests
- Deploy application to cloud
- Complete README and documentation

## Limitations
This is a student/portfolio implementation. Free cloud services can have quotas, sleeping services, paused projects, limited storage, and no production-grade disaster recovery. The project deliberately uses dummy users and sample coursework.

## Future Improvements
Add email notifications, background jobs, malware scanning, plagiarism integration, course enrollment, admin workflows, audit-event storage, signed URLs with short expiry, rate limiting, Redis caching, queues, CDN delivery, CI/CD tests, and infrastructure-as-code.
