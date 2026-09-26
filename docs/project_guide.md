# Project Guide

## 1. Simple Explanation
This portal is a shared online classroom workspace. A teacher posts an assignment. A student logs in from any location, reads the instructions, uploads the work, and receives a status. The teacher opens the stored submission, records marks and written feedback, and the student later sees the result.

## 2. Technical Explanation
The browser is the client. React calls FastAPI REST endpoints. Authentication produces an access token. FastAPI checks that token and the user's role. Assignment and submission metadata are relational records. The uploaded document is an object in storage. Only metadata such as filename, storage path, timestamps, status, marks and feedback is stored in the database.

Workflow:
```text
Teacher -> Create Assignment -> Cloud Database -> Student Dashboard
Student -> Upload -> Object Storage -> Submission Metadata -> Teacher Review
Teacher -> Marks + Feedback -> Cloud Database -> Student Feedback View
```

## 3. Industry Relevance
The same separation appears in LMS platforms, university portals, school systems, corporate training, certification platforms, bootcamps and EdTech. The pattern centralizes data, enables remote access, scales storage independently from database records, and creates an auditable workflow.

## 4. Cloud Concepts and Where They Appear
| Concept | Where it appears |
|---|---|
| Cloud computing | Hosted frontend/API/database/storage |
| SaaS | The finished portal is consumed through a browser |
| PaaS | Render/Supabase managed application services |
| IaaS | Optional AWS EC2/Azure VM/GCP Compute Engine mapping |
| Cloud database | Supabase PostgreSQL |
| Object storage | Supabase Storage |
| Authentication | Local JWT or Supabase Auth |
| Authorization | FastAPI role checks |
| RBAC | `student` and `teacher` permissions |
| REST API | `/api/...` endpoints |
| Client-server | React client -> FastAPI server |
| Serverless | Optional mapping to Lambda/Functions |
| Scalability | Stateless API + managed database/storage |
| Elasticity | Autoscaling/serverless mapping |
| Availability | Managed services and multiple service instances in production |
| Load balancing | Cloud load balancer in advanced architecture |
| CDN | Static frontend assets |
| API Gateway | Optional managed API entry point |
| Environment variables | `.env` configuration |
| Secrets | Service-role/database credentials kept server-side |
| Logging | Application and platform logs |
| Monitoring | Health endpoint and cloud metrics |
| Backup | Managed DB backup strategy in production |
| CI/CD | GitHub -> deployment provider |

## 5. Technology Options
### Option A — Beginner
HTML/CSS/JS + Flask + SQLite + local uploads. Difficulty: low. Cost: zero locally. Demonstrates client-server, CRUD, REST and file handling, but limited cloud depth.

### Option B — Recommended
React + FastAPI + Supabase Auth + Supabase PostgreSQL + Supabase Storage + free-tier hosting. Difficulty: medium. Demonstrates the requested cloud concepts without requiring a large AWS bill.

### Option C — Advanced
React/Next.js + FastAPI + API Gateway + serverless functions/containers + managed SQL/NoSQL + object storage + authentication + monitoring on AWS/Azure/GCP. Difficulty: high. Strong architecture learning, but more configuration and cost-control responsibility.

## 6. Roles
| Action | Student | Teacher | Optional Admin |
|---|---|---|---|
| Register/login | Yes | Yes | Yes |
| View assignments | Yes | Yes | Yes |
| Create assignment | No | Yes | Yes |
| Update/delete own assignment | No | Yes | Yes |
| Upload own work | Yes | No | No |
| View own submission | Yes | No | No |
| View permitted submissions | No | Yes | Yes |
| Grade | No | Yes | Yes |
| Feedback | Read own | Write | Yes |
| Manage users/courses | No | Course-only | Yes |

## 7. Database Design
Entities are `users`, `courses`, `assignments`, and `submissions`. Primary keys identify rows. Foreign keys connect teacher -> course -> assignment -> submission -> student. Indexes support email lookup, role lookup, assignment deadlines, assignment ownership, and submission queries.

Files are not normally stored as binary database fields because object storage is designed for large files, independent scaling, access policies and content delivery. The database keeps the reference and metadata.

## 8. Storage Design
```text
assignments/
  assignment_001/
    student_001/<random-id>.pdf
    student_002/<random-id>.pdf
```
A random UUID prevents predictable filename collisions. In a stronger production design, files remain private and the API returns short-lived signed URLs.

## 9. Deadline Logic
The server records the timestamp. If `submitted_at <= deadline`, status is `SUBMITTED`; otherwise it is `LATE`. A configuration flag can reject late submissions. Client clocks are not trusted because they can be changed.

## 10. Failure Handling
- Upload failure: return an error and do not create a successful submission record.
- Database failure: return a controlled 5xx response and log correlation information.
- Storage failure: preserve existing metadata and allow retry; avoid reporting success before storage completes.
- Expired token: return 401 and require re-authentication/refresh.
- Duplicate request: database uniqueness on `(assignment_id, student_id)` prevents duplicate logical submissions.
- Connection drop: the browser can retry the upload; a production system can use resumable/multipart upload.
- Backend failure: a stateless deployment can route a later request to another instance.

Idempotency means repeating the same logical request does not create multiple logical results. The unique submission constraint is one basic protection; a production API can accept an explicit idempotency key.

## 11. Security
Authentication answers “who are you?” Authorization answers “what can you do?”. The project combines both. HTTPS protects data in transit. Managed storage/database services generally provide encryption at rest. Password hashing is delegated to Supabase Auth in cloud mode or bcrypt in local mode. File type/size validation is server-side. Malware scanning is a recommended production addition. Service-role keys must never reach the browser.

Common mistakes: trusting client-side role fields, trusting client clocks, public storage buckets, hard-coded credentials, unrestricted CORS, missing authorization checks, storing raw passwords, and treating a file extension as proof that a file is safe.

## 12. Scalability
10 students: one API instance, managed database and object storage are sufficient.

1,000 students: add a managed database, caching for frequently read assignment data, a CDN for frontend assets, and autoscaling API instances.

100,000 students: keep the API stateless, put a load balancer/API gateway in front, autoscale compute, use object storage for files, queue expensive work such as scanning/notifications, use database indexes/read replicas where appropriate, cache hot reads, and monitor queue depth/error rates.

For a deadline surge, uploads should go directly to object storage when possible, metadata writes should be small transactions, background workers should process scanning/notifications, and the database should not carry file bytes.

## 13. Cloud Architecture Mapping
```text
Users
  |
 CDN / Frontend Hosting
  |
 API Gateway / Load Balancer
  |
 FastAPI containers or serverless functions
  |------------------|
  v                  v
Managed PostgreSQL   Object Storage
  |
Auth Provider        Monitoring / Logs
```
AWS example: S3/CloudFront, API Gateway, Lambda/App Runner/EC2, RDS/DynamoDB, S3, Cognito, CloudWatch. Azure: Static Web Apps/Blob Storage/CDN, API Management/Functions/App Service, Azure Database, Entra ID/B2C-style identity services, Monitor. GCP: Cloud Storage/Cloud CDN, API Gateway/Cloud Run/Cloud Functions, Cloud SQL/Firestore, Identity Platform, Cloud Logging/Monitoring.
