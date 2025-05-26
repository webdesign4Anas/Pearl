from fastapi import Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import Session,joinedload
from app import schemas,models,oauth2
from app.database import get_db
router=APIRouter(tags=["WishList"])
from typing import List
#Adding Item to  User's Wishlist
@router.post("/wishlist",response_model=schemas.WishListItemOut,status_code=status.HTTP_201_CREATED)
def create_wishlist(wishlist_item:schemas.WishListItem,db:Session=Depends(get_db),user:models.Users=Depends(oauth2.get_authenticated_user)):
    is_existed=db.query(models.Wishlists).filter(models.Wishlists.service_id==wishlist_item.service_id,models.Wishlists.user_id==user.id).first()
    if is_existed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item Already Exists In Your WishList")
    item=models.Wishlists(
        user_id=user.id,
        service_id=wishlist_item.service_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

#Viewing User's Specefic Wishlist
@router.get("/wishlist", response_model=List[schemas.WishListItemOut])
def get_wishlist(
    db: Session = Depends(get_db),
    user: models.Users = Depends(oauth2.get_authenticated_user)
):
    wishlist = (
        db.query(models.Wishlists)
        .options(joinedload(models.Wishlists.service).joinedload(models.Services.images))
        .filter(models.Wishlists.user_id == user.id)
        .all()
    )

    # Attach preview image (first one) to each service
    for item in wishlist:
        service = item.service
        if service.images:
            service.image_preview_url = service.images[0].image_url
        else:
            service.image_preview_url = None

    return wishlist


#Deleteing Item From User's WishList
@router.delete("/wishlist/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist_item(item_id:int,user:models.Users=Depends(oauth2.get_authenticated_user),db:Session=Depends(get_db)):
    query=db.query(models.Wishlists).filter(models.Wishlists.user_id==user.id,models.Wishlists.service_id==item_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Not Found")
    db.delete(query)
    db.commit()
    return{"message":"deleted succesfully"}










#@router.get("/wishlist",response_model=[schemas.ServiceSummaryOut],status_code=status.HTTP_200_OK)
#def view_wishlist(user:models.Users=Depends(oauth2.get_authenticated_user),db:Session=Depends(get_db)):
 #   query=db.query(models.Wishlists).filter(models.Wishlists.user_id==user.id).all()
  #  return query