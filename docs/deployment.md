# Deployment Guide

## Approach A — Student-friendly cloud
Current Supabase Free provides a managed Postgres database, authentication and storage within stated quotas. Use it for the cloud data/auth/storage layer. Deploy the FastAPI backend to a free web-service tier and the React frontend to a free static-hosting tier. Free hosting can sleep or pause, so this is appropriate for a portfolio/demo rather than a production SLA.

### Supabase
1. Create a project.
2. Run `cloud/supabase_schema.sql`.
3. Create a private `assignment-submissions` bucket.
4. Configure email/password authentication.
5. For a classroom demo, disable email confirmation if immediate account login is required.
6. Obtain project URL, anon key and server-side service-role key.
7. Obtain a Postgres connection string for `DATABASE_URL`.

### Backend environment
```env
ENVIRONMENT=cloud
AUTH_MODE=supabase
STORAGE_MODE=supabase
DATABASE_URL=<SUPABASE_POSTGRES_CONNECTION_STRING>
SECRET_KEY=<LONG_RANDOM_SERVER_SECRET>
SUPABASE_URL=<PROJECT_URL>
SUPABASE_ANON_KEY=<ANON_KEY>
SUPABASE_SERVICE_ROLE_KEY=<SERVER_ONLY_SERVICE_ROLE_KEY>
SUPABASE_BUCKET=assignment-submissions
CORS_ORIGINS=<FRONTEND_URL>
```

### Render-style backend
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables in the provider dashboard.

### Frontend
Set `VITE_API_URL` to the deployed backend URL, run `npm run build`, and deploy the `frontend/dist` static output.

## Approach B — AWS/Azure/GCP
AWS: React -> S3/CloudFront, API -> API Gateway + Lambda/App Runner/EC2, database -> RDS/DynamoDB, files -> S3, auth -> Cognito, logs -> CloudWatch.

Azure: Static Web Apps/Blob Storage + CDN, API Management + Functions/App Service, Azure Database, identity service, Azure Monitor.

GCP: Cloud Storage + Cloud CDN, API Gateway + Cloud Run/Cloud Functions, Cloud SQL/Firestore, Identity Platform, Cloud Logging/Monitoring.

## Local vs Cloud
Local mode uses SQLite, local uploads and local JWT. Cloud mode switches to managed PostgreSQL, Supabase Auth and Supabase Storage through environment variables. The application boundaries stay the same, which demonstrates portability and separation of concerns.
