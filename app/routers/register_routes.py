from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash,verify
from app import schemas,models,oauth2

router=APIRouter(tags=['Authentication'])

# Registeration for Users
@router.post("/register/user",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
def register_user(data:schemas.UserCreate,db:Session=Depends(get_db)):
    if db.query(models.Users).filter(models.Users.email==data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
    
    user= models.Users(
        email=data.email,
        password_hash=hash(data.password),
        role="USER",
        )
    db.add(user)
    db.commit()
    db.refresh(user)
     
    access_token=oauth2.create_access_token(data={"user_id":str(user.id)})
    return{"access_token":access_token,"token_type":"Bearer","role":user.role,"id":user.id}

#Register for Business_Owners
@router.post("/register/business",status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
def register_business(data:schemas.BusinessOwnerCreate,db:Session=Depends(get_db)):
    if db.query(models.Users).filter(models.Users.email==data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
    
    user= models.Users(
        email=data.email,
        password_hash=hash(data.password),
        role="BUSINESS_OWNER",
        )
    db.add(user)
    db.commit()
    db.refresh(user)
     
    business=models.BusinessOwners(
        id=user.id,
        business_type=data.business_type.upper(),
        business_name=data.business_name,
        description=data.description,
        status="PENDING"
    )

    db.add(business)
    db.commit()
    db.refresh(business)

    access_token=oauth2.create_access_token(data={"user_id":str(user.id)})
    return{"access_token":access_token,"token_type":"Bearer","status": "PENDING_APPROVAL","role":user.role,"id":user.id}
    
    
    




