"""
Calculator Widget for QGIS Plugin
Provides the UI and functionality for the calculator panel
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
    QLineEdit, QLabel, QListWidget, QListWidgetItem, QSplitter
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
import math
from .help_window import HelpWindow


class CalculatorWidget(QWidget):
    """Main calculator widget that displays as a dockable panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expression = ""
        self.advanced_mode = False
        self.help_window = None
        self.history = []  # Store calculation history
        self.max_history = 966  # Maximum history items to keep
        self.init_ui()
        # Set focus to receive keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Calculator")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        self.main_layout.addWidget(title)
        
        # History panel (right under title)
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(0, 5, 0, 5)
        
        history_title = QLabel("History")
        history_title_font = QFont()
        history_title_font.setPointSize(9)
        history_title_font.setBold(True)
        history_title.setFont(history_title_font)
        history_layout.addWidget(history_title)
        
        # History list widget
        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(100)
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        history_layout.addWidget(self.history_list)
        
        # Clear history button
        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setMinimumHeight(20)
        clear_history_btn.setMaximumHeight(22)
        clear_history_btn.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_history_btn)
        
        self.main_layout.addLayout(history_layout)
        
        # Mode button layout
        mode_layout = QHBoxLayout()
        self.mode_button = QPushButton("Advanced Calculator")
        self.mode_button.clicked.connect(self.toggle_mode)
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help)
        mode_layout.addStretch()
        mode_layout.addWidget(self.mode_button)
        mode_layout.addWidget(help_button)
        self.main_layout.addLayout(mode_layout)
        
        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        display_font = QFont()
        display_font.setPointSize(14)
        self.display.setFont(display_font)
        self.display.setMinimumHeight(50)
        self.display.setText("0")
        self.main_layout.addWidget(self.display)
        
        # Copy button
        copy_btn = QPushButton("Copy")
        copy_btn.setMaximumHeight(22)
        copy_btn.setMinimumHeight(20)
        copy_btn.clicked.connect(self.copy_to_clipboard)
        self.main_layout.addWidget(copy_btn)
        
        # Calculator buttons
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout()
        self.button_container.setLayout(self.button_layout)
        self.main_layout.addWidget(self.button_container)
        
        # Create simple calculator buttons
        self.create_simple_buttons()
        
        self.setLayout(self.main_layout)
    
    def create_simple_buttons(self):
        """Create simple calculator buttons"""
        # Clear previous layout
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        
        # Button grid layout
        grid = QGridLayout()
        grid.setSpacing(5)
        
        # Define buttons: (text, row, col, rowspan, colspan)
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("C", 4, 0, 1, 2), ("DEL", 4, 2, 1, 2),
        ]
        
        for button_data in buttons:
            text = button_data[0]
            row = button_data[1]
            col = button_data[2]
            rowspan = button_data[3] if len(button_data) > 3 else 1
            colspan = button_data[4] if len(button_data) > 4 else 1
            
            btn = QPushButton(text)
            btn.setMinimumHeight(45)
            btn_font = QFont()
            btn_font.setPointSize(12)
            btn.setFont(btn_font)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            
            # Style operator buttons differently
            if text in "+-*/" and text != "C" and text != "DEL":
                btn.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold;")
            elif text == "=":
                btn.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
            elif text in ["C", "DEL"]:
                btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
            
            grid.addWidget(btn, row, col, rowspan, colspan)
        
        self.button_layout.addLayout(grid)
    
    def create_advanced_buttons(self):
        """Create advanced calculator buttons"""
        # Clear previous layout
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        
        # Main grid layout
        grid = QGridLayout()
        grid.setSpacing(5)
        
        # Define advanced buttons
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3), ("√", 0, 4),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3), ("x²", 1, 4),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3), ("x³", 2, 4),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3), ("%", 3, 4),
            ("sin", 4, 0), ("cos", 4, 1), ("tan", 4, 2), ("log", 4, 3), ("ln", 4, 4),
            ("(", 5, 0), (")", 5, 1), ("x!", 5, 2), ("^", 5, 3), ("e", 5, 4),
            ("C", 6, 0, 1, 2), ("DEL", 6, 2, 1, 3),
        ]
        
        for button_data in buttons:
            text = button_data[0]
            row = button_data[1]
            col = button_data[2]
            rowspan = button_data[3] if len(button_data) > 3 else 1
            colspan = button_data[4] if len(button_data) > 4 else 1
            
            btn = QPushButton(text)
            btn.setMinimumHeight(45)
            btn_font = QFont()
            btn_font.setPointSize(11)
            btn.setFont(btn_font)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            
            # Style buttons differently based on type
            if text in "+-*/^":
                btn.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold;")
            elif text == "=":
                btn.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
            elif text in ["C", "DEL"]:
                btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
            elif text in ["√", "x²", "x³", "sin", "cos", "tan", "log", "ln", "x!", "π", "e", "%"]:
                btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
            elif text in ["(", ")"]:
                btn.setStyleSheet("background-color: #9c27b0; color: white; font-weight: bold;")
            
            grid.addWidget(btn, row, col, rowspan, colspan)
        
        self.button_layout.addLayout(grid)
    
    def toggle_mode(self):
        """Toggle between simple and advanced mode"""
        self.advanced_mode = not self.advanced_mode
        
        if self.advanced_mode:
            self.mode_button.setText("Simple Calculator")
            self.create_advanced_buttons()
        else:
            self.mode_button.setText("Advanced Calculator")
            self.create_simple_buttons()
    
    def _clear_layout(self, layout):
        """Recursively clear a layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
    
    def show_help(self):
        """Open the help window"""
        if self.help_window is None:
            self.help_window = HelpWindow(self)
        self.help_window.exec_()
    
    def safe_eval(self, expression):
        """Safely evaluate mathematical expression"""
        try:
            # Replace mathematical constants and functions
            expression = expression.replace("π", str(math.pi))
            expression = expression.replace("e", str(math.e))
            expression = expression.replace("√", "math.sqrt")
            expression = expression.replace("x²", "**2")
            expression = expression.replace("x³", "**3")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log10")
            expression = expression.replace("ln", "math.log")
            expression = expression.replace("^", "**")
            expression = expression.replace("%", "/100")  # Convert % to division by 100
            
            # For factorial, we need special handling
            import re
            # Find factorial patterns like "5!"
            def factorial_replace(match):
                num = match.group(1)
                return f"math.factorial({num})"
            expression = re.sub(r'(\d+)!', factorial_replace, expression)
            
            result = eval(expression)
            # Convert to float to ensure consistent formatting
            result = float(result)
            
            # Format the result to avoid scientific notation completely
            # This prevents issues with 'e' in numbers conflicting with Euler's number 'e'
            if result == 0:
                return "0.0"
            
            # Use Decimal for better precision with very small numbers
            from decimal import Decimal
            decimal_result = Decimal(str(result))
            
            # Format without scientific notation
            # Use enough decimal places to represent the number accurately
            if abs(result) < 1e-6:
                # For very small numbers, use more decimal places
                formatted = f"{result:.15f}".rstrip('0').rstrip('.')
            else:
                # For normal numbers, use up to 10 decimal places
                formatted = f"{result:.10f}".rstrip('0').rstrip('.')
            
            # Ensure we have at least one decimal place for consistency
            if '.' not in formatted:
                formatted += '.0'
            
            return formatted
        except Exception as e:
            return "Error"
    
    def on_button_click(self, text):
        """Handle button clicks"""
        current = self.display.text()
        
        if text == "C":
            # Clear
            self.expression = ""
            self.display.setText("0")
        elif text == "DEL":
            # Delete last character
            if current != "0":
                current = current[:-1]
                self.display.setText(current if current else "0")
                self.expression = current if current != "0" else ""
        elif text == "=":
            # Calculate result
            result = self.safe_eval(current)
            self.display.setText(result)
            self.expression = result
            # Add to history if calculation was successful
            if result != "Error" and current != "":
                self.add_to_history(current, result)
        elif text in ["sin", "cos", "tan", "log", "ln"]:
            # Trigonometric and logarithmic functions
            if current == "0":
                self.display.setText(text + "(")
            else:
                self.display.setText(current + text + "(")
            self.expression = self.display.text()
        elif text == "√":
            # Square root
            if current == "0":
                self.display.setText("√(")
            else:
                self.display.setText(current + "√(")
            self.expression = self.display.text()
        elif text == "x²":
            # Square
            self.display.setText(current + "x²")
            self.expression = self.display.text()
        elif text == "x³":
            # Cube
            self.display.setText(current + "x³")
            self.expression = self.display.text()
        elif text == "x!":
            # Factorial
            self.display.setText(current + "!")
            self.expression = self.display.text()
        elif text == "^":
            # Power
            self.display.setText(current + "^")
            self.expression = self.display.text()
        elif text == "π":
            # Pi
            if current == "0":
                self.display.setText("π")
            else:
                self.display.setText(current + "π")
            self.expression = self.display.text()
        elif text == "e":
            # Euler's number
            if current == "0":
                self.display.setText("e")
            else:
                self.display.setText(current + "e")
            self.expression = self.display.text()
        elif text == "%":
            # Percentage - divide by 100
            self.display.setText(current + "%")
            self.expression = self.display.text()
        elif text in "+-*/.^()":
            # Operators and parentheses
            if current == "0" and text not in "().":
                self.display.setText(text)
            else:
                self.display.setText(current + text)
            self.expression = self.display.text()
        else:
            # Number
            if current == "0":
                self.display.setText(text)
            else:
                self.display.setText(current + text)
            self.expression = self.display.text()
    
    def keyPressEvent(self, event):
        """Handle keyboard input for the calculator"""
        key = event.key()
        text = event.text()
        
        # Handle numbers 0-9
        if text.isdigit():
            self.on_button_click(text)
        # Handle operators
        elif text in "+-*/()":
            self.on_button_click(text)
        # Handle decimal point
        elif text == ".":
            self.on_button_click(".")
        # Handle equals with Enter or =
        elif key == Qt.Key_Return or key == Qt.Key_Equal or text == "=":
            self.on_button_click("=")
        # Handle backspace for delete
        elif key == Qt.Key_Backspace:
            self.on_button_click("DEL")
        # Handle Escape for clear
        elif key == Qt.Key_Escape:
            self.on_button_click("C")
        # Handle ^ for power
        elif text == "^":
            self.on_button_click("^")
        # For shift+8 (asterisk on some keyboards)
        elif text == "*":
            self.on_button_click("*")
        # For forward slash
        elif text == "/":
            self.on_button_click("/")
        else:
            super().keyPressEvent(event)
    
    def add_to_history(self, expression, result):
        """Add a calculation to the history"""
        history_item = f"{expression} = {result}"
        self.history.append((expression, result))
        
        # Keep only the last max_history items
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        # Update the history list widget
        self.update_history_display()
    
    def update_history_display(self):
        """Update the history list widget display"""
        self.history_list.clear()
        # Add items in reverse order (most recent first)
        for expr, result in reversed(self.history):
            item_text = f"{expr}\n= {result}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (expr, result))  # Store the data
            self.history_list.addItem(item)
    
    def on_history_item_clicked(self, item):
        """Handle clicking on a history item to reload it"""
        expr, result = item.data(Qt.UserRole)
        # Set the display to show the result
        self.display.setText(result)
        self.expression = result
    
    def clear_history(self):
        """Clear the calculation history"""
        self.history.clear()
        self.history_list.clear()
    
    def copy_to_clipboard(self):
        """Copy the current display value to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.display.text())
