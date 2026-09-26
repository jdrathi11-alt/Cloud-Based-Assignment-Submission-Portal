from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .db import Base, engine
from .routers import auth, courses, assignments, submissions, dashboard

settings=get_settings()
Path(settings.local_upload_dir).mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router); app.include_router(courses.router); app.include_router(assignments.router); app.include_router(submissions.router); app.include_router(dashboard.router)

@app.get("/health")
def health(): return {"status":"ok","environment":settings.environment,"storage_mode":settings.storage_mode}
