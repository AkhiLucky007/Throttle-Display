"""
Throttle Dashboard - Main Entry Point
Premium real-time embedded systems monitoring dashboard
"""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from comms.data_simulator import DataSimulator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and run the dashboard application"""
    
    # Create logs directory if it doesn't exist
    Path('logs').mkdir(exist_ok=True)
    
    logger.info("Starting Throttle Dashboard Application")
    
    # Enable high DPI scaling for crisp UI on modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application instance
    app = QApplication(sys.argv)
    app.setApplicationName("Throttle Dashboard")
    app.setOrganizationName("EmbeddedSystems")
    
    # Create and configure main window
    window = MainWindow()
    
    # For development/demo: Use data simulator
    # In production: Replace with SerialComm or WiFiComm
    simulator = DataSimulator()
    window.set_data_source(simulator)
    
    # Show the window
    window.show()
    
    logger.info("Application window displayed")
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
