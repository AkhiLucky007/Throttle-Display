"""
State Machine Module
Manages system state transitions (DISABLED / READY / FAULT)
"""
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class SystemState(Enum):
    """System state enumeration"""
    DISABLED = "DISABLED"
    READY = "READY"
    FAULT = "FAULT"


class StateMachine:
    """
    Manages system state based on throttle and enabled status
    
    State Transition Rules:
    - DISABLED: enabled = False
    - READY: enabled = True AND throttle <= fault_threshold
    - FAULT: enabled = True AND throttle > fault_threshold
    """
    
    def __init__(self, fault_threshold=70.0):
        """
        Initialize state machine
        
        Args:
            fault_threshold: Throttle percentage above which system faults
        """
        self.fault_threshold = fault_threshold
        self.current_state = SystemState.DISABLED
        self.previous_state = None
        
        logger.info(f"StateMachine initialized (fault threshold: {fault_threshold}%)")
        
    def update(self, throttle_pct: float, enabled: bool) -> SystemState:
        """
        Update state based on current conditions
        
        Args:
            throttle_pct: Current throttle percentage
            enabled: System enabled flag
            
        Returns:
            New system state
        """
        self.previous_state = self.current_state
        
        # Determine new state
        if not enabled:
            new_state = SystemState.DISABLED
        elif throttle_pct > self.fault_threshold:
            new_state = SystemState.FAULT
        else:
            new_state = SystemState.READY
            
        # Log state transitions
        if new_state != self.current_state:
            logger.info(f"State transition: {self.current_state.value} -> {new_state.value}")
            
        self.current_state = new_state
        return new_state
        
    def get_state_string(self) -> str:
        """Get current state as string"""
        return self.current_state.value
        
    def is_fault(self) -> bool:
        """Check if currently in fault state"""
        return self.current_state == SystemState.FAULT
        
    def is_ready(self) -> bool:
        """Check if currently in ready state"""
        return self.current_state == SystemState.READY
        
    def is_disabled(self) -> bool:
        """Check if currently disabled"""
        return self.current_state == SystemState.DISABLED
        
    def has_state_changed(self) -> bool:
        """Check if state changed in last update"""
        return self.current_state != self.previous_state
