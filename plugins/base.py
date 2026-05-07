"""
DevDesk Plugin Base Template
Use this as a starting point for creating your own plugins
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DevDeskPlugin(ABC):
    """Base class for all DevDesk plugins"""
    
    # Plugin metadata (override in subclass)
    name: str = "Plugin"
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = "A DevDesk plugin"
    
    def __init__(self):
        """Initialize the plugin"""
        self.enabled = True
    
    @abstractmethod
    async def get_data(self) -> Dict[str, Any]:
        """
        Fetch data for the plugin
        
        Returns:
            dict: Data to be sent to frontend
        """
        pass
    
    @abstractmethod
    def get_component_name(self) -> str:
        """
        Get the React component name to render
        
        Returns:
            str: Component name (e.g., "WeatherWidget")
        """
        pass
    
    def on_enable(self):
        """Called when plugin is enabled"""
        self.enabled = True
    
    def on_disable(self):
        """Called when plugin is disabled"""
        self.enabled = False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate plugin configuration
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: True if valid
        """
        return True


class PluginManager:
    """Manages plugin lifecycle and execution"""
    
    def __init__(self):
        """Initialize plugin manager"""
        self.plugins: Dict[str, DevDeskPlugin] = {}
    
    def register(self, plugin: DevDeskPlugin):
        """Register a new plugin"""
        self.plugins[plugin.name] = plugin
        print(f"✅ Plugin registered: {plugin.name} v{plugin.version}")
    
    def unregister(self, name: str):
        """Unregister a plugin"""
        if name in self.plugins:
            del self.plugins[name]
            print(f"❌ Plugin unregistered: {name}")
    
    async def execute_all(self) -> Dict[str, Any]:
        """Execute all enabled plugins and collect data"""
        results = {}
        for name, plugin in self.plugins.items():
            if plugin.enabled:
                try:
                    data = await plugin.get_data()
                    results[name] = {
                        "data": data,
                        "component": plugin.get_component_name()
                    }
                except Exception as e:
                    print(f"❌ Error executing plugin {name}: {e}")
        return results
