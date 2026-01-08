"""Sample Android World task: Send a text message."""

from loguru import logger

from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class SimpleMessageTask(BaseTask):
    """Send a text message to a contact."""

    goal = "Send a text message 'Hello World' to contact '555-5678'"
    
    task_tags = {"lang-en"}
    
    app_names = {"Messages"}

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task."""
        logger.info("Initializing SimpleMessageTask")
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Check if the message was sent successfully."""
        self._check_is_initialized()
        
        logger.info("Checking if message was sent")
        
        # In a real implementation, we would check the SMS database
        # For now, this is a placeholder
        try:
            answer = controller.interaction_cache
            if "finished" in str(answer).lower():
                return 1.0, "Message sent successfully"
            else:
                return 0.0, "Message not sent or task not completed"
        except Exception as e:
            logger.error(f"Error checking message: {e}")
            return 0.0, f"Error verifying message: {e}"
