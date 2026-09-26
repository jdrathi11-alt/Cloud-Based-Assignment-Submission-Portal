from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import require_role, get_current_user
from ..db import get_db
from ..models import Course
from ..schemas import CourseIn, CourseOut

router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Course)
    return q.filter(Course.teacher_id == user.id).all() if user.role == "teacher" else q.all()

@router.post("", response_model=CourseOut, status_code=201)
def create_course(data: CourseIn, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    c = Course(course_name=data.course_name, teacher_id=teacher.id); db.add(c); db.commit(); db.refresh(c); return c
