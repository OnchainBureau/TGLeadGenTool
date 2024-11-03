from subprocess import Popen, PIPE
import logging
import time

class DisplayManager:
    def __init__(self):
        self.displays = {}
        self.base_display = 99

    def create_virtual_display(self, instance_id: str) -> int:
        """Create a new virtual display for a Telegram instance."""
        display_num = self.base_display + len(self.displays)
        try:
            xvfb_cmd = f"Xvfb :{display_num} -screen 0 1024x768x16 -ac"
            process = Popen(xvfb_cmd.split(), stdout=PIPE, stderr=PIPE)
            time.sleep(1)  # Wait for display to initialize
            
            self.displays[instance_id] = {
                'display_num': display_num,
                'process': process
            }
            logging.info(f"Created virtual display :{display_num} for instance {instance_id}")
            return display_num
        except Exception as e:
            logging.error(f"Failed to create virtual display for instance {instance_id}: {e}")
            return None

    def get_display(self, instance_id: str) -> str:
        """Get display number for an instance."""
        if instance_id not in self.displays:
            display_num = self.create_virtual_display(instance_id)
            if display_num is None:
                return None
        return f":{self.displays[instance_id]['display_num']}"

    def cleanup(self):
        """Clean up all virtual displays."""
        for instance_id, display_info in self.displays.items():
            if display_info['process']:
                display_info['process'].terminate()
                logging.info(f"Terminated display for instance {instance_id}")