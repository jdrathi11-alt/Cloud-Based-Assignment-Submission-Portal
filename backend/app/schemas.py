from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="student", pattern="^(student|teacher)$")

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class CourseIn(BaseModel):
    course_name: str = Field(min_length=2, max_length=150)

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_name: str
    teacher_id: int

class AssignmentIn(BaseModel):
    course_id: int
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=2, max_length=5000)
    deadline: datetime
    max_marks: int = Field(gt=0, le=1000)
    allowed_file_types: str = "pdf,docx,zip"
    max_file_size_mb: int = Field(gt=0, le=50)

class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    title: str
    description: str
    deadline: datetime
    max_marks: int
    created_by: int
    allowed_file_types: str
    max_file_size_mb: int

class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    assignment_id: int
    student_id: int
    file_name: str
    file_url: str | None
    submitted_at: datetime
    submission_status: str
    marks: int | None
    feedback: str | None
    graded_at: datetime | None

class GradeIn(BaseModel):
    marks: int = Field(ge=0)
    feedback: str = Field(default="", max_length=5000)
