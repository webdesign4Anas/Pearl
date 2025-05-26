from app import models,utils
#accepting the business_owner_after_payment
def test_admin_accept_business_payment(client,session,test_business_owner):
    admin_payload={"email":"admin1","password":"22526618a","role":"ADMIN"}
    # register admin to the database
    admin=models.Users(
        email= admin_payload["email"],
        password_hash=utils.hash(admin_payload["password"]),
        role=admin_payload["role"],
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    # login the admin 
    response=client.post("/login",data={"username":admin_payload["email"],"password":admin_payload["password"]})
    assert response.status_code==201
    token=response.json()["access_token"]
    #get the business_owner id
    business_owner=session.query(models.Users).filter(models.Users.email==test_business_owner["email"]).first()
    business_owner_id:int=business_owner.id 
    #approving that businessowner and make the status to paid
    response_paid=client.put(f"/admin/business_owners/{business_owner_id}/approve",headers={"Authorization":f"Bearer {token}" })
    business_owner_after_modifying=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==business_owner_id).first()
    assert business_owner_after_modifying.status=="PAID"
    assert response_paid.status_code==200

#Rejecting the business_owner_Bad_payment
def test_admin_Reject_business_payment(client,session,test_business_owner):
    admin_payload={"email":"admin1","password":"22526618a","role":"ADMIN"}
    # register admin to the database
    admin=models.Users(
        email= admin_payload["email"],
        password_hash=utils.hash(admin_payload["password"]),
        role=admin_payload["role"],
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    # login the admin 
    response=client.post("/login",data={"username":admin_payload["email"],"password":admin_payload["password"]})
    assert response.status_code==201
    token=response.json()["access_token"]
    #get the business_owner id
    business_owner=session.query(models.Users).filter(models.Users.email==test_business_owner["email"]).first()
    business_owner_id:int=business_owner.id 
    #approving that businessowner and make the status to paid
    response_paid=client.put(f"/admin/business_owners/{business_owner_id}/reject",headers={"Authorization":f"Bearer {token}" })
    business_owner_after_modifying=session.query(models.BusinessOwners).filter(models.BusinessOwners.id==business_owner_id).first()
    assert business_owner_after_modifying.status=="Rejected"
    assert response_paid.status_code==200

# Blocking User
def test_block_user(client,session,test_user):
    #siging_up_admin
    admin_payload={"email":"admin22@gmail.com","password":"22526618a"}
    admin=models.Users(
        email=admin_payload["email"],
        password_hash=utils.hash(admin_payload["password"]),
        role="ADMIN",
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    #logging as admin
    login_response=client.post("/login", data={"username":admin_payload["email"],"password":admin_payload["password"]})
    assert login_response.status_code==201
    token=login_response.json()["access_token"]
    #blocking user
    user=session.query(models.Users).filter(models.Users.email==test_user["email"]).first()
    assert user is not None
    user_id=user.id
    #blocking user
    response=client.put(f"/admin/users/{user_id}/block",headers={"Authorization":f"Bearer {token}" })
    assert response.status_code==200
    user=session.query(models.Users).filter(models.Users.email==test_user["email"]).first()
    assert user.is_active==False

#unblock user
def test_Unblock_user(client,session,test_user):
    #siging_up_admin
    admin_payload={"email":"admin22@gmail.com","password":"22526618a"}
    admin=models.Users(
        email=admin_payload["email"],
        password_hash=utils.hash(admin_payload["password"]),
        role="ADMIN",
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    #logging as admin
    login_response=client.post("/login", data={"username":admin_payload["email"],"password":admin_payload["password"]})
    assert login_response.status_code==201
    token=login_response.json()["access_token"]
    #blocking user
    user=session.query(models.Users).filter(models.Users.email==test_user["email"]).first()
    assert user is not None
    user_id=user.id
    #blocking user
    response=client.put(f"/admin/users/{user_id}/unblock",headers={"Authorization":f"Bearer {token}" })
    assert response.status_code==200
    user=session.query(models.Users).filter(models.Users.email==test_user["email"]).first()
    assert user.is_active==True



#retrieve all users
def test_retrieve_all_users(client, session):
    # 1. Create admin user
    admin_payload = {
        "email": "admin_test@example.com", 
        "password": "adminpass123",
        "role": "ADMIN"
    }
    admin = models.Users(
        email=admin_payload["email"],
        password_hash=utils.hash(admin_payload["password"]),
        role="ADMIN",
        is_active=True
    )
    session.add(admin)
    session.commit()

    # 2. Create test users with different roles/statuses
    test_users = [
        {"email": "user1@test.com", "role": "USER", "is_active": True},
        {"email": "user2@test.com", "role": "BUSINESS_OWNER", "is_active": True},
        {"email": "user3@test.com", "role": "USER", "is_active": False},
    ]
    
    for user_data in test_users:
        user = models.Users(
            email=user_data["email"],
            password_hash=utils.hash("testpass123"),
            role=user_data["role"],
            is_active=user_data["is_active"]
        )
        session.add(user)
    session.commit()

    # 3. Login as admin
    login_response = client.post(
        "/login",
        data={"username": admin_payload["email"], "password": admin_payload["password"]}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Test different query combinations
    test_cases = [
        # (query_params, expected_count)
        ({}, 4),  # All users (admin + 3 test users)
        ({"role": "user"}, 2),
        ({"role": "business_owner"}, 1),
        ({"is_active": True}, 3),
        ({"is_active": False}, 1),
        ({"role": "user", "is_active": True}, 1),
        ({"skip": 1, "limit": 2}, 2),  # Pagination test
    ]

    for params, expected_count in test_cases:
        response = client.get(
            "/admin/users",
            params=params,
            headers=headers
        )
        assert response.status_code == 200
        assert len(response.json()) == expected_count


#not admin access that
def test_not_authorize_user_to_get_all_users(client,session,test_user):
     # 5. Test unauthorized access
    user_login = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    user_token = user_login.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    unauth_response = client.get(
        "/admin/users",
        headers=user_headers
    )
    assert unauth_response.status_code == 403  # Forbidden

#retrieve all payments for admin
def test_retrieve_all_payments_made_by_business_owners_For_the_admin(admin_object_and_token,client):
    bo1=client.post("/register/business",json={"email":"bo1@gmail.com","password":"123","business_name":"bestone","business_type":"PHOTOGRAPHER","description":"qwe"}).json()
    bo2=client.post("/register/business",json={"email":"bo2@gmail.com","password":"123","business_name":"best4one","business_type":"PHOTOGRAPHER","description":"qwe"}).json()
    token1=bo1["access_token"]
    token2=bo2["access_token"]
    response1=client.post("/business/payment",json={"card_nubmer":"1234567891234564","amount":200},headers={"Authorization":f"Bearer {token1}"})
    assert response1.status_code==202
    assert response1.json()["Status"]=="SUCCESS"
    response2=client.post("/business/payment",json={"card_nubmer":"121234564","amount":2450},headers={"Authorization":f"Bearer {token2}"})
    assert response2.status_code==400
    assert response2.json()["detail"]=="Payment Failed"
    payments=client.get("/admin/payments",headers={"Authorization":f"Bearer {admin_object_and_token["access_token"]}"})
    assert payments.status_code==200
    paymentj=payments.json()
    assert any(p["status"]=="SUCCESS" for p in paymentj)
    assert any(p["status"]=="FAILED" for p in paymentj)
    assert all(p["payment_type"]=="SIGNUP" for p in paymentj)



    

