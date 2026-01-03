"""
Test suite for ARKADAŠ synchronization engine
"""

import pytest
from arkadas.sync import SyncEngine, SyncState


class TestSyncEngine:
    """Tests for SyncEngine class"""
    
    def test_initialization(self):
        """Test sync engine initialization"""
        engine = SyncEngine()
        assert engine.organic_state is None
        assert engine.digital_state is None
        assert engine.sync_precision == 0.0
        assert not engine.is_calibrated
        assert engine.sync_count == 0
    
    def test_calibrate(self):
        """Test calibration"""
        engine = SyncEngine()
        result = engine.calibrate()
        
        assert result is True
        assert engine.is_calibrated is True
        assert engine.organic_state == 0.0
        assert engine.digital_state == 0.0
    
    def test_measure_organic(self):
        """Test organic field measurement"""
        engine = SyncEngine()
        value = 0.5
        result = engine.measure_organic(value)
        
        assert result == value
        assert engine.organic_state == value
    
    def test_measure_digital(self):
        """Test digital field measurement"""
        engine = SyncEngine()
        value = 0.5
        result = engine.measure_digital(value)
        
        assert result == value
        assert engine.digital_state == value
    
    def test_calculate_drift_no_measurements(self):
        """Test drift calculation without measurements"""
        engine = SyncEngine()
        drift = engine.calculate_drift()
        assert drift == 1.0  # Maximum drift
    
    def test_calculate_drift_with_measurements(self):
        """Test drift calculation with measurements"""
        engine = SyncEngine()
        engine.measure_organic(0.5)
        engine.measure_digital(0.6)
        
        drift = engine.calculate_drift()
        assert abs(drift - 0.1) < 0.0001  # abs(0.5 - 0.6) with floating point tolerance
    
    def test_calculate_drift_perfect_sync(self):
        """Test drift with perfect sync"""
        engine = SyncEngine()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5)
        
        drift = engine.calculate_drift()
        assert drift == 0.0
    
    def test_synchronize_not_calibrated(self):
        """Test sync without calibration"""
        engine = SyncEngine()
        result = engine.synchronize()
        assert result is False
    
    def test_synchronize_within_threshold(self):
        """Test successful synchronization"""
        engine = SyncEngine()
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5005)  # Within 0.001 threshold
        
        result = engine.synchronize()
        assert result is True
        assert engine.sync_count == 1
    
    def test_synchronize_outside_threshold(self):
        """Test sync outside threshold"""
        engine = SyncEngine()
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.6)  # Outside 0.001 threshold
        
        result = engine.synchronize()
        assert result is False
        # Should have applied adjustment
        assert engine.digital_state != 0.6
    
    def test_adjust_fields(self):
        """Test field adjustment"""
        engine = SyncEngine()
        engine.measure_organic(0.5)
        engine.measure_digital(0.7)
        
        initial_drift = engine.calculate_drift()
        engine.adjust_fields(initial_drift)
        
        new_drift = engine.calculate_drift()
        assert new_drift < initial_drift
    
    def test_is_synchronized(self):
        """Test sync status check"""
        engine = SyncEngine()
        assert not engine.is_synchronized()
        
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5)
        
        assert engine.is_synchronized()
    
    def test_get_sync_state_not_calibrated(self):
        """Test getting sync state without calibration"""
        engine = SyncEngine()
        state = engine.get_sync_state()
        assert state is None
    
    def test_get_sync_state_calibrated(self):
        """Test getting sync state"""
        engine = SyncEngine()
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5)
        
        state = engine.get_sync_state()
        assert isinstance(state, SyncState)
        assert state.organic_field == 0.5
        assert state.digital_field == 0.5
        assert state.drift == 0.0
    
    def test_get_precision_percentage(self):
        """Test precision percentage calculation"""
        engine = SyncEngine()
        engine.sync_precision = 0.95
        
        percentage = engine.get_precision_percentage()
        assert percentage == 95.0
    
    def test_reset(self):
        """Test engine reset"""
        engine = SyncEngine()
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5)
        engine.synchronize()
        
        engine.reset()
        
        assert engine.organic_state is None
        assert engine.digital_state is None
        assert engine.sync_precision == 0.0
        assert not engine.is_calibrated
        assert engine.sync_count == 0
    
    def test_get_metrics(self):
        """Test metrics retrieval"""
        engine = SyncEngine()
        engine.calibrate()
        engine.measure_organic(0.5)
        engine.measure_digital(0.5)
        engine.synchronize()
        
        metrics = engine.get_metrics()
        assert metrics["calibrated"] is True
        assert metrics["synchronized"] is True
        assert "precision" in metrics
        assert "drift" in metrics
        assert "sync_count" in metrics
        assert metrics["sync_count"] == 1
    
    def test_zero_drift_tolerance(self):
        """Test zero-drift tolerance enforcement"""
        engine = SyncEngine()
        engine.calibrate()
        
        # Test with drift just under threshold
        engine.measure_organic(0.5)
        engine.measure_digital(0.5 + engine.drift_threshold * 0.9)
        
        # Should be synchronized (drift < threshold)
        assert engine.is_synchronized()
        
        # Test with drift clearly over threshold
        engine.measure_digital(0.5 + engine.drift_threshold * 1.1)
        assert not engine.is_synchronized()
