"""
Unit Tests for State Machine
Demonstrates how to test core logic independently
"""
import unittest
from core.state_machine import StateMachine, SystemState


class TestStateMachine(unittest.TestCase):
    """Test cases for the StateMachine class"""
    
    def setUp(self):
        """Create a fresh state machine for each test"""
        self.sm = StateMachine(fault_threshold=70.0)
        
    def test_initial_state_is_disabled(self):
        """State machine should start in DISABLED state"""
        self.assertEqual(self.sm.current_state, SystemState.DISABLED)
        
    def test_disabled_when_not_enabled(self):
        """Should be DISABLED when enabled flag is False"""
        state = self.sm.update(throttle_pct=50.0, enabled=False)
        self.assertEqual(state, SystemState.DISABLED)
        self.assertTrue(self.sm.is_disabled())
        
    def test_ready_when_enabled_below_threshold(self):
        """Should be READY when enabled and throttle below 70%"""
        state = self.sm.update(throttle_pct=60.0, enabled=True)
        self.assertEqual(state, SystemState.READY)
        self.assertTrue(self.sm.is_ready())
        
    def test_fault_when_above_threshold(self):
        """Should be FAULT when enabled and throttle above 70%"""
        state = self.sm.update(throttle_pct=75.0, enabled=True)
        self.assertEqual(state, SystemState.FAULT)
        self.assertTrue(self.sm.is_fault())
        
    def test_fault_at_exact_threshold(self):
        """Throttle at exactly 70% should not fault"""
        state = self.sm.update(throttle_pct=70.0, enabled=True)
        self.assertEqual(state, SystemState.READY)
        
    def test_fault_just_above_threshold(self):
        """Throttle at 70.1% should fault"""
        state = self.sm.update(throttle_pct=70.1, enabled=True)
        self.assertEqual(state, SystemState.FAULT)
        
    def test_state_transition_detection(self):
        """Should detect when state changes"""
        # Start disabled
        self.sm.update(throttle_pct=50.0, enabled=False)
        self.assertFalse(self.sm.has_state_changed())
        
        # Enable -> READY
        self.sm.update(throttle_pct=50.0, enabled=True)
        self.assertTrue(self.sm.has_state_changed())
        
        # Stay in READY
        self.sm.update(throttle_pct=60.0, enabled=True)
        self.assertFalse(self.sm.has_state_changed())
        
    def test_custom_fault_threshold(self):
        """Should respect custom fault threshold"""
        sm_custom = StateMachine(fault_threshold=80.0)
        
        # 75% should be READY with 80% threshold
        state = sm_custom.update(throttle_pct=75.0, enabled=True)
        self.assertEqual(state, SystemState.READY)
        
        # 85% should be FAULT
        state = sm_custom.update(throttle_pct=85.0, enabled=True)
        self.assertEqual(state, SystemState.FAULT)


if __name__ == '__main__':
    unittest.main()
