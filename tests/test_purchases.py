from app import models
#test purchase booking for makeup-service
def test__booking_makeup_service(client,test_user,paid_business_owner,services):
    header={"Authorization":f"Bearer {test_user["access_token"]}"}
    payload={"service_id":services[0]["id"],"booking_date":services[0]["created_at"]}
    purchase=client.post("/purchase",json=payload,headers=header)
    assert purchase.status_code==201
    purchase_details=purchase.json()
    assert purchase_details["id"]==services[0]["id"]
    assert purchase_details["amount"]==services[0]["price"]


#test purchase booking for dress
def test_purchase_dress_service(client,test_user,paid_business_owner,session):
    dress=models.Services(
        owner_id=paid_business_owner.id,
        name="Best Dress",
        description="jewerly dress",
        price=1000,
        quantity=2,
        category="dress",
    )
    session.add(dress)
    session.commit()
    session.refresh(dress)
    header={"Authorization":f"Bearer {test_user["access_token"]}"}
    payload={"service_id":dress.id}
    purchase1=client.post("/purchase",json=payload,headers=header)
    assert purchase1.status_code==201
    assert purchase1.json()["amount"]==1000
    update=session.query(models.Services).get(dress.id)
    assert update.quantity==1
    purchase2=client.post("/purchase",json=payload,headers=header)
    assert purchase2.status_code==201
    purchase3=client.post("/purchase",json=payload,headers=header)
    assert purchase3.status_code==400
    assert purchase3.json()["detail"]=="Out OF Stock"
