"""
QGIS Plugin Package Initialization
This module initializes ORCA (On-the-flyReadyCalculatorAdd-on)
"""

from .qgis_calculator_plugin import QgisCalculatorPlugin


def classFactory(iface):
    """
    Load the plugin and return the plugin class
    
    Args:
        iface: QGIS interface object
        
    Returns:
        The plugin class instance
    """
    return QgisCalculatorPlugin(iface)
