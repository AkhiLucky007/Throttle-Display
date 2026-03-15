"""
Throttle Processor Module
Handles ADC to percentage conversion and validation
"""
import logging

logger = logging.getLogger(__name__)


class ThrottleProcessor:
    """
    Processes raw throttle ADC values into percentages
    Handles scaling, validation, and bounds checking
    """
    
    def __init__(self, adc_min=0, adc_max=4095):
        """
        Initialize processor with ADC range
        
        Args:
            adc_min: Minimum ADC value (default: 0)
            adc_max: Maximum ADC value (default: 4095 for 12-bit ADC)
        """
        self.adc_min = adc_min
        self.adc_max = adc_max
        self.adc_range = adc_max - adc_min
        
        logger.info(f"ThrottleProcessor initialized (ADC range: {adc_min}-{adc_max})")
        
    def adc_to_percentage(self, adc_value: int) -> float:
        """
        Convert ADC value to percentage
        
        Args:
            adc_value: Raw ADC reading
            
        Returns:
            Throttle percentage (0.0 - 100.0)
        """
        # Clamp to valid range
        adc_clamped = max(self.adc_min, min(self.adc_max, adc_value))
        
        # Linear scaling to percentage
        percentage = ((adc_clamped - self.adc_min) / self.adc_range) * 100.0
        
        return round(percentage, 1)
        
    def percentage_to_adc(self, percentage: float) -> int:
        """
        Convert percentage back to ADC value (for testing/simulation)
        
        Args:
            percentage: Throttle percentage (0.0 - 100.0)
            
        Returns:
            Estimated ADC value
        """
        # Clamp percentage
        pct_clamped = max(0.0, min(100.0, percentage))
        
        # Scale to ADC range
        adc_value = int(self.adc_min + (pct_clamped / 100.0) * self.adc_range)
        
        return adc_value
        
    def is_valid_adc(self, adc_value: int) -> bool:
        """
        Check if ADC value is within valid range
        
        Args:
            adc_value: ADC reading to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.adc_min <= adc_value <= self.adc_max
        
    def validate_percentage(self, percentage: float) -> bool:
        """
        Check if percentage is within valid range
        
        Args:
            percentage: Percentage value to validate
            
        Returns:
            True if valid, False otherwise
        """
        return 0.0 <= percentage <= 100.0
