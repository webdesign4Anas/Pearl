from pydantic import BaseModel,EmailStr,HttpUrl
from typing import Optional,Literal,List
from datetime import datetime


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    id: Optional[int]


class Token(BaseModel):
    access_token:str
    token_type:str

class UserCreate(BaseModel):
    email:EmailStr
    password:str
   

class BusinessOwnerCreate(UserCreate):
    business_type: Literal['MAKEUP_ARTIST', 'PHOTOGRAPHER', 'DRESS_RETAILER']
    business_name:str
    description:Optional[str]=None


class ServiceImageOut(BaseModel):
    id: int
    description: str
    image_url: str
    uploaded_at: str

    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name:str
    description:str
    price:float
    category:Literal["dress","makeup","photographer"]

class ServiceOut(ServiceCreate):
    id: int
    owner_id: int
    created_at: datetime
    images: List[ServiceImageOut] = []

    class Config:
        from_attributes = True    

class CreateServiceImage(BaseModel):
    image_url:str
    description:str
    service_id:int

class ServiceSummaryOut(BaseModel):
    id:int
    name:str
    price:float
    image_preview_url:Optional[str]=None
    class Config:
        from_attributes=True

class WishListItem(BaseModel):
    service_id:int

class WishListItemOut(BaseModel):
    service_id:int
    service:ServiceSummaryOut
    class Config:
        from_attributes=True

class PaymentRequest(BaseModel):
    card_nubmer:str
    amount:float


class UserOut(BaseModel):
    id:int
    email:str
    role:str
    is_active:bool
    created_at:datetime
    class Config:
        from_attributes=True

class PaymentOut(BaseModel):
    id:int
    user_id:int
    amount:float
    status:str
    payment_type:str
    created_at:datetime
    class Config:
        from_attributes=True

class BusinessOwnersOut(BaseModel):
    id:int
    business_type:str
    status:str
    business_name:str
    class Config:
        from_attributes=True

class PurchaseCreate(BaseModel):
    service_id:int
    booking_date:Optional[datetime]=None

class PurchaseOut(BaseModel):
    id:int
    user_id:int
    service_id:int
    commision:float
    amount:float
    booking_date:Optional[datetime]
    created_at:datetime
    class Config:
        from_attributes=True


class NotificationsOut(BaseModel):
    id:int
    message:str
    is_read:bool
    created_at:datetime
    class Config:
        from_attributes=True
