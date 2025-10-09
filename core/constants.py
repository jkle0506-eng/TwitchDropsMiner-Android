"""Constants for TwitchDropsMiner Android"""
from datetime import timedelta
from enum import Enum, auto

VERSION = "1.0.0-android"

# Twitch API constants
CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# GQL endpoint
GQL_URL = "https://gql.twitch.tv/gql"

# Websocket
WS_URL = "wss://pubsub-edge.twitch.tv/v1"
PING_INTERVAL = timedelta(minutes=4)
PING_TIMEOUT = timedelta(seconds=10)
MAX_WEBSOCKETS = 10
WS_TOPICS_LIMIT = 50

# Timing
WATCH_INTERVAL = timedelta(seconds=20)
ONLINE_DELAY = timedelta(seconds=120)

# Limits
MAX_CHANNELS = 100
MAX_INT = 2147483647


class State(Enum):
    """Application states"""
    IDLE = auto()
    INVENTORY_FETCH = auto()
    GAMES_UPDATE = auto()
    CHANNELS_FETCH = auto()
    CHANNELS_CLEANUP = auto()
    CHANNEL_SWITCH = auto()
    CHANNEL_ONLINE = auto()
    EXIT = auto()


class PriorityMode(Enum):
    """Priority modes for campaign selection"""
    PRIORITY_ONLY = "priority_only"
    ENDING_SOONEST = "ending_soonest"
    LOW_AVAILABILITY = "low_availability"


# GQL Operations
GQL_OPERATIONS = {
    "GetDropCampaigns": {
        "operationName": "ViewerDropsDashboard",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "8d5d9b5e3f088f9d1ff39eb2caab11f7a4cf7a3353da9ce82b5778226ff37268"
            }
        },
        "variables": {
            "fetchRewardCampaigns": True
        }
    },
    "GetInventory": {
        "operationName": "Inventory",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "37fea486d6179047c41d0f549088a4c3a7dd60c05c70956e5f1dce3996103923"
            }
        },
        "variables": {
            "fetchRewardCampaigns": True
        }
    },
    "GetStreamInfo": {
        "operationName": "StreamMetadata",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "059c4653b788f5bdb2f5a2d2a24b0ddc3831a15079001a3d927556a96fb0517f"
            }
        },
        "variables": {
            "channelLogin": ""
        }
    },
    "GetDirectory": {
        "operationName": "DirectoryPage_Game",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "d5c5df7ab9ae65c3ea0f225738c08a36a4a76e4c6c31db7f8c4b8dc064227f9e"
            }
        },
        "variables": {
            "limit": 30,
            "slug": "",
            "options": {
                "includeRestricted": ["SUB_ONLY_LIVE"],
                "systemFilters": ["DROPS_ENABLED"]
            }
        }
    },
    "ClaimDrop": {
        "operationName": "DropsPage_ClaimDropRewards",
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "2f884fa187b8fadb2a49db0adc033e636f7b6aaee6e76de1e2bba9a7baf0daf6"
            }
        },
        "variables": {
            "input": {
                "dropInstanceID": ""
            }
        }
    }
}

# Websocket topics
WEBSOCKET_TOPICS = {
    "User": {
        "Drops": "user-drop-events",
        "Notifications": "onsite-notifications",
    },
    "Channel": {
        "StreamState": "video-playback-by-id",
        "StreamUpdate": "broadcast-settings-update",
    }
}
