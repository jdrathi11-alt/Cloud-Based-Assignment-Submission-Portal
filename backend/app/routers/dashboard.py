from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..db import get_db
from ..models import Assignment, Submission, User

router=APIRouter(prefix="/api/dashboard",tags=["dashboard"])

@router.get("")
def dashboard(db:Session=Depends(get_db), user=Depends(get_current_user)):
    if user.role=="student":
        assignments=db.query(Assignment).count(); subs=db.query(Submission).filter_by(student_id=user.id).all()
        return {"role":"student","total_assignments":assignments,"pending_assignments":assignments-len(subs),"submitted_assignments":sum(s.submission_status=="SUBMITTED" for s in subs),"late_assignments":sum(s.submission_status=="LATE" for s in subs),"graded_assignments":sum(s.submission_status=="GRADED" for s in subs),"recent_feedback":[{"submission_id":s.id,"feedback":s.feedback,"marks":s.marks} for s in subs if s.feedback][-5:]}
    assignments=db.query(Assignment).filter_by(created_by=user.id).all(); ids=[a.id for a in assignments]
    subs=db.query(Submission).filter(Submission.assignment_id.in_(ids)).all() if ids else []
    return {"role":"teacher","total_assignments":len(assignments),"total_students":db.query(User).filter_by(role="student").count(),"total_submissions":len(subs),"pending_reviews":sum(s.submission_status in ("SUBMITTED","LATE") for s in subs),"late_submissions":sum(s.submission_status=="LATE" for s in subs),"graded_submissions":sum(s.submission_status=="GRADED" for s in subs)}
