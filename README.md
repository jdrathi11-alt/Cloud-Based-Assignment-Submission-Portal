# Cloud-Based Assignment Submission Portal

A full-stack web application for managing courses, assignments, student submissions, and teacher grading using a cloud-hosted backend, PostgreSQL database, and object storage.

## Overview

The Cloud-Based Assignment Submission Portal provides a centralized workflow for teachers and students:

1. Teachers create courses and assignments.
2. Students view their assignments and deadlines.
3. Students upload assignment files.
4. Files are stored in cloud object storage.
5. Submission metadata is stored in PostgreSQL.
6. Teachers review submissions and assign marks and feedback.
7. Students can view their grades and feedback.

The application is deployed with a React frontend on Vercel and a FastAPI backend on Render, with Supabase PostgreSQL and Supabase Storage used as managed cloud services.

## Live Deployment

- **Frontend:** https://frontend-six-jet-64.vercel.app/
- **Backend API:** https://cloud-based-assignment-submission-portal-3w3n.onrender.com
- **API documentation:** https://cloud-based-assignment-submission-portal-3w3n.onrender.com/docs
- **Health check:** https://cloud-based-assignment-submission-portal-3w3n.onrender.com/health

> The backend root URL returning `{"detail":"Not Found"}` is expected because the application exposes API routes rather than a homepage. Users should open the Vercel frontend.

## Features

### Student

- Register and log in
- View available assignments
- View assignment details and deadlines
- Upload supported assignment files
- Submit assignments to cloud storage
- View submission status
- View marks and teacher feedback

### Teacher

- Register and log in
- Create courses
- Create assignments
- Configure deadlines
- Configure maximum marks
- Configure allowed file types
- Configure maximum upload size
- View student submissions
- Grade submissions
- Provide feedback

### Backend

- REST API built with FastAPI
- JWT-based authentication/session flow
- Role-based authorization
- Server-side file validation
- Deadline validation
- Submission status management
- PostgreSQL persistence
- Cloud object-storage integration
- CORS configuration
- API documentation through Swagger/OpenAPI

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL via Supabase |
| Object Storage | Supabase Storage |
| Authentication | JWT-based application authentication |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| API Documentation | FastAPI Swagger/OpenAPI |
| Version Control | Git + GitHub |

## Cloud Architecture

```text
                    ┌──────────────────────┐
                    │      Student /       │
                    │       Teacher        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React + Vite       │
                    │   Vercel Frontend    │
                    └──────────┬───────────┘
                               │ HTTPS / REST API
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI Backend  │
                    │      Render          │
                    └───────┬───────┬──────┘
                            │       │
                metadata    │       │ files
                            ▼       ▼
                 ┌──────────────┐  ┌─────────────────┐
                 │  PostgreSQL  │  │ Supabase Storage│
                 │  Supabase    │  │ Object Storage  │
                 └──────────────┘  └─────────────────┘
```

### Request and data flow

**Authentication**

```text
Browser → Vercel → Render API → PostgreSQL
```

**Assignment creation**

```text
Teacher → Vercel → FastAPI → PostgreSQL
```

**Assignment submission**

```text
Student
   ↓
Vercel
   ↓
FastAPI
   ├── validate file/deadline
   ├── upload file → Supabase Storage
   └── save metadata → PostgreSQL
```

**Grading**

```text
Teacher → FastAPI → PostgreSQL
                         ↓
                  marks + feedback
                         ↓
Student Dashboard
```

## Database Design

The application uses the following main tables:

### `users`

Stores application users and their roles.

Important fields:

- `id`
- `auth_uid`
- `name`
- `email`
- `password_hash`
- `role`
- `created_at`

Roles currently supported:

- `student`
- `teacher`

### `courses`

Stores courses created by teachers.

Important fields:

- `id`
- `course_name`
- `teacher_id`
- `created_at`

### `assignments`

Stores assignment information.

Important fields:

- `id`
- `course_id`
- `title`
- `description`
- `deadline`
- `max_marks`
- `created_by`
- `allowed_file_types`
- `max_file_size_mb`
- `created_at`

### `submissions`

Stores submission metadata and grading information.

Important fields:

- `id`
- `assignment_id`
- `student_id`
- `file_name`
- `file_url`
- `storage_path`
- `submitted_at`
- `submission_status`
- `marks`
- `feedback`
- `graded_at`

### Why files are not stored directly in PostgreSQL

The database stores submission metadata, while the actual uploaded file is stored in object storage. This keeps the database focused on structured application data and allows files to be managed separately through cloud storage.

## Cloud Storage

The project uses a private Supabase Storage bucket:

```text
assignment-submissions
```

Files are organized using paths similar to:

```text
assignments/
  assignment_<assignment_id>/
    student_<student_id>/
      <unique-file-name>.pdf
```

A unique generated filename helps avoid collisions when students upload files with the same original filename.

## Submission Validation

The backend validates:

- Student authentication
- Assignment existence
- File extension
- Maximum file size
- Submission status
- Deadline
- Resubmission rules

Default allowed file types are:

```text
pdf, docx, zip
```

The default maximum file size is:

```text
10 MB
```

## Submission Status

The application uses statuses including:

- `SUBMITTED`
- `LATE`
- `GRADED`

Deadline comparisons are performed server-side using UTC-aware timestamps to avoid timezone-related inconsistencies between local development and cloud deployment.

## REST API

### Authentication

```text
POST /api/register
POST /api/login
```

### Courses

```text
GET  /api/courses
POST /api/courses
```

### Assignments

```text
GET  /api/assignments
POST /api/assignments
```

### Submissions

```text
POST /api/assignments/{assignment_id}/submit
GET  /api/submissions/me
GET  /api/assignments/{assignment_id}/submissions
GET  /api/submissions/{submission_id}/download
```

### Grading

```text
POST /api/submissions/{submission_id}/grade
```

The complete interactive API specification is available through the deployed Swagger UI:

https://cloud-based-assignment-submission-portal-3w3n.onrender.com/docs

## Project Structure

```text
Cloud-Based-Assignment-Submission-Portal/
│
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routers/
│   │   │   ├── assignments.py
│   │   │   ├── auth.py
│   │   │   ├── courses.py
│   │   │   ├── dashboard.py
│   │   │   └── submissions.py
│   │   └── services/
│   │       └── storage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── services/
│           └── api.js
│
├── cloud/
├── docs/
├── tests/
├── sample_files/
├── README.md
├── render.yaml
└── .gitignore
```

## Environment Variables

The backend uses environment variables for configuration and secrets.

Typical variables include:

```text
DATABASE_URL
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
SUPABASE_BUCKET
STORAGE_MODE
ENVIRONMENT
CORS_ORIGINS
SECRET_KEY
```

The frontend uses:

```text
VITE_API_URL
```

### Security rule

Never commit `.env` files, database passwords, Supabase service-role keys, JWT secrets, or other credentials to GitHub.

The project's `.gitignore` should exclude local environment files and the Python virtual environment.

## Local Development

### Backend

From the project root:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Frontend

Open another terminal:

```powershell
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

For local development, configure the frontend API URL through `VITE_API_URL`.

## Deployment

### Backend — Render

The backend is deployed as a Render web service using the project's Dockerfile.

Important cloud configuration includes:

- PostgreSQL `DATABASE_URL`
- Supabase URL
- Supabase service-role key
- Supabase storage bucket
- Cloud storage mode
- CORS origins

### Frontend — Vercel

The React/Vite frontend is deployed on Vercel.

The frontend receives the backend URL through:

```text
VITE_API_URL
```

Current production API:

```text
https://cloud-based-assignment-submission-portal-3w3n.onrender.com
```

## Testing Performed

The deployed application has been manually tested through the complete workflow:

1. Student registration
2. Teacher registration
3. Student login
4. Teacher login
5. Course creation
6. Assignment creation
7. Assignment visibility for students
8. File type validation
9. File upload
10. Cloud storage upload
11. Submission record creation
12. Teacher review
13. Grading
14. Feedback
15. Student viewing marks and feedback

The deployed end-to-end flow was successfully verified.

## Deployment Problems Resolved During Development

Several real deployment issues were identified and fixed during development:

- Passlib/bcrypt compatibility
- Missing Vercel API environment variable
- CORS configuration for the Vercel origin
- Naive/aware datetime comparison for deadlines
- Missing Supabase storage configuration
- Missing PostgreSQL driver
- Non-persistent local SQLite database on Render
- Incorrect PostgreSQL connection configuration
- Supabase connection routing/network configuration

These issues were useful for validating the application's cloud deployment rather than only testing it locally.

## Security Considerations

The application includes:

- Password hashing
- Authentication
- Role-based authorization
- Protected API endpoints
- Server-side validation
- Private object storage
- Environment-based secret configuration
- CORS configuration
- File type and size validation

### Production hardening still recommended

Before treating the system as a production application, review:

- Supabase Row Level Security (RLS)
- Supabase Storage policies
- Rate limiting
- More restrictive CORS configuration
- Secret rotation
- Audit logging
- Automated backups
- Monitoring and alerting
- More comprehensive automated tests

## Scalability

The architecture separates:

- Frontend hosting
- API/backend processing
- Relational database
- Object storage

This separation allows the individual components to scale independently.

For a larger deployment, additional techniques could include:

- Backend horizontal scaling
- Load balancing
- CDN caching
- Database indexing and connection pooling
- Object-storage lifecycle policies
- Background job queues
- Monitoring and centralized logging

## Results

The final deployed application successfully demonstrates a cloud-based assignment lifecycle:

```text
Teacher creates course
        ↓
Teacher creates assignment
        ↓
Student views assignment
        ↓
Student uploads file
        ↓
File stored in cloud object storage
        ↓
Submission metadata stored in PostgreSQL
        ↓
Teacher reviews submission
        ↓
Teacher assigns marks + feedback
        ↓
Student views result
```

## Limitations

This project is primarily an educational cloud-computing/full-stack application. Before use in a large institution, it would benefit from additional enterprise features such as:

- Administrative management
- Institutional SSO
- Email notifications
- More granular permissions
- Stronger storage policies
- Comprehensive automated testing
- Advanced monitoring
- Backup and disaster-recovery procedures

## Future Improvements

Potential enhancements include:

- Admin dashboard
- Course enrollment management
- Email deadline reminders
- Assignment version history
- Multiple submissions with version tracking
- Plagiarism detection integration
- File preview
- Advanced analytics
- Exportable grade reports
- Institutional authentication
- Automated notifications
- Audit logs

## Learning Outcomes

This project demonstrates practical experience with:

- Full-stack web development
- REST API design
- Authentication and authorization
- Relational database design
- PostgreSQL
- Cloud object storage
- File upload handling
- Cloud deployment
- Environment-based configuration
- CORS
- Git/GitHub
- Docker-based backend deployment
- Frontend hosting
- Debugging production deployment issues
- Cloud architecture

## Demo Flow

For a project demonstration, use this sequence:

1. Open the Vercel application.
2. Log in as a teacher.
3. Create/select a course.
4. Create an assignment.
5. Log out.
6. Log in as a student.
7. Open the assignment.
8. Upload a PDF/DOCX file.
9. Show successful submission.
10. Log in as the teacher.
11. Open the submission.
12. Grade it and add feedback.
13. Log in as the student.
14. Show the marks and feedback.

## Repository

GitHub:

https://github.com/jdrathi11-alt/Cloud-Based-Assignment-Submission-Portal

## Author

Developed as a cloud-computing project demonstrating a complete assignment submission and feedback workflow using modern web and managed cloud services.
