from app import models

#create wishlist for the user
def test_create_wishlist_for_user(client,session,services,test_business_owner,test_user):
    make_wishlist=client.post("/wishlist",json={"service_id":services[0]["id"]},headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert make_wishlist.status_code==201
    make_another=client.post("/wishlist",json={"service_id":services[0]["id"]},headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert make_another.status_code==400
    assert make_another.json()["detail"]=="Item Already Exists In Your WishList"



#retrive user specefic wishlist
def test_retrieve_user_specefic_wish_list(client,session,services,test_business_owner,test_user):
    image=models.ServiceImage(
        service_id=services[0]["id"],
        description="firstPhoto",
        image_url="www.bestimage.com"
    )
    session.add(image)
    session.commit()
    make_wishlist=client.post("/wishlist",json={"service_id":services[0]["id"]},headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert make_wishlist.status_code==201
    get_wishlist=client.get("/wishlist",headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    wishlists=get_wishlist.json()
    assert len(wishlists)==1
    service= wishlists[0]["service"]
    assert service["name"]=="wpop"
    assert service["image_preview_url"]=="www.bestimage.com"

def test_delete_that_wishlist(client,session,services,test_business_owner,test_user):
    make_wishlist=client.post("/wishlist",json={"service_id":services[0]["id"]},headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert make_wishlist.status_code==201
    delete_wishlist=client.delete("/wishlist/1",headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert delete_wishlist.status_code==204
    delete_same_wishlist=client.delete("/wishlist/1",headers={"Authorization":f"Bearer {test_user["access_token"]}"})
    assert delete_same_wishlist.status_code==404
    assert delete_same_wishlist.json()["detail"]=="Item Not Found"