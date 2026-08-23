import asyncio
import json
import time
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import platform
import fastapi

router = APIRouter(prefix="/ws", tags=["Real-time WebSockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Broadcast updated visitor count
        await self.broadcast({
            "type": "visitor_count",
            "active_visitors": len(self.active_connections),
            "timestamp": time.time()
        })

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/live-stats")
async def websocket_live_stats(websocket: WebSocket):
    """
    WebSocket endpoint for real-time live visitor counter and server heartbeat telemetry.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Receive client ping or commands
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                cmd = msg.get("command")
                if cmd == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": time.time(),
                        "active_visitors": len(manager.active_connections)
                    })
                elif cmd == "server_info":
                    await websocket.send_json({
                        "type": "server_info",
                        "active_connections": len(manager.active_connections),
                        "platform": platform.platform(),
                        "timestamp": time.time()
                    })
            except Exception:
                await websocket.send_json({"type": "echo", "data": data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "visitor_count",
            "active_visitors": len(manager.active_connections),
            "timestamp": time.time()
        })
