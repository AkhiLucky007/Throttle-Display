"""
Data Simulator — Project 1 (Throttle)
Output format matches MOCK_Data.py exactly:
    {"system": "enabled"|"disabled", "throttle": 72.3, "fault": "more"|"ok"}
"""
import random
import logging
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

logger = logging.getLogger(__name__)


class DataSimulator(QObject):
    data_received    = pyqtSignal(dict)
    connection_status = pyqtSignal(bool, str)

    def __init__(self, update_rate_ms=100, noise_level=2.0):
        super().__init__()
        self.update_rate_ms  = update_rate_ms
        self.noise_level     = noise_level
        self.timer           = QTimer()
        self.timer.timeout.connect(self._generate_data)

        self.throttle_target  = 30.0
        self.throttle_current = 30.0
        self.enabled          = True
        self.cycle_counter    = 0

        logger.info("Throttle simulator initialized")

    def start(self):
        self.timer.start(self.update_rate_ms)
        self.connection_status.emit(True, "Simulator Active")

    def stop(self):
        self.timer.stop()
        self.connection_status.emit(False, "Simulator Stopped")

    def _generate_data(self):
        self.cycle_counter += 1

        # Change throttle target every ~3 seconds
        if self.cycle_counter % 30 == 0:
            self.throttle_target = random.choice([20.0, 50.0, 65.0, 75.0, 85.0])

        # Toggle enabled occasionally
        if self.cycle_counter % 50 == 0:
            self.enabled = random.choice([True, False])

        # Smooth transition
        diff = self.throttle_target - self.throttle_current
        self.throttle_current += diff * 0.1

        # Add noise
        noisy = self.throttle_current + random.uniform(-self.noise_level, self.noise_level)
        noisy = round(max(0.0, min(100.0, noisy)), 1)

        # Packet format matches MOCK_Data.py exactly
        packet = {
            "system":   "enabled" if self.enabled else "disabled",
            "throttle": noisy,
            "fault":    "more" if noisy >= 70.0 else "ok"
        }

        self.data_received.emit(packet)
