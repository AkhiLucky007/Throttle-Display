"""
Main Window Module
Primary application window with data integration
"""
import logging
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon
from ui.dashboard_layout import DashboardLayout
from core.data_model import ThrottleData
from core.state_machine import StateMachine

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window
    Integrates data sources with UI components
    """
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.setWindowTitle("Throttle Display")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Data source (will be set externally)
        self.data_source = None
        
        # State machine
        self.state_machine = StateMachine(fault_threshold=70.0)
        
        # UI update timer
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self._update_ui_state)
        
        # Latest data
        self.latest_data = None

        # UI decay handling when disabled
        self._ui_display_value = 0.0
        self._decay_rate = 2.0  # percent per UI tick

        
        # Setup UI
        self._create_ui()
        self._apply_theme()
        
        logger.info("Main window initialized")
        
    def _create_ui(self):
        """Create and setup UI components"""
        # Create dashboard layout
        self.dashboard = DashboardLayout()
        self.setCentralWidget(self.dashboard)
        
    def _apply_theme(self):
        """Load and apply the premium dark theme"""
        theme_path = Path("assets/theme.qss")
        
        if theme_path.exists():
            try:
                with open(theme_path, 'r') as f:
                    stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                logger.info("Theme applied successfully")
            except Exception as e:
                logger.warning(f"Could not load theme: {e}")
        else:
            logger.warning("Theme file not found, using default styling")
            
    def set_data_source(self, data_source):
        """
        Connect a data source to the dashboard
        
        Args:
            data_source: Object with data_received and connection_status signals
                        (SerialComm, WiFiComm, or DataSimulator)
        """
        self.data_source = data_source
        
        # Connect signals
        data_source.data_received.connect(self._on_data_received)
        data_source.connection_status.connect(self._on_connection_status)
        
        # Start data source
        if hasattr(data_source, 'start'):
            data_source.start()
            logger.info("Data source started")
        
        # Start UI update timer (20 Hz)
        self.ui_timer.start(50)
      
    def _on_connection_status(self, connected: bool, message: str):
        """
        Handle connection status updates

        Args:
            connected: True if connected, False otherwise
            message: Status message
        """
        logger.info(f"Connection status: {message}")

        # Update connection indicator
        if self.dashboard.connection_indicator:
            self.dashboard.connection_indicator.set_active(connected)
            self.dashboard.connection_indicator.label.setText(message)


    def _on_data_received(self, packet: dict):
        """
        Handle incoming data packet.

        Supports BOTH formats:

        Mock / Hardware format  (MOCK_Data.py):
            {"system": "enabled", "throttle": 72.3, "fault": "more"}

        Simulator / legacy format:
            {"enabled": true, "throttle_pct": 72.3, "state": "ENABLED"}
        """
        try:
            if "system" in packet:
                # ── Real mock / hardware format ──────────────────────
                raw_system   = str(packet.get("system", "disabled"))
                throttle_pct = float(packet.get("throttle", 0.0))
                enabled      = (raw_system.lower() == "enabled")
                state_str    = "ENABLED" if enabled else "DISABLED"
                # ADC not supplied by mock — back-calculate from percentage
                adc_value    = int((throttle_pct / 100.0) * 4095)
            else:
                # ── Simulator / legacy format ────────────────────────
                throttle_pct = float(packet.get("throttle_pct", 0.0))
                adc_value    = int(packet.get("throttle_adc", 0))
                enabled      = bool(packet.get("enabled", False))
                state_str    = str(packet.get("state", "DISABLED"))

            self.latest_data = ThrottleData(
                throttle_pct=throttle_pct,
                throttle_adc=adc_value,
                enabled=enabled,
                state=state_str
            )

            self.state_machine.update(throttle_pct, enabled)

        except Exception as e:
            logger.error(f"Error processing data packet: {e}")
            
    def _update_ui_state(self):
        if self.latest_data is None:
            return

        if self.latest_data.enabled:
            self._ui_display_value = self.latest_data.throttle_pct
        else:
            if self._ui_display_value > 0:
                self._ui_display_value = max(
                    0.0,
                    self._ui_display_value - self._decay_rate
                )
            else:
                self._ui_display_value = 0.0

        # ── Value display ─────────────────────────
        self.dashboard.value_display.update_value(self._ui_display_value)

        # ── Overspeed indicator (HERE) ────────────
        if hasattr(self.dashboard, "overspeed_indicator"):
            self.dashboard.overspeed_indicator.set_active(
                self._ui_display_value > 70
            )

        # ── State / status updates ─────────────────
        self.dashboard.state_indicator.update_state(self.latest_data.state)
        self.dashboard.enabled_indicator.set_active(self.latest_data.enabled)

        # ── Plot ──────────────────────────────────
        self.dashboard.plot_widget.add_data_point(self._ui_display_value)

    def closeEvent(self, event):
        """Handle window close event"""
        logger.info("Application closing")
        
        # Stop data source
        if self.data_source and hasattr(self.data_source, 'stop'):
            self.data_source.stop()
            
        # Stop timers
        self.ui_timer.stop()
        
        event.accept()
