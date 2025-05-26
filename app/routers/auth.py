from fastapi import HTTPException,status,APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,utils,oauth2
router=APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(user_credentials.username==models.Users.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credentials not matched")
    if not utils.verify(user_credentials.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credentials not matched")
    access_token=oauth2.create_access_token(data={"user_id":user.id,"role":user.role})
    return{"access_token":access_token, "token_type":"bearer","role":user.role,"id":user.id}



