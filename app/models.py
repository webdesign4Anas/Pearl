from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,CheckConstraint,ForeignKey,Float,UniqueConstraint,Date
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,unique=True,nullable=False,index=True)
    password_hash=Column(String,nullable=False)
    role=Column(String,nullable=False)
    is_active=Column(Boolean,server_default="True")
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    __table_args__=(
        CheckConstraint(
        "role IN ('USER','ADMIN','BUSINESS_OWNER')",
        name="check_user_role"
    ),
    )

class BusinessOwners(Base):
    __tablename__="business_owners"
    id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),primary_key=True)
    business_type=Column(String,nullable=False,index=True)
    business_name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    approved=Column(Boolean,server_default="False")
    status=Column(String,nullable=False,index=True)
    payment_id=Column(Integer,ForeignKey("payments.id",ondelete="cascade"))
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 
    __table_args__=(
        CheckConstraint("business_type IN ('MAKEUP_ARTIST', 'PHOTOGRAPHER', 'DRESS_RETAILER')"),
        CheckConstraint(" status IN ('PENDING','PAID','Rejected') "),
        UniqueConstraint('business_name')
    )

class Services(Base):
    __tablename__="services"
    id= Column(Integer,primary_key=True)
    owner_id=Column(Integer,ForeignKey("business_owners.id",ondelete="cascade"),index=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    quantity=Column(Integer,server_default="0") #only used for dresses
    category=Column(String,nullable=False,index=True)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 
    images=relationship("ServiceImage",back_populates="service",cascade="all,delete")  #back_populates the variable name not the table or class
    __table_args__=(
        CheckConstraint("category IN ('makeup','photographer','dress')"),
    )

class ServiceImage(Base):
    __tablename__="service_image"
    id= Column(Integer,primary_key=True)
    description=Column(String,nullable=False)
    service_id=Column(Integer,ForeignKey("services.id",ondelete="cascade")) 
    image_url=Column(String,nullable=False)
    uploaded_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 
    service=relationship("Services",back_populates="images") #back_populates the variable name not the table or class

class Payments (Base):
    __tablename__="payments"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"))
    amount=Column(Float,nullable=False)
    status=Column(String,nullable=False,index=True)
    payment_type=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 
    __table_args__=(
        CheckConstraint("status IN ('SUCCESS', 'PENDING', 'FAILED')"),      #ensure that the status and payment_type field has only these three values
        CheckConstraint(" payment_type IN ('SIGNUP','PURCHASE') "),
    )


class Wishlists(Base):
    __tablename__="wishlists"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),index=True)
    service_id=Column(Integer,ForeignKey("services.id",ondelete="cascade"),index=True)
    added_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 
    service=relationship("Services")
    __table_args__=(
        UniqueConstraint('user_id','service_id',name="uquix_user_service"),
    )
    

class AdminLogs(Base):
    __tablename__="admin_logs"
    id=Column(Integer,primary_key=True)
    action_type=Column(String,nullable=False)
    performed_by=Column(Integer,ForeignKey("users.id"),index=True)
    target_user=Column(Integer,ForeignKey("users.id"))
    description=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()")) 


class Purchase(Base):
    __tablename__="purchases"
    id=Column(Integer,primary_key=True)
    service_id=Column(Integer,ForeignKey("services.id",ondelete="CASCADE"))
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    amount=Column(Float,nullable=False)
    commision=Column(Float,nullable=False)
    booking_date=Column(Date,nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    user=relationship("Users")
    service=relationship("Services")

class ServiceBooking(Base):
    __tablename__="service_booking"
    id=Column(Integer,primary_key=True)
    service_id=Column(Integer,ForeignKey("services.id" , ondelete= "CASCADE"),index=True)
    user_id=Column(Integer,ForeignKey("users.id" , ondelete= "CASCADE"))
    booking_date=Column(Date,nullable=False,index=True)
    __table_args__=(
        UniqueConstraint("booking_date","service_id",name="service_book_unique"),
    )
    user=relationship("Users")
    service=relationship("Services")

class Notification(Base):
    __tablename__="notifications"
    id=Column(Integer,primary_key=True)
    business_owner_id=Column(Integer,ForeignKey("business_owners.id",ondelete="CASCADE"))
    message=Column(String,nullable=False)
    is_read=Column(Boolean,default=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    business_owner=relationship("BusinessOwners")
   
                      







    


    





