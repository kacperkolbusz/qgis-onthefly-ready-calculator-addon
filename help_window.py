"""
Help Window for QGIS Calculator Plugin
Displays detailed information about all calculator operations and functions
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, 
    QPushButton, QWidget, QTabWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt as QtCore


class HelpWindow(QDialog):
    """Help window that explains all calculator operations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ORCA - Help & Operations Guide")
        self.setGeometry(100, 100, 700, 600)
        self.setModal(False)  # Allow window to be non-modal for better resizing
        self.init_ui()
    
    def init_ui(self):
        """Initialize the help window UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("ORCA (On-the-flyReadyCalculatorAdd-on) - Help & Operations Guide")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Create tab widget for different sections
        tabs = QTabWidget()
        
        # Simple Calculator Tab
        tabs.addTab(self.create_simple_operations_widget(), "Simple Operations")
        
        # Advanced Calculator Tab
        tabs.addTab(self.create_advanced_operations_widget(), "Advanced Operations")
        
        # Tips Tab
        tabs.addTab(self.create_tips_widget(), "Tips & Tricks")
        
        # About Tab
        tabs.addTab(self.create_about_widget(), "About")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setMinimumSize(500, 400)  # Set minimum size to prevent too small windows
    
    def create_about_widget(self):
        """Create about widget with plugin information"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # About content
        about_text = QLabel(
            "<b>QGIS Calculator v1.0.0</b><br><br>"
            "A lightweight, efficient calculator plugin for QGIS.<br><br>"
            "<b>Features:</b><br>"
            "• Simple & Advanced modes<br>"
            "• Keyboard & mouse input<br>"
            "• Calculation history<br>"
            "• Trigonometric & scientific functions<br>"
            "• Dockable panel interface<br><br>"
            "<b>Usage:</b><br>"
            "Click the calculator icon in the toolbar, or access via "
            "Plugins → ORCA<br><br>"
            "For detailed help, see the other tabs or press Help button.<br><br>"
            "<b>Questions, suggestions? Contact me:</b> kk.at.work@pm.me"
        )
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(about_text)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_simple_operations_widget(self):
        """Create widget with simple operations help"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        operations = [
            ("Addition (+)", "Adds two numbers together.\nExample: 5 + 3 = 8"),
            ("Subtraction (-)", "Subtracts the second number from the first.\nExample: 10 - 4 = 6"),
            ("Multiplication (*)", "Multiplies two numbers together.\nExample: 7 * 6 = 42"),
            ("Division (/)", "Divides the first number by the second.\nExample: 20 / 4 = 5"),
            ("Decimal Point (.)", "Allows you to use decimal numbers.\nExample: 5.5 + 2.3 = 7.8"),
            ("Clear (C)", "Clears the display and resets the calculator to 0."),
            ("Delete (DEL)", "Deletes the last digit from the current input."),
            ("Equals (=)", "Calculates and displays the result of your expression."),
        ]
        
        for op_name, op_desc in operations:
            frame = self.create_operation_frame(op_name, op_desc)
            layout.addWidget(frame)
        
        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)
        return widget
    
    def create_advanced_operations_widget(self):
        """Create widget with advanced operations help"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        operations = [
            ("Square Root (√)", "Calculates the square root of a number.\nExample: √(16) = 4\nUsage: √(number)"),
            ("Square (x²)", "Raises a number to the power of 2.\nExample: 5x² = 25"),
            ("Cube (x³)", "Raises a number to the power of 3.\nExample: 3x³ = 27"),
            ("Power (^)", "Raises a number to any power.\nExample: 2^8 = 256\nUsage: base^exponent"),
            ("Sine (sin)", "Trigonometric sine function. Uses radians.\nExample: sin(0) = 0\nUsage: sin(angle_in_radians)"),
            ("Cosine (cos)", "Trigonometric cosine function. Uses radians.\nExample: cos(0) = 1\nUsage: cos(angle_in_radians)"),
            ("Tangent (tan)", "Trigonometric tangent function. Uses radians.\nExample: tan(0) = 0\nUsage: tan(angle_in_radians)"),
            ("Logarithm (log)", "Base 10 logarithm.\nExample: log(100) = 2\nUsage: log(number)"),
            ("Natural Log (ln)", "Natural logarithm (base e).\nExample: ln(e) = 1\nUsage: ln(number)"),
            ("Factorial (!)", "Multiplies all positive integers up to that number.\nExample: 5! = 120 (5×4×3×2×1)\nUsage: number!"),
            ("Pi (π)", "Mathematical constant π ≈ 3.14159\nExample: 2 * π ≈ 6.28318"),
            ("Euler's Number (e)", "Mathematical constant e ≈ 2.71828\nExample: ln(e) = 1"),
            ("Parentheses ()", "Groups operations to control order of calculation.\nExample: (2 + 3) * 4 = 20 (not 14)"),
        ]
        
        for op_name, op_desc in operations:
            frame = self.create_operation_frame(op_name, op_desc)
            layout.addWidget(frame)
        
        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)
        return widget
    
    def create_tips_widget(self):
        """Create widget with tips and tricks"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        tips_title = QLabel("Tips & Tricks")
        tips_title_font = QFont()
        tips_title_font.setPointSize(12)
        tips_title_font.setBold(True)
        tips_title.setFont(tips_title_font)
        layout.addWidget(tips_title)
        
        tips = [
            ("Order of Operations", 
             "The calculator follows standard math order of operations (PEMDAS):\n"
             "1. Parentheses\n"
             "2. Exponents/Powers\n"
             "3. Multiplication and Division (left to right)\n"
             "4. Addition and Subtraction (left to right)\n\n"
             "Example: 2 + 3 * 4 = 14 (not 20)"),
            
            ("Using Trigonometric Functions",
             "Trigonometric functions (sin, cos, tan) use RADIANS, not degrees.\n"
             "To convert degrees to radians: radians = degrees × π / 180\n\n"
             "Common values:\n"
             "• sin(0) = 0\n"
             "• cos(0) = 1\n"
             "• sin(π/2) ≈ sin(1.5708) = 1"),
            
            ("Parentheses for Complex Expressions",
             "Use parentheses to make complex calculations clear:\n"
             "✓ (5 + 3) * 2 = 16\n"
             "✗ 5 + 3 * 2 = 11 (multiplied first)\n\n"
             "You can nest parentheses: ((2 + 3) * 4) + 1 = 21"),
            
            ("Working with Decimals",
             "The calculator supports decimal numbers:\n"
             "• 5.5 + 2.3 = 7.8\n"
             "• 7.5 / 2.5 = 3.0\n"
             "• √(2.25) = 1.5"),
            
            ("Keyboard Tips",
             "Click buttons with your mouse or use keyboard:\n"
             "• Number keys: 0-9\n"
             "• Operations: + - * /\n"
             "• Decimal: .\n"
             "• Delete: Backspace (DEL)\n"
             "• Clear: C\n"
             "• Calculate: Enter or ="),
            
            ("Mode Switching",
             "Click 'Advanced Calculator' to switch to advanced mode with:\n"
             "• Trigonometric functions\n"
             "• Powers and roots\n"
             "• Logarithms\n"
             "• Factorial\n"
             "• Mathematical constants\n\n"
             "Click 'Simple Calculator' to return to basic operations."),
        ]
        
        for tip_title, tip_content in tips:
            frame = self.create_operation_frame(tip_title, tip_content)
            layout.addWidget(frame)
        
        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)
        return widget
    
    def create_operation_frame(self, title, description):
        """Create a styled frame for an operation"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setLineWidth(1)
        frame.setStyleSheet(
            "QFrame { "
            "background-color: #f5f5f5; "
            "border: 1px solid #ddd; "
            "border-radius: 4px; "
            "padding: 10px; "
            "margin: 5px 0px; "
            "}"
        )
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_font = QFont()
        desc_font.setPointSize(10)
        desc_label.setFont(desc_font)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        frame.setLayout(layout)
        return frame
