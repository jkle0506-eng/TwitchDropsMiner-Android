"""Utility functions and classes"""
import json
import random
import string
import asyncio
from datetime import datetime, timezone
from typing import TypeVar, Generic

_T = TypeVar("_T")


def create_nonce(chars: str, length: int) -> str:
    """Generate a random nonce string."""
    return ''.join(random.choices(chars, k=length))


def timestamp(time_str: str) -> datetime:
    """Convert ISO timestamp string to datetime object."""
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))


def json_minify(data: dict | list) -> str:
    """Returns minified JSON for payload usage."""
    return json.dumps(data, separators=(',', ':'))


class AwaitableValue(Generic[_T]):
    """A value that can be awaited until it's set."""
    def __init__(self):
        self._value: _T = None
        self._event = asyncio.Event()

    def has_value(self) -> bool:
        return self._event.is_set()

    def wait(self):
        return self._event.wait()

    def get_with_default(self, default):
        if self._event.is_set():
            return self._value
        return default

    async def get(self):
        await self._event.wait()
        return self._value

    def set(self, value: _T):
        self._value = value
        self._event.set()

    def clear(self):
        self._event.clear()


class ExponentialBackoff:
    """Exponential backoff iterator for retries."""
    def __init__(self, base: float = 1.0, maximum: float = 60.0, multiplier: float = 2.0):
        self.base = base
        self.maximum = maximum
        self.multiplier = multiplier
        self._current = base

    def __iter__(self):
        return self

    def __next__(self) -> float:
        value = self._current
        self._current = min(self._current * self.multiplier, self.maximum)
        return value

    def reset(self):
        self._current = self.base


class Game:
    """Represents a Twitch game."""
    def __init__(self, data: dict):
        self.id = int(data["id"])
        self.name = data.get("displayName") or data["name"]
        self.slug = data.get("slug", self.name.lower().replace(' ', '-'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Game({self.id}, {self.name})"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return self.id
