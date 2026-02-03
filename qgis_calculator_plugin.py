"""
ORCA (On-the-flyReadyCalculatorAdd-on) Plugin Class
Implements the plugin interface and manages the dockable calculator widget
"""

from PyQt5.QtWidgets import QAction, QDockWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pathlib import Path
from .calculator_widget import CalculatorWidget
from .resources import get_icon_path


class QgisCalculatorPlugin:
    """Main plugin class for QGIS"""
    
    def __init__(self, iface):
        """
        Constructor
        
        Args:
            iface: QGIS interface object
        """
        self.iface = iface
        self.calculator_dock = None
        self.action = None
    
    def initGui(self):
        """
        Initialize the GUI
        Called when the plugin is loaded
        """
        # Create the action
        icon_path = get_icon_path()
        
        # Check if icon exists, if not create a placeholder
        if not Path(icon_path).exists():
            # Create a placeholder icon (1x1 transparent PNG)
            icon = QIcon()
        else:
            icon = QIcon(icon_path)
        
        self.action = QAction(icon, "ORCA", self.iface.mainWindow())
        self.action.triggered.connect(self.toggle_calculator)
        
        # Add action to Plugins menu
        self.iface.addPluginToMenu("&ORCA", self.action)
        self.iface.addToolBarIcon(self.action)
    
    def unload(self):
        """
        Unload the plugin
        Called when the plugin is unloaded
        """
        if self.calculator_dock:
            self.iface.removeDockWidget(self.calculator_dock)
        
        self.iface.removePluginMenu("&ORCA", self.action)
        self.iface.removeToolBarIcon(self.action)
    
    def toggle_calculator(self):
        """
        Toggle the calculator dock widget visibility
        """
        if self.calculator_dock is None:
            self.create_calculator_dock()
        else:
            if self.calculator_dock.isVisible():
                self.calculator_dock.hide()
            else:
                self.calculator_dock.show()
    
    def create_calculator_dock(self):
        """
        Create and add the calculator dock widget
        """
        # Create the dock widget
        self.calculator_dock = QDockWidget("On-the-flyReadyCalculatorAdd-on", self.iface.mainWindow())
        
        # Create the calculator widget
        calculator = CalculatorWidget()
        self.calculator_dock.setWidget(calculator)
        
        # Add the dock to the right side
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.calculator_dock)
