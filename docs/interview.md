# Interview Preparation — 10 Questions and Answers

## 1. Explain your project.
I built a cloud-based assignment submission and feedback portal. Teachers create assignments and deadlines, while students authenticate, view assignments, upload files and receive marks and feedback. I separated relational metadata from file storage so the database does not have to store large binary documents. FastAPI exposes the REST API and enforces role permissions; cloud mode uses managed authentication, PostgreSQL and object storage.

## 2. Why use object storage instead of the database for files?
Object storage is designed for large unstructured objects and can scale independently. The database only needs the filename, storage path, status and other metadata, which keeps queries smaller and makes storage delivery easier to manage.

## 3. How is authentication different from authorization?
Authentication verifies identity. Authorization checks what an authenticated identity may do. In this project, the token identifies the user and the backend then checks whether the role is student or teacher before performing protected operations.

## 4. How does RBAC work?
Each user has a role. Student routes allow student submission and feedback access, while teacher routes allow assignment creation and grading. The backend performs these checks server-side rather than trusting the frontend.

## 5. How does the file upload work?
The student sends multipart form data. The server checks authentication, assignment existence, deadline policy, extension and size, then uploads the bytes to storage and records the storage path and submission metadata in the database.

## 6. How do you prevent students from downloading another student's file?
The download endpoint loads the submission and checks the authenticated user's ID against the submission owner. Teachers are also checked against the assignment owner. Only after authorization does the server read the stored object.

## 7. How would you scale this to 100,000 students?
I would keep the API stateless, place a load balancer/API gateway in front, autoscale compute, use managed database services, store files in object storage, cache hot reads, use queues/background workers for expensive processing, and add monitoring. Deadline spikes are especially important because many students may upload simultaneously.

## 8. How do you handle security?
I avoid hard-coded secrets, enforce HTTPS in deployment, validate inputs and uploads server-side, keep storage private, use role checks, hash local passwords, use a managed auth provider in cloud mode, restrict CORS and log security-relevant events. A production system should add malware scanning, rate limiting and stronger audit controls.

## 9. How is the project deployed?
The cloud version uses a managed database/auth/storage platform and a hosted FastAPI service plus a static React frontend. Environment variables hold URLs and secrets. The same codebase can be run locally using SQLite and a local upload directory.

## 10. What happens when something fails?
The system should not report a successful submission until storage and metadata operations succeed. Token failures return 401, authorization failures return 403, missing resources return 404, oversized files return 413, and conflicts return 409. Production systems can add retries, idempotency keys, queues and observability.
