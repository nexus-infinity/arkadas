"""
Synchronization Engine Module
Implements military-grade Organic ⚭ Digital synchronization
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class SyncState:
    """Represents the current synchronization state"""
    organic_field: float
    digital_field: float
    drift: float
    precision: float
    last_sync: float


class SyncEngine:
    """
    Synchronization Engine
    Military-grade precision alignment between organic and digital fields
    Zero-drift tolerance
    """
    
    def __init__(self):
        self.organic_state: Optional[float] = None
        self.digital_state: Optional[float] = None
        self.sync_precision = 0.0
        self.drift_threshold = 0.001  # Maximum allowed drift (0.1%)
        self.last_sync_time = 0.0
        self.sync_count = 0
        self.is_calibrated = False
        
    def calibrate(self) -> bool:
        """
        Calibrate the synchronization system
        
        Returns:
            True if calibration successful
        """
        # Initialize both fields
        self.organic_state = 0.0
        self.digital_state = 0.0
        self.last_sync_time = time.time()
        self.is_calibrated = True
        return True
    
    def measure_organic(self, value: float) -> float:
        """
        Measure the organic field state
        
        Args:
            value: Organic field measurement
            
        Returns:
            Normalized organic state
        """
        self.organic_state = value
        return value
    
    def measure_digital(self, value: float) -> float:
        """
        Measure the digital field state
        
        Args:
            value: Digital field measurement
            
        Returns:
            Normalized digital state
        """
        self.digital_state = value
        return value
    
    def calculate_drift(self) -> float:
        """
        Calculate drift between organic and digital fields
        
        Returns:
            Drift value (0.0 = perfect sync)
        """
        if self.organic_state is None or self.digital_state is None:
            return 1.0  # Maximum drift if not measured
        
        # Calculate absolute difference
        drift = abs(self.organic_state - self.digital_state)
        return drift
    
    def synchronize(self) -> bool:
        """
        Perform synchronization between organic and digital fields
        
        Returns:
            True if sync successful (within drift threshold)
        """
        if not self.is_calibrated:
            return False
        
        drift = self.calculate_drift()
        
        # Check if within tolerance
        if drift <= self.drift_threshold:
            # Successful sync
            self.sync_precision = 1.0 - drift
            self.last_sync_time = time.time()
            self.sync_count += 1
            return True
        else:
            # Need adjustment
            self.adjust_fields(drift)
            return False
    
    def adjust_fields(self, drift: float) -> None:
        """
        Adjust fields to reduce drift
        
        Args:
            drift: Current drift value
        """
        if self.organic_state is None or self.digital_state is None:
            return
        
        # Apply correction - bring fields closer together
        correction = drift * 0.5  # Apply 50% correction per cycle
        
        if self.organic_state > self.digital_state:
            self.digital_state += correction
        else:
            self.digital_state -= correction
        
        # Recalculate precision after adjustment
        new_drift = self.calculate_drift()
        self.sync_precision = max(0.0, 1.0 - new_drift)
    
    def get_sync_state(self) -> Optional[SyncState]:
        """
        Get current synchronization state
        
        Returns:
            SyncState object or None if not calibrated
        """
        if not self.is_calibrated or self.organic_state is None or self.digital_state is None:
            return None
        
        return SyncState(
            organic_field=self.organic_state,
            digital_field=self.digital_state,
            drift=self.calculate_drift(),
            precision=self.sync_precision,
            last_sync=self.last_sync_time
        )
    
    def is_synchronized(self) -> bool:
        """
        Check if fields are currently synchronized
        
        Returns:
            True if within drift threshold
        """
        if not self.is_calibrated:
            return False
        
        drift = self.calculate_drift()
        return drift <= self.drift_threshold
    
    def get_precision_percentage(self) -> float:
        """
        Get sync precision as percentage
        
        Returns:
            Precision percentage (0.0 - 100.0)
        """
        return self.sync_precision * 100.0
    
    def reset(self) -> None:
        """Reset synchronization engine"""
        self.organic_state = None
        self.digital_state = None
        self.sync_precision = 0.0
        self.last_sync_time = 0.0
        self.sync_count = 0
        self.is_calibrated = False
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get synchronization metrics
        
        Returns:
            Metrics dictionary
        """
        return {
            "calibrated": self.is_calibrated,
            "synchronized": self.is_synchronized(),
            "precision": self.sync_precision,
            "precision_percentage": self.get_precision_percentage(),
            "drift": self.calculate_drift(),
            "drift_threshold": self.drift_threshold,
            "sync_count": self.sync_count,
            "organic_state": self.organic_state,
            "digital_state": self.digital_state,
            "time_since_last_sync": time.time() - self.last_sync_time if self.last_sync_time > 0 else 0,
        }
