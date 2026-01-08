"""Sample Android World task: Create and verify a contact."""

from loguru import logger

from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class SimpleContactTask(BaseTask):
    """Create a new contact and verify it was added."""

    goal = "Create a new contact named 'John Doe' with phone number '555-1234'"
    
    task_tags = {"lang-en"}
    
    app_names = {"Contacts"}

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task by clearing existing contacts."""
        logger.info("Initializing SimpleContactTask")
        # In a real implementation, we would clear existing contacts
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Check if the contact was created successfully."""
        self._check_is_initialized()
        
        # In a real implementation, we would query the contacts database
        # For now, this is a placeholder
        logger.info("Checking if contact was created")
        
        # Placeholder logic - in real implementation, check contacts database
        # using ADB or ContentProvider queries
        try:
            # Example: controller.execute_adb_command("content query --uri content://contacts/...")
            # For now, return success if user answered with "finished"
            answer = controller.interaction_cache
            if "finished" in str(answer).lower():
                return 1.0, "Contact created successfully"
            else:
                return 0.0, "Contact not created or task not completed"
        except Exception as e:
            logger.error(f"Error checking contact: {e}")
            return 0.0, f"Error verifying contact: {e}"
