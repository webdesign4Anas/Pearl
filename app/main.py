from fastapi import  FastAPI,APIRouter,status
from fastapi import FastAPI, WebSocket,WebSocketDisconnect
from app.websockets import manager
from app.routers import users,auth,register_routes,wishlist,services,admin,payment,notifications,purchases
from app.jwt_websockets import get_user_from_websocket
app=FastAPI()



app.include_router(users.router)
app.include_router(auth.router)
app.include_router(register_routes.router)
app.include_router(wishlist.router)
app.include_router(services.router)
app.include_router(admin.router)
app.include_router(payment.router)
app.include_router(notifications.router)
app.include_router(purchases.router)

@app.get("/")
def root():
    return{"message":"Hello World"}






@app.websocket("/ws/{business_owner_id}")
async def websocket_endpoint(websocket: WebSocket, business_owner_id: int):
    await websocket.accept()

    user = await get_user_from_websocket(websocket)
    if not user or user.role != "BUSINESS_OWNER" or user.id != business_owner_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # now you're authenticated
    await manager.connect(business_owner_id, websocket)
