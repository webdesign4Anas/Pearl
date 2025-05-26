from app import models
# test for business_owners who are paid
def test_create_service_as_business_owner(client, test_business_owner,session):
    bo_user = session.query(models.Users).filter_by(email=test_business_owner["email"]).first()
    business_owner = session.query(models.BusinessOwners).filter_by(id=bo_user.id).first()
    business_owner.status = "PAID"
    session.commit()
    token=test_business_owner["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Bridal Makeup",
        "description": "Professional bridal makeup",
        "price": 500.0,
        "category": "makeup",
    }
    res = client.post("/services", json=payload, headers=headers)
    assert res.status_code == 201
    assert res.json()["name"] == payload["name"]

# test for business_owners who are NOTTT paid
def test_create_service_as_unpaid_business_owner(client, test_business_owner,session):
    token=test_business_owner["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "popo Makeup",
        "description": "Professional bridal makeup",
        "price": 500.0,
        "category": "makeup",
    }
    res = client.post("/services", json=payload, headers=headers)
    assert res.status_code == 403
