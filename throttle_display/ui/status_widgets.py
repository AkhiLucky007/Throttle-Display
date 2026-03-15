"""
Status Widgets Module
Reusable UI components for displaying system status
"""
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class OverspeedIndicator(QWidget):
    """
    Blinking overspeed warning indicator
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.dot = QWidget()
        self.dot.setFixedSize(10, 10)
        self.dot.setStyleSheet(
            "background-color: transparent; border-radius: 5px;"
        )

        self.label = QLabel("Overspeed Warning")
        self.label.setStyleSheet(
            "color: #ef4444; font-size: 12px; font-weight: 600;"
        )
        self.label.hide()

        layout.addWidget(self.dot)
        layout.addWidget(self.label)

        self._blink_on = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._toggle)

    def _toggle(self):
        self._blink_on = not self._blink_on
        color = "#ef4444" if self._blink_on else "transparent"
        self.dot.setStyleSheet(
            f"background-color: {color}; border-radius: 5px;"
        )

    def set_active(self, active: bool):
        if active:
            self.label.show()
            if not self.timer.isActive():
                self.timer.start(400)
        else:
            self.timer.stop()
            self.dot.setStyleSheet(
                "background-color: transparent; border-radius: 5px;"
            )
            self.label.hide()



class StateIndicator(QLabel):
    """
    Large, prominent state display (DISABLED / READY / FAULT)
    Features color-coded styling and smooth animations
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("StateLabel")
        self.setProperty("class", "StateLabel")
        self._state = "DISABLED"
        self.update_state("DISABLED")
        
    def update_state(self, state: str):
        """
        Update displayed state
        
        Args:
            state: One of "DISABLED", "READY", "FAULT"
        """
        self._state = state
        self.setText(state)
        self.setProperty("state", state)
        
        # Force style update
        self.style().unpolish(self)
        self.style().polish(self)
        
    @pyqtProperty(str)
    def state(self):
        return self._state


class ValueDisplay(QLabel):
    """
    Large numeric value display (for throttle percentage)
    """
    
    def __init__(self, suffix="", parent=None):
        super().__init__(parent)
        self.suffix = suffix
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("ValueLabel")
        self.setProperty("class", "ValueLabel")
        self.update_value(0.0)
        
    def update_value(self, value: float):
        """
        Update displayed value
        
        Args:
            value: Numeric value to display
        """
        # Color-code based on value
        if value > 70:
            color = "#ef4444"  # Red
        elif value > 60:
            color = "#f59e0b"  # Orange/Yellow
        else:
            color = "#3b82f6"  # Blue
            
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 56px;
                font-weight: 700;
                letter-spacing: -2px;
            }}
        """)
        
        self.setText(f"{value:.1f}{self.suffix}")


class StatusIndicator(QWidget):
    """
    Small status indicator with label (e.g., "Connected", "Enabled")
    Shows colored dot + text
    """
    
    def __init__(self, label: str, parent=None):
        super().__init__(parent)
        self.label_text = label
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        
        # Indicator dot
        self.dot = QWidget()
        self.dot.setFixedSize(10, 10)
        self.dot.setProperty("class", "Indicator")
        
        # Label
        self.label = QLabel(label)
        self.label.setStyleSheet("color: #9ca3af; font-size: 12px;")
        
        layout.addWidget(self.dot)
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.set_active(False)
        
    def set_active(self, active: bool):
        """
        Set indicator state
        
        Args:
            active: True for active/connected, False for inactive
        """
        if active:
            self.dot.setStyleSheet("""
                QWidget {
                    background-color: #22c55e;
                    border-radius: 5px;
                }
            """)
            self.label.setStyleSheet("color: #22c55e; font-size: 12px; font-weight: 600;")
        else:
            self.dot.setStyleSheet("""
                QWidget {
                    background-color: #6b7280;
                    border-radius: 5px;
                }
            """)
            self.label.setStyleSheet("color: #6b7280; font-size: 12px;")


class SectionLabel(QLabel):
    """
    Section header label with consistent styling
    """
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "SectionHeader")
        self.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                padding: 8px 0 4px 0;
            }
        """)
