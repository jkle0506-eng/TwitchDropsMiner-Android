"""Custom exceptions for TwitchDropsMiner Android"""

class MinerException(Exception):
    """Base exception class for this application."""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown miner error")


class ExitRequest(MinerException):
    """Raised when the application is requested to exit."""
    def __init__(self):
        super().__init__("Application was requested to exit")


class RequestException(MinerException):
    """Raised for cases where a web request doesn't return what we wanted."""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown error during request")


class LoginException(RequestException):
    """Raised when an exception occurs during login phase."""
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Unknown error during login")


class CaptchaRequired(LoginException):
    """Captcha is required."""
    def __init__(self):
        super().__init__("Captcha is required")


class GQLException(RequestException):
    """Raised when a GQL request returns an error response."""
    def __init__(self, message: str):
        super().__init__(message)


class WebsocketClosed(RequestException):
    """Raised when the websocket connection has been closed."""
    def __init__(self, *args, received: bool = False):
        if args:
            super().__init__(*args)
        else:
            super().__init__("Websocket has been closed")
        self.received = received
