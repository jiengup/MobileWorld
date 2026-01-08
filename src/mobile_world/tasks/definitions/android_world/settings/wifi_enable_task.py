"""Sample Android World task: Turn on WiFi."""

from loguru import logger

from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class WifiEnableTask(BaseTask):
    """Enable WiFi on the device."""

    goal = "Turn on WiFi"
    
    task_tags = {"lang-en"}
    
    app_names = {"Settings"}

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task by ensuring WiFi is off."""
        logger.info("Initializing WifiEnableTask")
        # In a real implementation, we would disable WiFi first
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Check if WiFi was enabled successfully."""
        self._check_is_initialized()
        
        logger.info("Checking if WiFi is enabled")
        
        # In a real implementation, we would check WiFi state via ADB
        # Example: adb shell settings get global wifi_on
        try:
            answer = controller.interaction_cache
            if "finished" in str(answer).lower():
                return 1.0, "WiFi enabled successfully"
            else:
                return 0.0, "WiFi not enabled or task not completed"
        except Exception as e:
            logger.error(f"Error checking WiFi state: {e}")
            return 0.0, f"Error verifying WiFi state: {e}"
