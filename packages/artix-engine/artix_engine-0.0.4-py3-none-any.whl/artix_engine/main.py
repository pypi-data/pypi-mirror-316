import asyncio
import json
import websockets
import logging
from typing import (
    Callable,
    Dict
)
from .types import Message

logging.basicConfig(level=logging.INFO)

class Client:
    def __init__(self, token: str):
        """Create client\nGet your token on discord developer!"""
        self.gateway_url: str = "wss://gateway.discord.gg/?v=10&encoding=json"
        self.token = token
        self.heartbeat_interval = None
        self.session = None
        self.event_handlers: Dict[str, Callable] = {}
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
    
    def handler_events(self, event_name: str):
        """Handling events"""
        def decorator(func: Callable):
            self.event_handlers[event_name] = func
            logging.info(f"Handler for {event_name} registered.")
            return func
        return decorator
    async def connect(self):
        """Connect on gateway."""
        async with websockets.connect(self.gateway_url) as ws:
            logging.info("connecting to gateway...")
            self.session = ws

            hello_message = await ws.recv()
            hell_data = json.loads(hello_message)
            self.heartbeat_interval = hell_data['d']['heartbeat_interval'] / 1000
            logging.info(f"Getting heartbeat: {self.heartbeat_interval}S")

            await self.identity()
            await asyncio.gather(self.heartbeat(), self.handle_events())

    async def identity(self):
        """Set identity"""
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 512,
                "properties": {
                    "os": "linux",
                    "browser": "artix",
                    "device": "artix"
                }
            }
        }
        logging.info("authorization")
        await self.session.send(json.dumps(payload))
    
    async def heartbeat(self):
        """Send hearbeat"""
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            logging.info("HEARTBEAT SEND")
            await self.session.send(json.dumps({"op": 1, "d": None}))
    
    async def handle_events(self):
        async for message in self.session:
            event = json.loads(message)
            op = event.get('op')
            t = event.get('t')  # Назва події
            d = event.get('d')  # Дані події

            if op == 0 and t in self.event_handlers:
                handler = self.event_handlers[t]
                logging.info(f"Handling event {t}")
                await handler(Message(self, d))
