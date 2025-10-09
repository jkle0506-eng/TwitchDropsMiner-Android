"""Inventory and drops management"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from core.utils import timestamp, Game

if TYPE_CHECKING:
    from core.twitch_client import TwitchClient
    from core.channel import Channel


class Benefit:
    """Represents a drop benefit/reward."""

    def __init__(self, data: dict):
        benefit_data = data["benefit"]
        self.id = benefit_data["id"]
        self.name = benefit_data["name"]
        self.image_url = benefit_data.get("imageAssetURL", "")

    def __str__(self):
        return self.name


class TimedDrop:
    """Represents a timed drop."""

    def __init__(self, campaign: 'DropsCampaign', data: dict):
        self._twitch = campaign._twitch
        self.campaign = campaign

        self.id = data["id"]
        self.name = data["name"]
        self.benefits = [Benefit(b) for b in (data.get("benefitEdges") or [])]

        self.starts_at = timestamp(data["startAt"])
        self.ends_at = timestamp(data["endAt"])

        self.required_minutes = data.get("requiredMinutesWatched", 0)
        self.current_minutes = 0

        self.claim_id: Optional[str] = None
        self.is_claimed = False

        # Parse self edge if available
        if "self" in data and data["self"]:
            self_data = data["self"]
            self.claim_id = self_data.get("dropInstanceID")
            self.is_claimed = self_data.get("isClaimed", False)
            self.current_minutes = self_data.get("currentMinutesWatched", 0)

        self.precondition_drops = [d["id"] for d in (data.get("preconditionDrops") or [])]

    @property
    def progress(self) -> float:
        """Progress as a fraction (0.0 to 1.0)."""
        if self.required_minutes == 0:
            return 1.0
        return min(self.current_minutes / self.required_minutes, 1.0)

    @property
    def remaining_minutes(self) -> int:
        """Minutes remaining to complete."""
        return max(0, self.required_minutes - self.current_minutes)

    @property
    def is_complete(self) -> bool:
        """Check if drop is complete."""
        return self.current_minutes >= self.required_minutes

    @property
    def active(self) -> bool:
        """Check if drop is currently active."""
        now = datetime.now(timezone.utc)
        return self.starts_at <= now < self.ends_at

    def can_earn(self) -> bool:
        """Check if drop can be earned."""
        return (
            self.active
            and not self.is_claimed
            and not self.is_complete
        )

    def rewards_text(self) -> str:
        """Get rewards as text."""
        if not self.benefits:
            return "No rewards"
        return ", ".join(b.name for b in self.benefits)

    def __str__(self):
        return f"{self.name} ({self.current_minutes}/{self.required_minutes}min)"

    def __repr__(self):
        return f"TimedDrop({self.name}, {self.progress:.0%})"


class DropsCampaign:
    """Represents a drops campaign."""

    def __init__(self, twitch: 'TwitchClient', data: dict):
        self._twitch = twitch

        self.id = data["id"]
        self.name = data["name"]
        self.game = Game(data["game"])

        self.starts_at = timestamp(data["startAt"])
        self.ends_at = timestamp(data["endAt"])

        self.image_url = data.get("imageURL", "")
        self.description = data.get("description", "")

        # Account linking
        self.account_link_url = data.get("accountLinkURL")
        self.eligible = True

        # Check if account is linked
        if "self" in data and data["self"]:
            self.eligible = data["self"].get("isAccountConnected", False)

        # Parse drops
        self.drops: list[TimedDrop] = []
        self.timed_drops: dict[str, TimedDrop] = {}

        time_based_drops = data.get("timeBasedDrops") or []
        for drop_data in time_based_drops:
            drop = TimedDrop(self, drop_data)
            self.drops.append(drop)
            self.timed_drops[drop.id] = drop

        # Allowed channels
        self.allowed_channels: set = set()
        allow_data = data.get("allow") or {}
        if allow_data.get("isEnabled"):
            channels_data = allow_data.get("channels") or []
            for ch_data in channels_data:
                # Store channel IDs
                self.allowed_channels.add(int(ch_data["id"]))

    @property
    def active(self) -> bool:
        """Check if campaign is currently active."""
        now = datetime.now(timezone.utc)
        return self.starts_at <= now < self.ends_at

    @property
    def total_drops(self) -> int:
        """Total number of drops."""
        return len(self.drops)

    @property
    def claimed_drops(self) -> int:
        """Number of claimed drops."""
        return sum(1 for d in self.drops if d.is_claimed)

    @property
    def remaining_drops(self) -> int:
        """Number of remaining drops."""
        return sum(1 for d in self.drops if not d.is_claimed)

    @property
    def progress(self) -> float:
        """Overall campaign progress."""
        if not self.drops:
            return 0.0
        return sum(d.progress for d in self.drops) / len(self.drops)

    @property
    def remaining_minutes(self) -> int:
        """Total remaining minutes."""
        return sum(d.remaining_minutes for d in self.drops if not d.is_claimed)

    @property
    def availability(self) -> float:
        """Campaign availability (time until end)."""
        now = datetime.now(timezone.utc)
        total = (self.ends_at - self.starts_at).total_seconds()
        remaining = (self.ends_at - now).total_seconds()
        return max(0.0, remaining / total) if total > 0 else 0.0

    @property
    def first_drop(self) -> Optional[TimedDrop]:
        """Get first earnable drop."""
        earnable = [d for d in self.drops if d.can_earn()]
        if not earnable:
            return None
        earnable.sort(key=lambda d: d.remaining_minutes)
        return earnable[0]

    def get_drop(self, drop_id: str) -> Optional[TimedDrop]:
        """Get drop by ID."""
        return self.timed_drops.get(drop_id)

    def can_earn(self, channel: Optional['Channel'] = None) -> bool:
        """Check if campaign can be earned."""
        if not self.eligible or not self.active:
            return False

        if channel is None:
            return any(d.can_earn() for d in self.drops)

        # Check channel restrictions
        if self.allowed_channels and channel.id not in self.allowed_channels:
            return False

        # Check if channel is playing the right game
        if channel.game and channel.game != self.game:
            return False

        return any(d.can_earn() for d in self.drops)

    def __str__(self):
        return f"{self.name} ({self.game.name})"

    def __repr__(self):
        return f"DropsCampaign({self.name}, {self.claimed_drops}/{self.total_drops})"
