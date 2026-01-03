"""
Synchronizer Module - Organic ⚭ Digital synchronization.

Bridges the organic (human) and digital (machine) domains,
creating coherent alignment between biological and computational processes.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import time


class OrganicDigitalSync:
    """Synchronizes organic (biological) and digital (computational) states."""
    
    def __init__(self, sync_frequency: float = 1.0):
        """
        Initialize synchronizer.
        
        Args:
            sync_frequency: Synchronization frequency in Hz
        """
        self.sync_frequency = sync_frequency
        self.sync_period = 1.0 / sync_frequency
        self.last_sync_time = None
        self.organic_state = {}
        self.digital_state = {}
        self.coherence_score = 0.0
        
    def sync_organic_input(self, organic_data: Dict[str, Any]):
        """
        Process organic (human) input data.
        
        Args:
            organic_data: Dictionary containing organic domain data
        """
        self.organic_state.update(organic_data)
        self.last_sync_time = datetime.now()
        self._calculate_coherence()
        
    def sync_digital_input(self, digital_data: Dict[str, Any]):
        """
        Process digital (machine) input data.
        
        Args:
            digital_data: Dictionary containing digital domain data
        """
        self.digital_state.update(digital_data)
        self.last_sync_time = datetime.now()
        self._calculate_coherence()
        
    def get_synchronized_state(self) -> Dict[str, Any]:
        """
        Get the current synchronized state combining both domains.
        
        Returns:
            Dictionary containing merged organic and digital state
        """
        return {
            'organic': self.organic_state.copy(),
            'digital': self.digital_state.copy(),
            'coherence': self.coherence_score,
            'timestamp': self.last_sync_time
        }
    
    def _calculate_coherence(self):
        """Calculate coherence score between organic and digital states."""
        if not self.organic_state or not self.digital_state:
            self.coherence_score = 0.0
            return
            
        # Simple coherence calculation based on matching keys
        common_keys = set(self.organic_state.keys()) & set(self.digital_state.keys())
        if not common_keys:
            self.coherence_score = 0.0
            return
            
        total_keys = len(set(self.organic_state.keys()) | set(self.digital_state.keys()))
        self.coherence_score = len(common_keys) / total_keys
        
    def is_synchronized(self) -> bool:
        """
        Check if system is currently synchronized.
        
        Returns:
            True if coherence score is above threshold
        """
        return self.coherence_score >= 0.5
    
    def get_coherence(self) -> float:
        """
        Get current coherence score.
        
        Returns:
            Coherence value between 0.0 and 1.0
        """
        return self.coherence_score
    
    def reset_sync(self):
        """Reset synchronization state."""
        self.organic_state = {}
        self.digital_state = {}
        self.coherence_score = 0.0
        self.last_sync_time = None
