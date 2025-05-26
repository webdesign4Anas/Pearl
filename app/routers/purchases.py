from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas,oauth2,models
from app.websockets import manager
from fastapi_mail import FastMail,MessageSchema,MessageType
from app.config import conf
router=APIRouter(tags=["Purchases"])

#purchase details and registeration of purchases

@router.post("/purchase",response_model=schemas.PurchaseOut,status_code=status.HTTP_201_CREATED)
async def purchase_service(purchase_data:schemas.PurchaseCreate,db:Session=Depends(get_db),user:models.Users=Depends(oauth2.get_authenticated_user)):
    service=db.query(models.Services).filter(models.Services.id==purchase_data.service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Service Not Found")
    category=service.category
    # check if its dress and has stock
    if category=="dress":
        if service.quantity<=0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Out OF Stock")
        service.quantity-=1
#check if its makeup or photographer
    if category in ["makeup","photographer"]:
        if not purchase_data.booking_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Booking Date Required")
        existed=db.query(models.ServiceBooking).filter(models.ServiceBooking.id==purchase_data.service_id,models.ServiceBooking.booking_date==purchase_data.booking_date).first()
        if existed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Service ALREADY BOOKED IN THAT TIME")
        added_service=models.ServiceBooking(
            service_id=service.id,
            user_id=user.id,
            booking_date=purchase_data.booking_date
        )
        db.add(added_service)
    #calculation commission amounts
    commision_rate=0.10
    commision=service.price*commision_rate
    purchase= models.Purchase(
        service_id=service.id,
        user_id=user.id,
        amount=service.price,
        commision=commision,
        booking_date=purchase_data.booking_date,
    )
    business_owner_id=service.owner_id
    notification=models.Notification(
        business_owner_id=business_owner_id,
        message=f"new purchase for service {service.name} by user {user.email}"
    )
    db.add(purchase)
    db.add(notification)
    db.commit()
    db.refresh(purchase)
    business_owner=db.query(models.Users).filter(models.Users.id==business_owner_id).first()
    message=MessageSchema(
        subject="New Purchase Required",
        recipients=[business_owner.email],
        body=f"Hello {business_owner.email} your got a purchase from service {service.name}",
        subtype=MessageType.plain,
    )

    fm=FastMail(conf)
    await fm.send_message(message)
    await manager.send_personal_message("you got new purchase",business_owner_id)
    return purchase
        