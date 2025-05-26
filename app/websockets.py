from fastapi import WebSocket,WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections:dict[int,WebSocket]={}
    async def connect(self,business_owner_id:int,websocket:WebSocket):
        await websocket.accept()
        self.active_connections[business_owner_id]=websocket

    def disconnect(self,business_owner_id:int):
        self.active_connections.pop(business_owner_id,None)


    async def send_personal_message(self, message: str, business_owner_id: int):
        websocket = self.active_connections.get(business_owner_id)
        if websocket:
            await websocket.send_text(message)   
manager=ConnectionManager()