from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.config import settings
from app import models
from app.utils import hash
import pytest
from fastapi.testclient import TestClient
from app.database import get_db,Base
from app.main import app
database_name="pearl_test"
SQL_ALCHEMY_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{database_name}"

engine=create_engine(SQL_ALCHEMY_URL) # that is what connect the postgresql with sqlalchemy

TestingSessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)   # responsible for talking to the database 

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db=TestingSessionLocal()
    try:
            yield db                                                          # yield db: Passes the session to path operation functions.
    finally:
            db.close()    

@pytest.fixture()
def client (session):                            #(session) → Creates tables & yields a DB session.  (client) → Overrides get_db and provides TestClient 
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)
    

@pytest.fixture()
def test_user(client):
     payload={"email":"anasahmed2452@gmail.com","password":"22526618a"}
     response=client.post("/register/user",json=payload)
     new_user=response.json()
     new_user["password"]=payload["password"]
     new_user["email"]=payload["email"]
     assert "email" in new_user
     return new_user
     

@pytest.fixture()
def test_business_owner(client):
     payload={"email":"business_owner@gmail.com","password":"22526618a","business_type":"MAKEUP_ARTIST","business_name":"FirstBo","description":"the best one ever"}
     response=client.post("/register/business",json=payload)
     new_user=response.json()
     new_user["password"]=payload["password"]
     new_user["email"]=payload["email"]
     assert "email" in new_user
     return new_user
          



@pytest.fixture()
def admin_object_and_token(client,session):
     admin_payload={"email":"admin2245@gmail.com","password":"22526618a","role":"ADMIN"}
     admin=models.Users(
          email=admin_payload["email"],
          password_hash=hash(admin_payload["password"]),
          role=admin_payload["role"],
     )
     session.add(admin)
     session.commit()
     session.refresh(admin)
     response=client.post("/login",data={"username":admin_payload["email"],"password":admin_payload["password"]})
     token=response.json()["access_token"]
     assert response.status_code==201
     return{"admin":admin , "access_token":token}

@pytest.fixture()
def paid_business_owner(test_business_owner,session):
    business_owner_id=session.query(models.Users).filter(models.Users.email==test_business_owner["email"]).first().id
    business_owner_modified=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==business_owner_id).first()
    business_owner_modified.status="PAID"
    session.commit()
    return business_owner_modified


@pytest.fixture()
def services(paid_business_owner, client, test_business_owner):
    service_data = [
        {"owner_id": 1, "name": "wpop", "description": "23asdkasdd", "price": 200, "quantity": 20, "category": "makeup"},
        {"owner_id": 1, "name": "wwpop", "description": "23asdkasdd", "price": 2100, "quantity": 40, "category": "makeup"},
        {"owner_id": 1, "name": "wp34op", "description": "23asdkasdd", "price": 2020, "quantity": 10, "category": "makeup"}
    ]
    
    created_services = []
    headers = {"Authorization": f"Bearer {test_business_owner['access_token']}"}
    
    for service in service_data:
        res = client.post("/services", json=service, headers=headers)
        assert res.status_code == 201  # Verify successful creation
        created_services.append(res.json())
    
    return created_services  # Returns list of all created services













@pytest.fixture
def test_service(session, paid_business_owner):
    from app import models
    service = models.Services(
        name="Test Service",
        price=100.00,
        category="makeup",
        owner_id=paid_business_owner.id,
        quantity=10,
        description="asdsad"
    )
    session.add(service)
    session.commit()
    return service