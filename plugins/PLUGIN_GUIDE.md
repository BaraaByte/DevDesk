# DevDesk Plugin Setup Guide

## Creating Your First Plugin

### 1. Understand the Plugin Structure

All plugins inherit from `DevDeskPlugin` and must implement:
- `get_data()` - Fetch data asynchronously
- `get_component_name()` - Return React component name

### 2. Basic Plugin Template

```python
from plugins.base import DevDeskPlugin
from typing import Dict, Any

class MyPlugin(DevDeskPlugin):
    name = "My Plugin"
    version = "1.0.0"
    author = "Your Name"
    description = "What my plugin does"
    
    async def get_data(self) -> Dict[str, Any]:
        # Fetch and return data
        return {"message": "Hello from my plugin"}
    
    def get_component_name(self) -> str:
        return "MyPluginWidget"
```

### 3. Register Your Plugin

In the backend `main.py`:

```python
from plugins.my_plugin import MyPlugin
from plugins.base import PluginManager

plugin_manager = PluginManager()
plugin_manager.register(MyPlugin())
```

### 4. Create the React Component

In `frontend/src/components/plugins/MyPluginWidget.tsx`:

```tsx
export default function MyPluginWidget({ data, isDark }) {
  return (
    <div>
      <h3>My Plugin</h3>
      <p>{data.message}</p>
    </div>
  )
}
```

## Plugin Examples

### Weather Widget
See `weather_example.py` for a complete weather plugin example

### Next Steps
1. Fork the repository
2. Create your plugin
3. Submit a pull request to share it with the community!

## Plugin Best Practices

- Handle errors gracefully
- Use async/await for I/O operations
- Cache data when possible
- Validate configuration input
- Add logging for debugging
- Document your plugin's configuration options
