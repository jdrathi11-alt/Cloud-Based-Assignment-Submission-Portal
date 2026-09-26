# Project Report — Cloud-Based Student Assignment Submission & Feedback Portal

## Abstract
The Cloud-Based Student Assignment Submission & Feedback Portal is a web application that demonstrates cloud computing through managed authentication, relational data, object storage, REST APIs, role-based authorization, secure file handling, deployment, testing and scalability design. Teachers publish assignments and review submissions; students upload work and receive marks and feedback.

## Introduction
Traditional assignment workflows depend on paper, email attachments or scattered storage. This project centralizes coursework metadata and submission files behind authenticated web access.

## Problem Statement
Students need a consistent way to access deadlines and submit work. Teachers need a central place to track submissions, retrieve files, grade work and communicate feedback.

## Objectives
- provide role-based student and teacher workflows
- separate database metadata from file objects
- expose REST APIs
- support local development and cloud deployment
- demonstrate security, scalability and failure handling
- create reproducible GitHub proof of work

## Existing System
Email, local folders and paper-based workflows can make status tracking and centralized access difficult.

## Proposed System
A React frontend communicates with FastAPI. Authentication protects requests. PostgreSQL/Supabase stores structured records and Supabase Storage stores assignment files. The backend enforces role permissions.

## User Roles
Students register/login, view assignments, upload/resubmit, download their files and read grades/feedback. Teachers create assignments, set deadlines, review submissions and grade. An admin role is a future extension.

## Cloud Computing Concepts
The project demonstrates SaaS usage, PaaS/managed services, cloud database, object storage, authentication, RBAC, REST, client-server architecture, serverless mapping, scalability, elasticity, availability, load balancing, CDN, API gateway, environment variables, secrets, logging, monitoring, backup, CI/CD and cloud deployment.

## Technology Stack
React/Vite, FastAPI, SQLAlchemy, SQLite for local mode, PostgreSQL/Supabase for cloud mode, Supabase Auth, Supabase Storage, pytest, Render/static hosting.

## System Architecture
```text
User -> React -> FastAPI -> Auth
                    |-> PostgreSQL
                    |-> Object Storage
                    |-> Logs/Monitoring
```

## Database Design
Users own roles. Teachers own courses. Courses contain assignments. Students create submissions for assignments. Foreign keys maintain relationships. Indexes improve common lookup paths.

## Cloud Storage Design
Files are stored under assignment/student prefixes. Metadata stores file name, storage path, timestamp and status. Private object storage plus controlled download endpoints reduces accidental exposure.

## Authentication and Authorization
Cloud mode uses Supabase Auth for identity and FastAPI for application-level authorization. Local mode uses bcrypt password hashes and signed JWTs. Role checks protect teacher-only and student-only operations.

## Assignment Management
Teachers create, update and delete assignments. Input includes title, description, course, deadline, maximum marks, allowed extensions and maximum file size.

## Submission Workflow
The server authenticates the student, validates assignment existence, deadline, extension and file size, uploads the file, then stores metadata. Status is `SUBMITTED` or `LATE`. A unique assignment/student constraint supports controlled resubmission.

## Deadline Management
Server-side UTC timestamps are compared with the assignment deadline. The client clock is not trusted. Late submission can be allowed or rejected through configuration.

## Feedback and Grading
Authorized teachers can assign marks up to the maximum and enter feedback. Students can read their own result but cannot change it.

## API Design
The API follows resource-oriented HTTP methods and uses JSON for metadata and multipart form data for files. `401` indicates authentication failure, `403` authorization failure, `404` missing resources, `409` conflicts and `413` oversized files.

## Implementation
The backend is modular: configuration, database, models, schemas, authentication, storage service and routers. The frontend has authentication, student and teacher dashboards and a reusable API service.

## Testing
The repository includes automated health and authentication tests plus a 25-case manual/acceptance test plan.

## Cloud Deployment
A student-friendly deployment uses Supabase for cloud auth/database/storage and a free web-service/static-hosting provider for the FastAPI and React components. A higher-scale architecture can map the same boundaries to AWS, Azure or GCP.

## Security
Security controls include authentication, authorization, input validation, server-side file checks, private storage, environment variables, HTTPS, restricted CORS and no credential commits. Production enhancements include malware scanning, rate limiting, centralized audit logging and managed secrets.

## Scalability
Object storage keeps large files outside the database. Stateless APIs can scale horizontally. A load balancer, autoscaling, caching, queues and background workers can absorb deadline spikes.

## Results
The completed system provides a reproducible workflow from login to assignment creation, submission, storage, review, grading and feedback.

## Advantages
Centralized records, remote access, independent file scaling, structured APIs, clear authorization boundaries and a deployable architecture.

## Limitations
Free-tier services have quotas and may pause/sleep. The sample application does not include enterprise-grade malware scanning, full audit logging, advanced notifications or disaster recovery.

## Future Scope
Notifications, plagiarism detection, course enrollment, admin console, background jobs, signed URLs, Redis caching, queues, CDN optimization, CI/CD gates and infrastructure-as-code.

## Conclusion
The project demonstrates that a seemingly simple assignment portal can be decomposed into cloud-native services: identity, API compute, managed relational data and object storage. This separation is the main cloud-computing learning outcome.
