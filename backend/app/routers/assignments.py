from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import require_role, get_current_user
from ..db import get_db
from ..models import Assignment, Course
from ..schemas import AssignmentIn, AssignmentOut

router = APIRouter(prefix="/api/assignments", tags=["assignments"])

@router.get("", response_model=list[AssignmentOut])
def get_assignments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Assignment)
    return q.filter(Assignment.created_by == user.id).all() if user.role == "teacher" else q.all()

@router.get("/{assignment_id}", response_model=AssignmentOut)
def get_assignment(assignment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    return a

@router.post("", response_model=AssignmentOut, status_code=201)
def create_assignment(data: AssignmentIn, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    course = db.get(Course, data.course_id)
    if not course or course.teacher_id != teacher.id: raise HTTPException(403, "Course is not yours")
    a = Assignment(**data.model_dump(), created_by=teacher.id); db.add(a); db.commit(); db.refresh(a); return a

@router.put("/{assignment_id}", response_model=AssignmentOut)
def update_assignment(assignment_id: int, data: AssignmentIn, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    if a.created_by != teacher.id: raise HTTPException(403, "Not your assignment")
    for k,v in data.model_dump().items(): setattr(a,k,v)
    db.commit(); db.refresh(a); return a

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    if a.created_by != teacher.id: raise HTTPException(403, "Not your assignment")
    db.delete(a); db.commit(); return {"message":"Assignment deleted"}
