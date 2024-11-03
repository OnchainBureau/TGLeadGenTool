import re
import logging
from pathlib import Path
from .telegram_instance import TelegramInstance
from .database import Database
from .display_manager import DisplayManager

class MessageHandler:
    def __init__(self, instances_dir: Path, db: Database):
        self.instances_dir = instances_dir
        self.db = db
        self.display_manager = DisplayManager()  # Add this line
        self.instances = self._setup_instances()

    def _setup_instances(self):
        """Setup all Telegram instances."""
        instances = []
        for instance_dir in self.instances_dir.iterdir():
            if instance_dir.is_dir() and (instance_dir / "Telegram").exists():
                instance = TelegramInstance(
                    instance_path=instance_dir,
                    display_manager=self.display_manager
                )
                instances.append(instance)
        return instances
    
    def __del__(self):
        """Cleanup display manager when handler is destroyed."""
        if hasattr(self, 'display_manager'):
            self.display_manager.cleanup()

    def extract_group_links(self, text: str):
        """Extract Telegram group links from text."""
        return re.findall(r'https?://t\.me/\S+', text)

    def process_main_channel(self, channel_link: str):
        """Process main channel and extract group links."""
        if not self.instances:
            logging.error("No Telegram instances available.")
            return

        instance = self.instances[0]  # Use first instance for scraping
        if instance.navigate_to_group(channel_link):
            messages = instance.get_visible_messages()

            for message in messages:
                links = self.extract_group_links(message)
                for link in links:
                    self.db.add_group(link.strip())