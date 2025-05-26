from fastapi import FastAPI,Depends,HTTPException,status,APIRouter,Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from  app.database import get_db
from app import schemas,models,oauth2
from typing import Optional,List




router=APIRouter(prefix="/admin",tags=["Admin"])

#retrieve all users for admin
@router.get("/users",status_code=status.HTTP_200_OK,response_model=list[schemas.UserOut])
def retireve_all_users(
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    role:Optional[str]=Query(None),
    is_active:Optional[bool]=Query(None),
    skip:int=0 ,
    limit:int=20,
    ):
    query=db.query(models.Users)
    if role:
        query=query.filter(models.Users.role==role.upper())
    if is_active is not None:
        query=query.filter(models.Users.is_active==is_active)

    return query.offset(skip).limit(limit).all()

#retrieve all payments for admin
@router.get("/payments",status_code=status.HTTP_200_OK,response_model=List[schemas.PaymentOut])
def get_all_payments(
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    payment_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
    query=db.query(models.Payments)
    if status:
        query=query.filter(models.Payments.status==status.upper())

    if payment_type:
        query=query.filter(models.Payments.payment_type==payment_type.upper())

    payment=query.offset(skip).limit(limit).all()      

    return  payment    

#retrieve all business_owner
@router.get("/business_owners",response_model=schemas.BusinessOwnersOut,status_code=status.HTTP_200_OK)
def get_all_business_owners(
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
    status:Optional[str]=Query(None),
    business_type:Optional[str]=Query(None),
    skip:int=0 ,
    limit:int=20,
):
    query=db.query(models.BusinessOwners)
    
    if status:
        query=query.filter(models.BusinessOwners.status==status.upper())

    if business_type:
        query=query.filter(models.BusinessOwners.business_type==business_type.upper())

    return query.offset(skip).limit(limit).all()

#Approve business_owner
@router.put("/business_owners/{owner_id}/approve",status_code=status.HTTP_200_OK)
def accept_user(
    owner_id:int,
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    owner=db.query(models.BusinessOwners).filter(models.BusinessOwners.id==owner_id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Owner Not Found")
    owner.status="PAID"
    db.commit()
    return {"detail": "Approved and status updated to PAID"}

#Reject Business_Owner
@router.put("/business_owners/{owner_id}/reject",status_code=status.HTTP_200_OK)
def accept_user(
    owner_id:int,
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    owner=db.query(models.BusinessOwners).filter(models.BusinessOwners.id==owner_id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Owner Not Found")
    owner.status="Rejected"
    db.commit()
    return {"detail": "Rejected Successfully"}  

#Blocking User
@router.put("/users/{user_id}/block",status_code=status.HTTP_200_OK)
def block_user(
    user_id:int,
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=False
    db.commit()
    return{f"User({user.email}) is Blocked Successfully"}

#Un-Blocking User
@router.put("/users/{user_id}/unblock",status_code=status.HTTP_200_OK)
def block_user(
    user_id:int,
    db:Session=Depends(get_db),
    admin:models.Users=Depends(oauth2.require_admin_user),
):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    user.is_active=True
    db.commit()
    return{f"User({user.email}) is Un-Blocked Successfully"}


#reviewing all revenues
@router.get("/revenues",status_code=status.HTTP_200_OK)
def get_all_revenues(db:Session=Depends(get_db),admin:models.Users=Depends(oauth2.require_admin_user)):
    
    total_sales=db.query(func.sum(models.Purchase.amount)).scalar() or 0.0
    total_commision=db.query(func.sum(models.Purchase.commision)).scalar or 0.0
    return{" total_sum ":{total_sales}," total_commision ":total_commision}
