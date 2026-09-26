from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..auth import require_role, get_current_user
from ..config import get_settings
from ..db import get_db
from ..models import Assignment, Submission, Course
from ..schemas import SubmissionOut, GradeIn
from ..services.storage import StorageService

router = APIRouter(prefix="/api", tags=["submissions"])
settings = get_settings()


def check_file(upload: UploadFile, assignment: Assignment, size: int):
    ext = Path(upload.filename or "").suffix.lower().lstrip(".")
    allowed = {x.strip().lower().lstrip(".") for x in assignment.allowed_file_types.split(",") if x.strip()}
    if ext not in allowed: raise HTTPException(400, f"File type .{ext} is not allowed")
    if size > assignment.max_file_size_mb * 1024 * 1024: raise HTTPException(413, "File exceeds assignment size limit")

@router.post("/assignments/{assignment_id}/submit", response_model=SubmissionOut)
async def submit_assignment(assignment_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), student=Depends(require_role("student"))):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    now = datetime.now(timezone.utc)
    existing = db.query(Submission).filter_by(assignment_id=assignment_id, student_id=student.id).first()
    if existing and existing.submission_status == "GRADED": raise HTTPException(409, "Graded submissions cannot be resubmitted")
    content = await file.read()
    check_file(file, a, len(content))
    if now > a.deadline and not settings.allow_late_submissions: raise HTTPException(400, "Deadline has passed")
    storage = StorageService()
    path, url = storage.upload(content, file.filename, assignment_id, student.id)
    status = "LATE" if now > a.deadline else "SUBMITTED"
    if existing:
        existing.file_name=file.filename; existing.storage_path=path; existing.file_url=url; existing.submitted_at=now; existing.submission_status=status; existing.marks=None; existing.feedback=None; existing.graded_at=None
        db.commit(); db.refresh(existing); return existing
    sub = Submission(assignment_id=assignment_id, student_id=student.id, file_name=file.filename, storage_path=path, file_url=url, submitted_at=now, submission_status=status)
    db.add(sub); db.commit(); db.refresh(sub); return sub

@router.get("/submissions/me", response_model=list[SubmissionOut])
def my_submissions(db: Session = Depends(get_db), student=Depends(require_role("student"))):
    return db.query(Submission).filter(Submission.student_id == student.id).order_by(Submission.submitted_at.desc()).all()

@router.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionOut])
def assignment_submissions(assignment_id: int, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    a=db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404,"Assignment not found")
    if a.created_by != teacher.id: raise HTTPException(403,"Not your assignment")
    return db.query(Submission).filter(Submission.assignment_id==assignment_id).all()

@router.get("/submissions/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    s=db.get(Submission, submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role=="student" and s.student_id!=user.id: raise HTTPException(403,"Private submission")
    if user.role=="teacher":
        a=db.get(Assignment,s.assignment_id)
        if not a or a.created_by!=user.id: raise HTTPException(403,"Not permitted")
    return s

@router.post("/submissions/{submission_id}/grade", response_model=SubmissionOut)
def grade_submission(submission_id:int, data:GradeIn, db:Session=Depends(get_db), teacher=Depends(require_role("teacher"))):
    s=db.get(Submission, submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    a=db.get(Assignment,s.assignment_id)
    if not a or a.created_by!=teacher.id: raise HTTPException(403,"Not permitted")
    if data.marks>a.max_marks: raise HTTPException(400,"Marks cannot exceed maximum marks")
    s.marks=data.marks; s.feedback=data.feedback; s.graded_at=datetime.now(timezone.utc); s.submission_status="GRADED"
    db.commit(); db.refresh(s); return s

@router.get("/submissions/{submission_id}/feedback", response_model=SubmissionOut)
def feedback(submission_id:int, db:Session=Depends(get_db), student=Depends(require_role("student"))):
    s=db.get(Submission,submission_id)
    if not s or s.student_id!=student.id: raise HTTPException(404,"Submission not found")
    return s

@router.get("/submissions/{submission_id}/download")
def download_submission(submission_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    s=db.get(Submission,submission_id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role=="student" and s.student_id!=user.id: raise HTTPException(403,"Private submission")
    if user.role=="teacher":
        a=db.get(Assignment,s.assignment_id)
        if not a or a.created_by!=user.id: raise HTTPException(403,"Not permitted")
    try: content=StorageService().download(s.storage_path)
    except FileNotFoundError: raise HTTPException(404,"Stored file not found")
    return Response(content=content, media_type="application/octet-stream", headers={"Content-Disposition": f'attachment; filename="{s.file_name}"'})
