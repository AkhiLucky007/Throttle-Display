"""
Dashboard Layout Module
Main dashboard UI composition
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel
)
from PyQt6.QtCore import Qt

from ui.status_widgets import (
    StateIndicator,
    ValueDisplay,
    StatusIndicator,
    SectionLabel,
    OverspeedIndicator
)
from ui.plot_widget import PlotWidget


class DashboardLayout(QWidget):
    """
    Main dashboard layout
    Organizes all visual components in a premium, clean design
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main components (accessible by parent)
        self.value_display = None
        self.state_indicator = None
        self.plot_widget = None
        self.enabled_indicator = None
        self.connection_indicator = None
        self.overspeed_indicator = None

        self._create_layout()

    def _create_layout(self):
        """Build the complete dashboard layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ── Top section: Metrics cards ─────────────────────────────
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)

        # Throttle percentage card
        throttle_card = self._create_metric_card(
            "THROTTLE POSITION",
            is_value=True
        )
        self.value_display = throttle_card["widget"]

        # State card
        state_card = self._create_metric_card(
            "SYSTEM STATE",
            is_state=True
        )
        self.state_indicator = state_card["widget"]

        metrics_layout.addWidget(throttle_card["container"])
        metrics_layout.addWidget(state_card["container"])

        main_layout.addLayout(metrics_layout)

        # ── Plot section (WITH overspeed indicator) ────────────────
        plot_container = self._create_plot_section()
        main_layout.addWidget(plot_container, stretch=1)

        # ── Bottom status bar ──────────────────────────────────────
        status_bar = self._create_status_bar()
        main_layout.addWidget(status_bar)

    def _create_metric_card(self, title: str, is_value=False, is_state=False):
        """Create a metric display card"""
        container = QFrame()
        container.setObjectName("MetricCard")
        container.setStyleSheet("""
            QFrame#MetricCard {
                background-color: #141b2d;
                border-radius: 12px;
                border: 1px solid #1f2937;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        header = SectionLabel(title)
        layout.addWidget(header)

        if is_value:
            widget = ValueDisplay(suffix=" %")
        elif is_state:
            widget = StateIndicator()
        else:
            widget = QLabel("—")

        layout.addWidget(widget)
        layout.addStretch()

        return {"container": container, "widget": widget}

    def _create_plot_section(self):
        """Create the live plot section (overspeed belongs here)"""
        container = QFrame()
        container.setObjectName("PlotCard")
        container.setStyleSheet("""
            QFrame#PlotCard {
                background-color: #141b2d;
                border-radius: 12px;
                border: 1px solid #1f2937;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Header row
        header_layout = QHBoxLayout()
        header = SectionLabel("LIVE THROTTLE SIGNAL")
        header_layout.addWidget(header)

        # Overspeed indicator aligned to graph area
        self.overspeed_indicator = OverspeedIndicator()
        header_layout.addStretch()
        header_layout.addWidget(self.overspeed_indicator)

        layout.addLayout(header_layout)

        # Plot widget
        self.plot_widget = PlotWidget(history_seconds=6)
        layout.addWidget(self.plot_widget)

        return container

    def _create_status_bar(self):
        """Create bottom status bar with system indicators only"""
        container = QFrame()
        container.setFixedHeight(50)
        container.setStyleSheet("""
            QFrame {
                background-color: #141b2d;
                border-radius: 8px;
                border: 1px solid #1f2937;
            }
        """)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(20)

        self.enabled_indicator = StatusIndicator("System Enabled")
        self.connection_indicator = StatusIndicator("Connection")

        layout.addWidget(self.enabled_indicator)
        layout.addWidget(self.connection_indicator)
        layout.addStretch()

        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #4b5563; font-size: 11px;")
        layout.addWidget(version_label)

        return container
