"""TwitchDropsMiner Android - Main Application"""
import asyncio
import logging
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

from core.settings import Settings
from core.twitch_client import TwitchClient
from ui.screens import (
    HomeScreen,
    LoginScreen,
    InventoryScreen,
    SettingsScreen,
    ChannelsScreen,
    LogsScreen
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TwitchDrops")


class TwitchDropsMinerApp(MDApp):
    """Main application class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "TwitchDropsMiner"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"

        # Core
        self.settings = Settings()
        self.twitch_client: TwitchClient = None

        # UI
        self.screen_manager: ScreenManager = None
        self.logs: list[str] = []

        # Asyncio
        self.loop = None

    def build(self):
        """Build the application UI."""
        # Setup asyncio
        self.loop = asyncio.get_event_loop()

        # Create screen manager
        self.screen_manager = ScreenManager()

        # Add screens
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(InventoryScreen(name='inventory'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(ChannelsScreen(name='channels'))
        self.screen_manager.add_widget(LogsScreen(name='logs'))

        # Initialize Twitch client
        callbacks = {
            'on_print': self.on_print,
            'on_status': self.on_status,
            'on_progress': self.on_progress,
            'on_channel': self.on_channel,
            'on_drop': self.on_drop,
            'on_inventory': self.on_inventory,
            'on_notify': self.on_notify,
        }
        self.twitch_client = TwitchClient(self.settings, callbacks)

        # Check if logged in
        if self.settings.oauth_token:
            self.screen_manager.current = 'home'
        else:
            self.screen_manager.current = 'login'

        # Schedule asyncio loop
        Clock.schedule_interval(self._run_async_loop, 0)

        return self.screen_manager

    def _run_async_loop(self, dt):
        """Run asyncio loop."""
        try:
            self.loop.stop()
            self.loop.run_forever()
        except Exception as e:
            logger.error(f"Async loop error: {e}")

    def on_start(self):
        """Called when the application starts."""
        logger.info("TwitchDropsMiner started")

    def on_stop(self):
        """Called when the application stops."""
        logger.info("TwitchDropsMiner stopping")

        # Stop twitch client
        if self.twitch_client and self.twitch_client._running:
            asyncio.run_coroutine_threadsafe(
                self.twitch_client.stop(),
                self.loop
            )

        # Save settings
        self.settings.save(force=True)

    # ========================================================================
    # CALLBACKS
    # ========================================================================

    def on_print(self, message: str):
        """Handle print message."""
        logger.info(message)
        self.logs.append(f"{message}")

        # Update logs screen if visible
        if self.screen_manager.current == 'logs':
            logs_screen = self.screen_manager.get_screen('logs')
            logs_screen.add_log(message)

    def on_status(self, status: str):
        """Handle status update."""
        home_screen = self.screen_manager.get_screen('home')
        home_screen.update_status(status)

    def on_progress(self, current: int, total: int):
        """Handle progress update."""
        home_screen = self.screen_manager.get_screen('home')
        home_screen.update_progress(current, total)

    def on_channel(self, channel_name: str):
        """Handle channel update."""
        home_screen = self.screen_manager.get_screen('home')
        home_screen.update_channel(channel_name)

    def on_drop(self, drop):
        """Handle drop update."""
        home_screen = self.screen_manager.get_screen('home')
        home_screen.update_drop(drop)

    def on_inventory(self, inventory: list):
        """Handle inventory update."""
        inventory_screen = self.screen_manager.get_screen('inventory')
        inventory_screen.update_inventory(inventory)

    def on_notify(self, title: str, message: str):
        """Handle notification."""
        if platform == 'android':
            try:
                from android.runnable import run_on_ui_thread
                from jnius import autoclass

                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
                NotificationManager = autoclass('android.app.NotificationManager')
                Context = autoclass('android.content.Context')

                @run_on_ui_thread
                def show_notification():
                    activity = PythonActivity.mActivity
                    notification_service = activity.getSystemService(Context.NOTIFICATION_SERVICE)

                    builder = NotificationCompat.Builder(activity, "twitch_drops")
                    builder.setContentTitle(title)
                    builder.setContentText(message)
                    builder.setSmallIcon(activity.getApplicationInfo().icon)

                    notification_service.notify(1, builder.build())

                show_notification()
            except Exception as e:
                logger.error(f"Notification error: {e}")

        # Show snackbar
        Snackbar(text=f"{title}: {message}").open()

    # ========================================================================
    # ACTIONS
    # ========================================================================

    def start_mining(self):
        """Start mining."""
        if self.twitch_client and not self.twitch_client._running:
            asyncio.run_coroutine_threadsafe(
                self.twitch_client.start(),
                self.loop
            )

    def stop_mining(self):
        """Stop mining."""
        if self.twitch_client and self.twitch_client._running:
            asyncio.run_coroutine_threadsafe(
                self.twitch_client.stop(),
                self.loop
            )

    def login(self, oauth_token: str):
        """Login with OAuth token."""
        self.settings.oauth_token = oauth_token
        self.settings.save()

        # Try to login
        asyncio.run_coroutine_threadsafe(
            self.twitch_client.login(),
            self.loop
        )

        # Switch to home screen
        self.screen_manager.current = 'home'

    def logout(self):
        """Logout."""
        # Stop mining
        self.stop_mining()

        # Clear token
        self.settings.oauth_token = ""
        self.settings.user_id = None
        self.settings.username = ""
        self.settings.save()

        # Switch to login screen
        self.screen_manager.current = 'login'


def main():
    """Main entry point."""
    TwitchDropsMinerApp().run()


if __name__ == '__main__':
    main()
