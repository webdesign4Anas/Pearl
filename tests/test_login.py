

def test_user_login(client,test_user):
    login_data = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
    response=client.post("/login",data=login_data)
    assert response.status_code==201
    token=response.json()["token_type"]
    assert token =="bearer"


def test_business_owners_login(client,test_business_owner):
    login_data = {
            "username": test_business_owner["email"],
            "password": test_business_owner["password"]
        }
    response=client.post("/login",data=login_data)
    assert response.status_code==201
    token=response.json()["token_type"]
    assert token =="bearer"
    