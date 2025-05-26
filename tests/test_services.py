from app import models
#test create service for the paid business_owner
def test_create_service_for_paid_business_owner(client,session,test_business_owner):
    business_owner_id=session.query(models.Users).filter(models.Users.email==test_business_owner["email"]).first().id
    business_owner_modified=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==business_owner_id).first()
    business_owner_modified.status="PAID"
    session.commit()
    token=test_business_owner["access_token"]
    header={"Authorization":f"Bearer {token}"}
    create_service=client.post("/services",json={"name":"makeup1","description":"amazingone","price":200,"category":"makeup"},headers=header)
    assert create_service.status_code==201
    assert create_service.json()["id"]==1


#test create service fpr unpaid business owners
def test_create_service_for_UNpaid_business_owner(client,session,test_business_owner):
    token=test_business_owner["access_token"]
    header={"Authorization":f"Bearer {token}"}
    create_service=client.post("/services",json={"name":"makeup1","description":"amazingone","price":200,"category":"makeup"},headers=header)
    assert create_service.status_code==403


#retrieve all services for the normal user
def test_retrieve_all_services_for_normal_user(client,test_user,session,test_business_owner):
    business_owner_id=session.query(models.Users).filter(models.Users.email==test_business_owner["email"]).first().id
    business_owner_modified=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==business_owner_id).first()
    business_owner_modified.status="PAID"
    session.commit()
    token=test_business_owner["access_token"]
    header={"Authorization":f"Bearer {token}"}
    create_service=client.post("/services",json={"name":"makeup1","description":"amazingone","price":800,"category":"makeup"},headers=header)
    assert create_service.status_code==201
    assert create_service.json()["id"]==1
    res = client.get("/services?category=makeup")
    assert res.status_code == 200
    services = res.json()
    assert all(service["category"] == "makeup" for service in services)
    assert isinstance(services,list)


#test get one service

def test_get_one_service(client,session,test_user,test_business_owner,paid_business_owner):
    
    services=[
         {"owner_id":1,"name":"wpop","description":"23asdkasdd","price":200,"quantity":20,"category":"makeup"},
         {"owner_id":1,"name":"wwpop","description":"23asdkasdd","price":2100,"quantity":40,"category":"makeup"},
         {"owner_id":1,"name":"wp34op","description":"23asdkasdd","price":2020,"quantity":10,"category":"makeup"}
    ]
    
    for service in services:
        res=client.post("/services",json=service,headers={"Authorization":f"Bearer {test_business_owner["access_token"]}"})
        assert res.status_code==201
        services=res.json()
    onepost=client.get("/services/1").json()
    assert onepost["name"]=="wpop"







