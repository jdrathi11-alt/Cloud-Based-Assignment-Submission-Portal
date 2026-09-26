from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .config import get_settings
from .db import get_db
from .models import User

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
bearer=HTTPBearer(auto_error=False); settings=get_settings()

def hash_password(password): return pwd.hash(password)
def verify_password(password,hashed): return pwd.verify(password,hashed)
def create_token(user):
    payload={"sub":str(user.id),"role":user.role,"exp":datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload,settings.secret_key,algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials=Depends(bearer), db: Session=Depends(get_db)):
    if not credentials: raise HTTPException(401,"Authentication required")
    token=credentials.credentials
    if settings.auth_mode=="supabase":
        try:
            from supabase import create_client
            client=create_client(settings.supabase_url,settings.supabase_anon_key)
            result=client.auth.get_user(token)
            auth_user=result.user
            user=db.query(User).filter(User.auth_uid==auth_user.id).first()
            if not user: raise HTTPException(401,"Profile not found")
            return user
        except HTTPException: raise
        except Exception: raise HTTPException(401,"Invalid or expired authentication token")
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=["HS256"]); user_id=int(payload["sub"])
    except (JWTError,KeyError,ValueError): raise HTTPException(401,"Invalid or expired token")
    user=db.get(User,user_id)
    if not user: raise HTTPException(401,"User not found")
    return user

def require_role(*roles):
    def dependency(user=Depends(get_current_user)):
        if user.role not in roles: raise HTTPException(403,"Insufficient permissions")
        return user
    return dependency
