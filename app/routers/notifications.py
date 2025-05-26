from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from app import oauth2,schemas,models

router=APIRouter(tags=["Notifications"])
#retrieve all notifications for specefic BO
@router.get("/notifications",status_code=status.HTTP_200_OK,response_model=list[schemas.NotificationsOut])
def get_notifications(db:session=Depends(get_db),owner:models.Users=Depends(oauth2.require_paid_business_owner)):
    return (db.query(models.Notification).filter(models.Notification.business_owner_id==owner.id).order_by(models.Notification.created_at.desc()).all())


#mark specefic notification as read
@router.put("/notifications/{notification_id}/mark-read",status_code=status.HTTP_200_OK)
def mark_as_read(notification_id:int,db:session=Depends(get_db),owner:models.Users=Depends(oauth2.require_paid_business_owner)):
    notification=db.query(models.Notification).filter(models.Notification.id==notification_id,models.Notification.business_owner_id==owner.id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="notification not found")
    notification.is_read=True
    db.commit()
    return {"status":"marked_as_read"}



  