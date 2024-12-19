import asyncio
import json
import logging
from pathlib import Path

import jwt

from fastapi import WebSocket, APIRouter, HTTPException, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from starlette.types import Message

logger = logging.getLogger(__name__)


class ConnectionManager:

    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self.active_connections = []
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    async def connect(self, websocket: WebSocket, token: str):
        try:
            _ = jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
        except jwt.ExpiredSignatureError:
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="Invalid token")

        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Connection established with {websocket} len={len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Connection closed with {websocket} len={len(self.active_connections)}")

    async def broadcast(self, channel: str, payload):
        message = json.dumps({"channel": channel, "payload": payload})
        tasks = []
        for connection in self.active_connections:
            tasks.append(connection.send_text(message))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, WebSocketDisconnect):
                self.disconnect(self.active_connections[i])


def setup_app(app, jwt_secret_key: str, base_path='/ws', jwt_algorithm: str = "HS256"):
    ws_router = get_ws_router(
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm=jwt_algorithm,
        base_path=base_path
    )
    current_dir = Path(__file__).parent
    static_dir = current_dir / "static/js"

    app.mount("/js", StaticFiles(directory=static_dir), name="js")
    app.include_router(ws_router)

    return app


def get_ws_router(jwt_secret_key: str, base_path='ws', jwt_algorithm: str = "HS256"):
    ws_router = APIRouter()

    current_dir = Path(__file__).parent
    static_dir = current_dir / "static/js"
    ws_router.mount(f"{base_path}/js", StaticFiles(directory=static_dir), name="js")

    manager = ConnectionManager(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm)

    @ws_router.post(f"{base_path}/emmit")
    async def emmit_endpoint(request: Request):
        payload = await request.json()
        await manager.broadcast(payload["channel"], payload["payload"])
        return True

    @ws_router.websocket(f"{base_path}/")
    async def websocket_endpoint(websocket: WebSocket):
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="Token required")

        await manager.connect(websocket, token)
        try:
            while True:
                message: Message = await websocket.receive()
                if message["type"] == "websocket.disconnect":
                    manager.disconnect(websocket)
                    break
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    return ws_router
