from jose import jwt, JWTError
from fastapi import WebSocket, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.config import settings

async def get_user_from_websocket(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    db: Session = SessionLocal()
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db.close()

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return user
