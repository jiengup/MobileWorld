"""Sample Android World task: Change screen brightness."""

from loguru import logger

from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class BrightnessTask(BaseTask):
    """Adjust screen brightness to maximum."""

    goal = "Set screen brightness to maximum"
    
    task_tags = {"lang-en"}
    
    app_names = {"Settings"}

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task."""
        logger.info("Initializing BrightnessTask")
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Check if brightness was set to maximum."""
        self._check_is_initialized()
        
        logger.info("Checking if brightness is at maximum")
        
        # In a real implementation, we would check brightness via ADB
        # Example: adb shell settings get system screen_brightness
        try:
            answer = controller.interaction_cache
            if "finished" in str(answer).lower():
                return 1.0, "Brightness set to maximum successfully"
            else:
                return 0.0, "Brightness not set or task not completed"
        except Exception as e:
            logger.error(f"Error checking brightness: {e}")
            return 0.0, f"Error verifying brightness: {e}"
