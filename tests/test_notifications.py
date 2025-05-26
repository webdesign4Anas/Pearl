from app import models
def test_retrieve_notificaitons_for_specefic_business_owner(client,test_business_owner,session,paid_business_owner):
    notifications1=models.Notification(
        business_owner_id=paid_business_owner.id,
        message="U GOT NEW PURCHASE",
        is_read=False,
    )
    notifications2=models.Notification(
        business_owner_id=paid_business_owner.id,
        message="U Have NEW PURCHASE",
        is_read=True,
    )
    session.add_all([notifications1,notifications2])
    session.commit()
    response=client.get("/notifications",headers={"Authorization":f"Bearer {test_business_owner["access_token"]}"})
    notificationslist=response.json()
    assert response.status_code==200
    assert notificationslist[0]["message"]=="U GOT NEW PURCHASE"
    assert notificationslist[1]["message"]=="U Have NEW PURCHASE"

def test_make_user_specefic_notification_become_read(client,test_business_owner,session,paid_business_owner):
    notifications1=models.Notification(
        business_owner_id=paid_business_owner.id,
        message="U GOT NEW PURCHASE",
        is_read=False,
    )
    notifications2=models.Notification(
        business_owner_id=paid_business_owner.id,
        message="U Have NEW PURCHASE",
        is_read=True,
    )
    session.add_all([notifications1,notifications2])
    session.commit()
    response=client.put("/notifications/1/mark-read",headers={"Authorization":f"Bearer {test_business_owner["access_token"]}"})
    assert response.status_code==200
    response=client.put("/notifications/2/mark-read",headers={"Authorization":f"Bearer {test_business_owner["access_token"]}"})
    assert response.status_code==200
    response=client.put("/notifications/3/mark-read",headers={"Authorization":f"Bearer {test_business_owner["access_token"]}"}) #testing id that is not existed
    assert response.status_code==404
    




