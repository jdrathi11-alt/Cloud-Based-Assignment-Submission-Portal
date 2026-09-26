from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, TokenOut
from ..auth import hash_password, verify_password, create_token
from ..config import get_settings

router=APIRouter(prefix="/api",tags=["auth"]); settings=get_settings()

def supabase_client():
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_anon_key)

@router.post("/register",response_model=TokenOut,status_code=201)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if data.role=="teacher" and not settings.allow_teacher_signup: raise HTTPException(403,"Teacher self-registration is disabled")
    if db.query(User).filter(User.email==data.email.lower()).first(): raise HTTPException(409,"Email already registered")
    if settings.auth_mode=="supabase":
        try:
            result=supabase_client().auth.sign_up({"email":data.email.lower(),"password":data.password,"options":{"data":{"name":data.name,"role":data.role}}})
            if not result.user: raise HTTPException(400,"Supabase did not create the user")
            user=User(name=data.name,email=data.email.lower(),auth_uid=result.user.id,role=data.role)
            db.add(user);db.commit();db.refresh(user)
            if not result.session: raise HTTPException(400,"Account created. Disable email confirmation in Supabase Auth for this classroom demo, then log in.")
            return {"access_token":result.session.access_token,"user":user}
        except HTTPException: raise
        except Exception as e: raise HTTPException(400,f"Cloud authentication error: {e}")
    user=User(name=data.name,email=data.email.lower(),password_hash=hash_password(data.password),role=data.role)
    db.add(user);db.commit();db.refresh(user);return {"access_token":create_token(user),"user":user}

@router.post("/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    if settings.auth_mode=="supabase":
        try:
            result=supabase_client().auth.sign_in_with_password({"email":data.email.lower(),"password":data.password})
            auth_user=result.user
            user=db.query(User).filter(User.auth_uid==auth_user.id).first()
            if not user: raise HTTPException(401,"User profile not found")
            return {"access_token":result.session.access_token,"user":user}
        except HTTPException: raise
        except Exception: raise HTTPException(401,"Invalid email or password")
    user=db.query(User).filter(User.email==data.email.lower()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_token(user),"user":user}

@router.post("/logout")
def logout(): return {"message":"Logout handled by client token removal; cloud sessions expire/refresh through the auth provider."}
