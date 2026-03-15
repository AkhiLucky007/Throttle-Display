"""
Data Model Module
Defines the structure of throttle system data
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ThrottleData:
    """
    Immutable data structure representing one throttle reading
    """
    throttle_pct: float      # Throttle percentage (0-100)
    throttle_adc: int        # Raw ADC value (0-4095)
    enabled: bool            # System enabled flag
    state: str               # System state: DISABLED, READY, or FAULT
    timestamp: datetime = None
    
    def __post_init__(self):
        """Auto-set timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
            
    @property
    def is_fault(self) -> bool:
        """Check if system is in fault state"""
        return self.state == "FAULT"
        
    @property
    def is_ready(self) -> bool:
        """Check if system is ready"""
        return self.state == "READY"
        
    @property
    def is_disabled(self) -> bool:
        """Check if system is disabled"""
        return self.state == "DISABLED"
        
    def __str__(self):
        """Human-readable string representation"""
        return (f"ThrottleData(pct={self.throttle_pct:.1f}%, "
                f"adc={self.throttle_adc}, "
                f"state={self.state}, "
                f"enabled={self.enabled})")
