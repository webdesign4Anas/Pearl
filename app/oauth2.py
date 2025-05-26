from jose import jwt , JWTError
from app.config import settings
from datetime import datetime,timedelta
from app import models
from app.database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import schemas
from fastapi.security import OAuth2PasswordBearer
SECRET_KEY=f"{settings.secret_key}"
ALGORITHM=f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES=F"{settings.access_token_expire_minutes}"
oauth_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int= payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_authenticated_user(token:str=Depends(oauth_scheme),db: Session=Depends(get_db)):

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could'nt validate credentials",headers={"www-authenticate":"bearer"})
    user_token=verify_access_token(token,credentials_exception)
    user=db.query(models.Users).filter(models.Users.id==user_token.id).first()
    return user

def require_admin_user(user=Depends(get_authenticated_user)):
    if user.role !="ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admins Only")
    return user

def require_business_owner(user=Depends(get_authenticated_user)):
    if user.role !="BUSINESS_OWNER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="BUSINESS_OWNERS Only")
    return user

def require_paid_business_owner(user=Depends(get_authenticated_user),db:Session=Depends(get_db)):
    if user.role !="BUSINESS_OWNER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="BUSINESS_OWNERS ONLY")
    business=db.query(models.BusinessOwners).filter(models.BusinessOwners.id==user.id).first()
    if business.status !="PAID":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Payment Required")
    return user