from app import models

def test_user_registration(client,session):
    payload={"email":"anasahmed71023@gmial.com" ,"password":"22526618a"}
    response=client.post("/register/user",json=payload)
    assert response.status_code==201
    user_in_db=session.query(models.Users).filter_by(email=payload["email"]).first()
    assert user_in_db is not None
    assert user_in_db.email==payload["email"]
    assert response.json()["token_type"] is not None




def test_business_owner_registration(client,session):
    payload={"email":"firstbusinessOwner@gmail.com","password":"22526618a","business_type":"MAKEUP_ARTIST","business_name":"FirstBo","description":"the best one ever"}
    response=client.post("/register/business",json=payload)
    assert response.status_code==201
    as_user=session.query(models.Users).filter(models.Users.email==payload["email"]).first()
    assert as_user is not None
    assert as_user.role=="BUSINESS_OWNER"
    as_business_owner=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==as_user.id).first()
    assert as_business_owner is not None
    assert as_business_owner.business_name==payload["business_name"]


def test_duplicate_email_business_owner(client):
    payload = {
        "email": "firstbusinessOwner@gmail.com",
        "password": "securepass",
        "business_type": "PHOTOGRAPHER",
        "business_name": "PhotoPro",
        "description": "Quality shots"
    }
    # First registration
    client.post("/register/business", json=payload)
    # Second with same email
    response = client.post("/register/business", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email Already Exists"

def test_invalid_business_type(client):
    payload=payload = {
        "email": "firstbusinessOwner@gmail.com",
        "password": "securepass",
        "business_type": "notvalidbitch",
        "business_name": "PhotoPro",
        "description": "Quality shots"
    }
    response=client.post("/register/business",json=payload)
    assert response.status_code==422

def test_missing_fields(client):
    payload={ "email": "firstbusinessOwner@gmail.com",
        "password": "securepass",}
    response=client.post("/register/business",json=payload)
    assert response.status_code==422
