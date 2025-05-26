from fastapi import HTTPException,status,APIRouter,Depends
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas,oauth2,models
from typing import List
router=APIRouter(prefix="/users",tags=["Authentication"])


#review user-purchases
@router.get("/my-purchases", response_model=List[schemas.PurchaseOut])
def get_user_purchases(
    db: Session = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    return db.query(models.Purchase).filter_by(user_id=user.id).all()
