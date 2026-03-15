"""
Plot Widget Module
Real-time throttle percentage plotting
"""
import pyqtgraph as pg
from collections import deque
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer



class PlotWidget(pg.PlotWidget):
    """
    Custom plot widget for displaying live throttle data
    Features smooth scrolling and color-coded zones
    """
    
    def __init__(self, history_seconds=10, update_rate_ms=50):
        """
        Initialize plot widget
        
        Args:
            history_seconds: How many seconds of data to display
            update_rate_ms: UI update rate in milliseconds
        """
        super().__init__()
        
        self.history_seconds = history_seconds

        # Calculate buffer size
        self.max_points = int((history_seconds * 1000) / update_rate_ms)
        
        # Data buffers (using deque for efficient append/pop)
        self.time_data = deque(maxlen=self.max_points)
        self.throttle_data = deque(maxlen=self.max_points)
        self.time_counter = 0
        
        # Configure plot appearance
        self._setup_plot_style()
        
        # Create plot curve
        self.curve = self.plot(
            pen=pg.mkPen(color='#3b82f6', width=2.5),
            name='Throttle %'
        )
        
        # Add threshold lines
        self._add_threshold_lines()
        
    def _setup_plot_style(self):
        """Configure premium plot styling"""
        # Background
        self.setBackground('#141b2d')
        
        # Remove default padding
        self.plotItem.setContentsMargins(10, 10, 10, 10)
        
        # Grid
        self.showGrid(x=True, y=True, alpha=0.2)
        
        # Axes
        axis_color = '#4b5563'
        text_color = '#9ca3af'
        
        # X-axis (Time)
        self.setLabel('bottom', 'Time', units='s', color=text_color)
        self.getAxis('bottom').setPen(axis_color)
        self.getAxis('bottom').setTextPen(text_color)
        
        # Y-axis (Throttle)
        self.setLabel('left', 'Throttle', units='%', color=text_color)
        self.getAxis('left').setPen(axis_color)
        self.getAxis('left').setTextPen(text_color)
        
        # Set Y range
        self.setYRange(0, 100, padding=0.02)
        
        # Disable auto-range
        self.enableAutoRange(axis='y', enable=False)
        bottom_axis = self.getAxis('bottom')
        #bottom_axis.setTickSpacing(major=1, minor=None)

        
    def _add_threshold_lines(self):
        """Add visual threshold indicators"""
        # Fault threshold line (70%)
        fault_line = pg.InfiniteLine(
            pos=70,
            angle=0,
            pen=pg.mkPen(color='#ef4444', width=1.5, style=Qt.PenStyle.DashLine),
            label='70%',
            labelOpts={'position': 0.95, 'color': '#ef4444'}
        )
        self.addItem(fault_line)
        
        # Warning zone (70%-100%)
        warning_region = pg.LinearRegionItem(
            values=[70, 100],
            brush=pg.mkBrush(255, 165, 0, 15),
            movable=False
        )
        self.addItem(warning_region)
        
    def add_data_point(self, throttle_pct: float):
        """
        Add new throttle data point
        
        Args:
            throttle_pct: Throttle percentage (0-100)
        """
        # Increment time counter
        self.time_counter += 1
        
        # Time in seconds
        time_sec = self.time_counter * 0.05  # Assuming 50ms updates
        
        # Add to buffers
        self.time_data.append(time_sec)
        self.throttle_data.append(throttle_pct)
        
        # Update plot curve
        self.curve.setData(list(self.time_data), list(self.throttle_data))
        
        # Auto-scroll X axis to show latest data
        if len(self.time_data) > 0:
            latest_time = self.time_data[-1]
            # Show last 10 seconds
            self.setXRange(
                max(0, latest_time - self.history_seconds),
                latest_time,
                padding=0
            )

            
    def clear_plot(self):
        """Clear all data from plot"""
        self.time_data.clear()
        self.throttle_data.clear()
        self.time_counter = 0
        self.curve.setData([], [])
