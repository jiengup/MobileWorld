# Android World Integration Guide

## Overview

MobileWorld now supports **Android World** as an alternative benchmark suite alongside the default Mobile World tasks. Android World is integrated as a separate suite family that can be selected when running evaluations.

## Architecture

The integration adds Android World as a separate task suite through the `suite_family` parameter:

- **mobile_world** (default): Original MobileWorld benchmark tasks (201 tasks across 20 applications)
- **android_world**: Android World benchmark tasks (currently 5 sample tasks, expandable)

## Task Structure

Android World tasks are located in:
```
src/mobile_world/tasks/definitions/android_world/
├── __init__.py
├── contacts/
│   ├── __init__.py
│   └── simple_contact_task.py
├── settings/
│   ├── __init__.py
│   ├── brightness_task.py
│   └── wifi_enable_task.py
├── simple_alarm_task.py
└── simple_message_task.py
```

## Usage

### Listing Android World Tasks

```bash
mw info task --suite-family android_world
```

### Running Android World Evaluation

```bash
# Launch environment
sudo mw env run --count 1

# Run evaluation with android_world suite
sudo mw eval \
    --agent_type qwen3vl \
    --task ALL \
    --suite-family android_world \
    --model_name Qwen3-VL-235B-A22B \
    --llm_base_url [your_api_url] \
    --log_file_root traj_logs/android_world_logs
```

### Starting Server with Android World

```bash
mw server --suite-family android_world --port 6800
```

### Switching Suite Families at Runtime

The suite family can be switched dynamically via the API:

```python
from mobile_world.runtime.client import AndroidEnvClient

client = AndroidEnvClient(url="http://localhost:6800")
client.switch_suite_family("android_world")
```

Or via the API endpoint:
```bash
curl -X POST "http://localhost:6800/suite_family/switch?target_family=android_world"
```

## Adding New Android World Tasks

### Step 1: Create Task File

Create a new Python file in the appropriate category directory (or at the root):

```python
# src/mobile_world/tasks/definitions/android_world/my_category/my_task.py

from loguru import logger
from mobile_world.runtime.controller import AndroidController
from mobile_world.tasks.base import BaseTask


class MyAndroidWorldTask(BaseTask):
    """Description of your task."""

    goal = "Your task instruction here"
    
    task_tags = {"lang-en"}  # or {"lang-cn"} for Chinese
    
    app_names = {"AppName"}  # Android app(s) used

    def initialize_task_hook(self, controller: AndroidController) -> bool:
        """Initialize the task (setup preconditions)."""
        logger.info("Initializing MyAndroidWorldTask")
        # Setup code here
        return True

    def is_successful(self, controller: AndroidController) -> float | tuple[float, str]:
        """Verify task completion."""
        self._check_is_initialized()
        
        # Verification logic here
        # Return (1.0, "Success message") or (0.0, "Failure message")
        answer = controller.interaction_cache
        if "expected_value" in str(answer):
            return 1.0, "Task completed successfully"
        else:
            return 0.0, "Task not completed"
```

### Step 2: Task Registry Auto-Discovery

Tasks are automatically discovered and registered by the `TaskRegistry` when:
- They inherit from `BaseTask`
- They are in a `.py` file under `android_world/`
- They define required attributes: `goal`, `app_names`, `task_tags`

No manual registration needed!

### Step 3: Verify Task

List tasks to verify your new task is loaded:
```bash
mw info task --suite-family android_world --filter MyAndroidWorldTask
```

## Sample Tasks Included

The integration includes 5 sample Android World tasks:

1. **SimpleContactTask** - Create a new contact
2. **SimpleAlarmTask** - Set an alarm
3. **SimpleMessageTask** - Send a text message
4. **WifiEnableTask** - Turn on WiFi
5. **BrightnessTask** - Adjust screen brightness

These serve as templates for creating more comprehensive Android World tasks.

## Implementation Details

### TaskRegistry Changes

The `TaskRegistry` class now accepts a `suite_family` parameter:

```python
TaskRegistry(suite_family="android_world")
```

This automatically loads tasks from the correct directory:
- `mobile_world`: `src/mobile_world/tasks/definitions/`
- `android_world`: `src/mobile_world/tasks/definitions/android_world/`

### AVD Configuration

Both suite families currently use the same Android Virtual Device:
- AVD: `Pixel_8_API_34_x86_64`

To use a different AVD for Android World, modify `AVD_MAPPING` in `src/mobile_world/core/server.py`:

```python
AVD_MAPPING: dict[str, str] = {
    "mobile_world": "Pixel_8_API_34_x86_64",
    "android_world": "Your_Custom_AVD_Name",
}
```

### CLI Changes

All relevant CLI commands now support `--suite-family` argument:
- `mw info task --suite-family android_world`
- `mw info app --suite-family android_world`
- `mw eval --suite-family android_world`
- `mw server --suite-family android_world`

## Migrating from Google's Android World

To integrate tasks from Google's Android World repository:

1. Study the original task structure from https://github.com/google-research/android_world
2. Create equivalent task classes that inherit from `BaseTask`
3. Implement `initialize_task_hook()` for task setup
4. Implement `is_successful()` for verification
5. Place tasks in appropriate category subdirectories

## Future Enhancements

Possible future improvements:
- Add more Android World tasks based on the official benchmark
- Support loading tasks from the `third-party/android_world` directory
- Custom evaluation metrics specific to Android World
- Dedicated AVD configurations for different task types

## Troubleshooting

### Tasks Not Loading

Check the task file location:
```bash
find src/mobile_world/tasks/definitions/android_world -name "*.py"
```

Verify task class inherits from BaseTask:
```python
class MyTask(BaseTask):  # ✓ Correct
    ...

class MyTask:  # ✗ Wrong - won't be discovered
    ...
```

### Suite Family Not Found

Ensure the suite family is in the allowed choices:
- Valid: `mobile_world`, `android_world`
- Invalid: Any other value

### AVD Not Starting

Check the AVD name in `AVD_MAPPING` matches an existing AVD:
```bash
# In the Docker container
emulator -list-avds
```

## Contributing

When adding new Android World tasks:
1. Follow the existing task structure
2. Use descriptive task names (e.g., `CreateContactWithPhotoTask`)
3. Add comprehensive docstrings
4. Implement robust verification logic
5. Test with actual device/emulator

## References

- [Android World (Google Research)](https://github.com/google-research/android_world)
- [MobileWorld Paper](https://arxiv.org/abs/2512.19432)
- [BaseTask API Documentation](../src/mobile_world/tasks/base.py)
