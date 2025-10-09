"""Websocket client for Twitch PubSub"""
import asyncio
import json
import logging
from time import time
from typing import Optional, TYPE_CHECKING

import aiohttp

from core.constants import WS_URL, PING_INTERVAL, PING_TIMEOUT, MAX_WEBSOCKETS, WS_TOPICS_LIMIT
from core.utils import create_nonce
from core.exceptions import WebsocketClosed

if TYPE_CHECKING:
    from core.twitch_client import TwitchClient

logger = logging.getLogger("TwitchDrops.websocket")


class Websocket:
    """Single websocket connection."""

    def __init__(self, pool: 'WebsocketPool', index: int):
        self._pool = pool
        self._twitch = pool._twitch
        self._idx = index

        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._running = False
        self._handle_task: Optional[asyncio.Task] = None

        self.topics: dict[str, any] = {}

        # Ping tracking
        self._next_ping = time()
        self._max_pong = self._next_ping + PING_TIMEOUT.total_seconds()

    @property
    def connected(self) -> bool:
        return self._ws is not None and not self._ws.closed

    async def start(self):
        """Start websocket connection."""
        if self._running:
            return

        self._running = True
        self._handle_task = asyncio.create_task(self._handle())

    async def stop(self):
        """Stop websocket connection."""
        if not self._running:
            return

        self._running = False

        if self._ws and not self._ws.closed:
            await self._ws.close()

        if self._handle_task:
            self._handle_task.cancel()
            try:
                await self._handle_task
            except asyncio.CancelledError:
                pass

    async def _handle(self):
        """Main websocket handler."""
        session = await self._twitch.get_session()

        while self._running:
            try:
                async with session.ws_connect(WS_URL) as ws:
                    self._ws = ws
                    logger.info(f"Websocket[{self._idx}] connected")

                    # Subscribe to topics
                    await self._subscribe_topics()

                    # Main loop
                    while self._running and not ws.closed:
                        # Check ping
                        now = time()
                        if now >= self._next_ping:
                            await self._send_ping()
                            self._next_ping = now + PING_INTERVAL.total_seconds()
                            self._max_pong = now + PING_TIMEOUT.total_seconds()

                        # Check pong timeout
                        if now >= self._max_pong:
                            logger.warning(f"Websocket[{self._idx}] pong timeout")
                            break

                        # Receive messages
                        try:
                            msg = await asyncio.wait_for(ws.receive(), timeout=0.5)

                            if msg.type == aiohttp.WSMsgType.TEXT:
                                await self._handle_message(json.loads(msg.data))
                            elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED):
                                break

                        except asyncio.TimeoutError:
                            continue

            except Exception as e:
                logger.error(f"Websocket[{self._idx}] error: {e}")

            if self._running:
                await asyncio.sleep(5)  # Reconnect delay

    async def _send_ping(self):
        """Send PING message."""
        if self._ws and not self._ws.closed:
            await self._ws.send_json({"type": "PING"})
            logger.debug(f"Websocket[{self._idx}] sent PING")

    async def _subscribe_topics(self):
        """Subscribe to topics."""
        if not self.topics or not self._ws:
            return

        message = {
            "type": "LISTEN",
            "nonce": create_nonce("abcdefghijklmnopqrstuvwxyz", 30),
            "data": {
                "topics": list(self.topics.keys()),
                "auth_token": self._twitch.settings.oauth_token
            }
        }

        await self._ws.send_json(message)
        logger.info(f"Websocket[{self._idx}] subscribed to {len(self.topics)} topics")

    async def _handle_message(self, message: dict):
        """Handle received message."""
        msg_type = message.get("type")

        if msg_type == "PONG":
            self._max_pong = self._next_ping
            logger.debug(f"Websocket[{self._idx}] received PONG")

        elif msg_type == "MESSAGE":
            data = message.get("data", {})
            topic = data.get("topic")

            if topic in self.topics:
                try:
                    payload = json.loads(data.get("message", "{}"))
                    await self.topics[topic](payload)
                except Exception as e:
                    logger.error(f"Error handling topic {topic}: {e}")

        elif msg_type == "RESPONSE":
            error = message.get("error")
            if error:
                logger.error(f"Websocket[{self._idx}] error response: {error}")

        elif msg_type == "RECONNECT":
            logger.warning(f"Websocket[{self._idx}] reconnect requested")
            if self._ws:
                await self._ws.close()

    def add_topic(self, topic: str, handler):
        """Add a topic to subscribe to."""
        self.topics[topic] = handler


class WebsocketPool:
    """Pool of websocket connections."""

    def __init__(self, twitch: 'TwitchClient'):
        self._twitch = twitch
        self.websockets: list[Websocket] = []
        self._running = False

    async def start(self):
        """Start websocket pool."""
        if self._running:
            return

        self._running = True

        # Create initial websocket
        ws = Websocket(self, 0)
        self.websockets.append(ws)

        # Add user topics
        if self._twitch.settings.user_id:
            user_id = self._twitch.settings.user_id
            ws.add_topic(f"user-drop-events.{user_id}", self._handle_drop_event)

        await ws.start()

    async def stop(self):
        """Stop websocket pool."""
        if not self._running:
            return

        self._running = False

        for ws in self.websockets:
            await ws.stop()

        self.websockets.clear()

    async def _handle_drop_event(self, payload: dict):
        """Handle drop progress event."""
        try:
            event_type = payload.get("type")

            if event_type == "drop-progress":
                drop_id = payload.get("drop_id")
                current_minutes = payload.get("current_minutes", 0)
                required_minutes = payload.get("required_minutes", 0)

                logger.info(f"Drop progress: {drop_id} - {current_minutes}/{required_minutes}")

                # Update drop in inventory
                for campaign in self._twitch.inventory:
                    drop = campaign.get_drop(drop_id)
                    if drop:
                        drop.current_minutes = current_minutes
                        self._twitch.update_drop(drop)
                        break

            elif event_type == "drop-claim":
                drop_id = payload.get("drop_id")
                logger.info(f"Drop ready to claim: {drop_id}")

                # Find and claim drop
                for campaign in self._twitch.inventory:
                    drop = campaign.get_drop(drop_id)
                    if drop and not drop.is_claimed:
                        await self._twitch.claim_drop(drop)
                        break

        except Exception as e:
            logger.error(f"Error handling drop event: {e}")
