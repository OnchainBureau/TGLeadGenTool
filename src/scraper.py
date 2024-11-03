import asyncio
from typing import List
from .telegram_instance import TelegramInstance
from .database import Database
from .display_manager import DisplayManager
import logging
import os
from pathlib import Path

class TelegramScraper:
    def __init__(self):
        self.db = Database()
        self.target_channel = os.getenv('TARGET_CHANNEL')
        self.message_template = os.getenv('MESSAGE_TEMPLATE', "Hello! I'm interested in this group.")
        self.display_manager = DisplayManager()  # Add this line
        self.clients = self._setup_clients()

    def _setup_clients(self) -> List[TelegramInstance]:
        """Setup Telegram clients from environment variables."""
        clients = []
        client_count = int(os.getenv('CLIENT_COUNT', 3))
        instance_ids = os.getenv('INSTANCE_IDS', '').split(',')

        for i in range(client_count):
            instance_id = instance_ids[i]
            instance_path = Path(f"/app/instances/{instance_id}")
            # Updated to use display_manager instead of display_number
            client = TelegramInstance(
                instance_path=instance_path,
                display_manager=self.display_manager
            )
            clients.append(client)

        return clients
    
    def __del__(self):
        """Cleanup display manager when scraper is destroyed."""
        if hasattr(self, 'display_manager'):
            self.display_manager.cleanup()

    async def process_groups(self):
        """Main processing logic."""
        # Start all clients
        for client in self.clients:
            client.start()
        
        await asyncio.sleep(15)  # Wait for all clients to fully start

        # Get messages from target channel using the first client
        client = self.clients[0]
        if client.navigate_to_group(self.target_channel):
            messages = client.get_visible_messages()

            # Extract and store group links
            links = client.extract_group_links(messages)
            for link in links:
                self.db.add_group(link.strip())

        # Process unprocessed groups
        unprocessed = self.db.get_unprocessed_groups()
        for i, group in enumerate(unprocessed):
            client = self.clients[i % len(self.clients)]
            if client.join_group(group.group_link):
                if client.send_message(group.group_link, self.message_template):
                    self.db.mark_group_processed(group.group_link, f"client_{i % len(self.clients)}")
                await asyncio.sleep(2)  # Rate limiting

        # Optionally stop clients after processing
        for client in self.clients:
            client.stop()