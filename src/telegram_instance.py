import pyautogui
import time
import logging
import os
from pathlib import Path
from subprocess import Popen, PIPE
from .display_manager import DisplayManager

class TelegramInstance:
    def __init__(self, instance_path: Path, display_manager: DisplayManager):
        self.instance_path = instance_path
        self.exe_path = instance_path / "Telegram"
        self.tdata_path = instance_path / "tdata"
        self.process = None
        self.display_manager = display_manager
        self.display = self.display_manager.get_display(instance_path.name)

    def start(self):
        """Start the Telegram instance."""
        if self.display is None:
            logging.error(f"No display available for instance {self.instance_path.name}")
            return False

        try:
            env = os.environ.copy()
            env['DISPLAY'] = self.display
            
            self.process = Popen(
                [str(self.exe_path)],
                env=env,
                cwd=str(self.instance_path)
            )
            logging.info(f"Started Telegram instance {self.instance_path.name} on display {self.display}")
            return True
        except Exception as e:
            logging.error(f"Failed to start Telegram instance: {e}")
            return False

    def navigate_to_group(self, group_link: str):
        """Navigate to a specific group using GUI automation."""
        try:
            # Ensure the correct DISPLAY is set
            os.environ["DISPLAY"] = self.display

            # Focus on the Telegram window
            pyautogui.getWindowsWithTitle("Telegram")[0].activate()
            time.sleep(2)

            # Click on the search bar (coordinates might need adjustment)
            pyautogui.click(x=200, y=50)  # Example coordinates
            time.sleep(1)

            # Type the group link
            pyautogui.write(group_link, interval=0.1)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)
            logging.info(f"Navigated to group: {group_link} in instance {self.instance_path.name}")
            return True
        except Exception as e:
            logging.error(f"Error navigating to group in instance {self.instance_path.name}: {e}")
            return False

    def get_visible_messages(self):
        """Retrieve visible messages using GUI automation."""
        # Implement message retrieval logic using GUI automation
        # This might involve taking screenshots and OCR, which can be complex
        # Placeholder implementation
        return "Sample message containing https://t.me/samplegroup"

    def extract_group_links(self, text: str):
        """Extract Telegram group links from text."""
        import re
        return re.findall(r'https?://t\.me/\S+', text)

    def join_group(self, group_link: str):
        """Join a Telegram group using GUI automation."""
        try:
            if self.navigate_to_group(group_link):
                # Click 'Join' button (coordinates might need adjustment)
                pyautogui.click(x=300, y=300)  # Example coordinates
                time.sleep(2)
                logging.info(f"Joined group: {group_link} in instance {self.instance_path.name}")
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to join group {group_link} in instance {self.instance_path.name}: {e}")
            return False

    def send_message(self, group_link: str, message: str):
        """Send a message to a Telegram group using GUI automation."""
        try:
            if self.navigate_to_group(group_link):
                # Click on the message input field
                pyautogui.click(x=300, y=500)  # Example coordinates
                time.sleep(1)
                # Type the message
                pyautogui.write(message, interval=0.1)
                time.sleep(0.5)
                # Press Enter to send
                pyautogui.press('enter')
                logging.info(f"Sent message to group: {group_link} in instance {self.instance_path.name}")
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to send message to group {group_link} in instance {self.instance_path.name}: {e}")
            return False

    def stop(self):
        """Stop the Telegram instance."""
        if self.process:
            self.process.terminate()
            self.process = None