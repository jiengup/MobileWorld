# Android World Benchmark Tasks

This directory contains tasks from the Android World benchmark suite, integrated into the MobileWorld framework.

## Overview

Android World is a benchmark for evaluating autonomous agents on Android devices. These tasks have been adapted to work with the MobileWorld infrastructure while maintaining compatibility with the Android World evaluation methodology.

## Current Tasks

### Contacts
- **SimpleContactTask**: Create a new contact with name and phone number

### Settings
- **BrightnessTask**: Adjust screen brightness to maximum
- **WifiEnableTask**: Enable WiFi on the device

### Other
- **SimpleAlarmTask**: Set an alarm for a specific time
- **SimpleMessageTask**: Send a text message to a contact

## Task Structure

Each task follows the MobileWorld `BaseTask` interface:

```python
class ExampleTask(BaseTask):
    goal = "Task description that the agent will see"
    task_tags = {"lang-en"}  # or {"lang-cn"} 
    app_names = {"AppName"}
    
    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Setup preconditions for the task"""
        return True
    
    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Verify task completion (0.0 = failure, 1.0 = success)"""
        return 1.0, "Success message"
```

## Adding New Tasks

1. Create a new `.py` file in this directory or an appropriate subdirectory
2. Define a class that inherits from `BaseTask`
3. Implement required attributes: `goal`, `app_names`, `task_tags`
4. Implement `initialize_task_hook()` and `is_successful()` methods
5. The task will be automatically discovered and registered

See the [Android World Integration Guide](../../../docs/android_world_integration.md) for detailed instructions.

## Running Android World Tasks

```bash
# List all android_world tasks
mw info task --suite-family android_world

# Run evaluation with android_world tasks
sudo mw eval \
    --agent_type qwen3vl \
    --task ALL \
    --suite-family android_world \
    --model_name [your_model] \
    --llm_base_url [your_url]
```

## Task Categories

Tasks are organized into categories matching common Android functionality:

- **contacts/**: Contact management tasks
- **settings/**: Device settings tasks
- **Root level**: Other general tasks (alarms, messages, etc.)

You can add more categories as needed by creating new subdirectories.

## Verification Methods

Android World tasks can use various verification methods:

1. **ADB Commands**: Query device state directly
   ```python
   # Example: Check WiFi state
   result = controller.execute_adb_command("settings get global wifi_on")
   ```

2. **Content Providers**: Query Android databases
   ```python
   # Example: Check contacts
   result = controller.execute_adb_command("content query --uri content://contacts/...")
   ```

3. **UI Inspection**: Analyze current screen state
   ```python
   # Example: Check for UI elements
   xml = controller.get_xml()
   ```

4. **User Confirmation**: Rely on agent's "finished" action
   ```python
   answer = controller.interaction_cache
   if "finished" in str(answer).lower():
       return 1.0, "Success"
   ```

## Integration Notes

- These tasks use the same `BaseTask` interface as MobileWorld tasks
- They can be run on the same Android emulator (Pixel_8_API_34_x86_64)
- Task registry automatically discovers and loads them when `suite_family="android_world"`
- All MobileWorld infrastructure (logging, evaluation, visualization) works with android_world tasks

## Contributing

When contributing new Android World tasks:

1. **Follow naming conventions**: Use descriptive PascalCase names ending with "Task"
2. **Add docstrings**: Explain what the task does
3. **Implement robust verification**: Don't just check for "finished", verify actual state
4. **Test thoroughly**: Ensure tasks can be completed and verified correctly
5. **Document edge cases**: Note any special requirements or limitations

## References

- [Android World (Google Research)](https://github.com/google-research/android_world)
- [MobileWorld Documentation](../../../docs/)
- [BaseTask API](../../base.py)
