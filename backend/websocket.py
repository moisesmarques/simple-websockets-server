#!/usr/bin/env python
import os
import asyncio
import websockets
import aioredis
import json
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

CONNECTIONS = {}

async def handler(websocket):
    try:
        credentials = await websocket.recv()        
        token = jwt.decode(credentials.strip(), os.getenv("JWT_SECRET"), algorithms=["HS256"])        
        user_id = token['sub']
        CONNECTIONS[user_id] = websocket

        await websocket.wait_closed()

    except websockets.exceptions.ConnectionClosedOK:
        pass
    except Exception as e:
        pass

async def process_events():
    
    redis = aioredis.from_url(os.getenv("REDIS_URL"))
    pubsub = redis.pubsub()
    await pubsub.subscribe("events")
    
    async for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"].decode())
            receivers = event.get("receivers", None)
            
            if receivers is None:
                websocket_receivers = CONNECTIONS.values() 
            else:
                websocket_receivers = (CONNECTIONS[receiver_id] for receiver_id in receivers if receiver_id in CONNECTIONS)
            
            try:
                websockets.broadcast(websocket_receivers, json.dumps(event["data"]))
            except Exception as e:
                for receiver_id in receivers:
                    if receiver_id in CONNECTIONS:
                        del CONNECTIONS[receiver_id]

async def main():
    async with websockets.serve(handler, host="0.0.0.0", port=8888):
    #async with websockets.unix_serve(handler, path=f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock"):
        await process_events()

if __name__ == "__main__":
    asyncio.run(main())
