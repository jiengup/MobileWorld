"""Sample Android World task: Set an alarm."""

from loguru import logger

from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class SimpleAlarmTask(BaseTask):
    """Set an alarm for a specific time."""

    goal = "Set an alarm for 7:00 AM tomorrow"
    
    task_tags = {"lang-en"}
    
    app_names = {"Clock"}

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task."""
        logger.info("Initializing SimpleAlarmTask")
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Check if the alarm was set successfully."""
        self._check_is_initialized()
        
        logger.info("Checking if alarm was set")
        
        # In a real implementation, we would check the alarm database
        # For now, this is a placeholder based on user confirmation
        try:
            answer = controller.interaction_cache
            if "finished" in str(answer).lower():
                return 1.0, "Alarm set successfully"
            else:
                return 0.0, "Alarm not set or task not completed"
        except Exception as e:
            logger.error(f"Error checking alarm: {e}")
            return 0.0, f"Error verifying alarm: {e}"
