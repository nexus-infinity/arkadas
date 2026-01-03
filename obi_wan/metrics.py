"""
Metrics Module - Measurement interface.

Provides standardized interface for measuring and tracking system metrics.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import deque


class Metric:
    """Individual metric tracker."""
    
    def __init__(self, name: str, unit: str = "", max_history: int = 100):
        """
        Initialize a metric.
        
        Args:
            name: Metric name
            unit: Unit of measurement
            max_history: Maximum number of historical values to keep
        """
        self.name = name
        self.unit = unit
        self.max_history = max_history
        self.history = deque(maxlen=max_history)
        self.current_value = None
        self.last_update = None
        
    def record(self, value: float, timestamp: Optional[datetime] = None):
        """
        Record a metric value.
        
        Args:
            value: Metric value
            timestamp: Optional timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.current_value = value
        self.last_update = timestamp
        self.history.append((timestamp, value))
        
    def get_current(self) -> Optional[float]:
        """Get current metric value."""
        return self.current_value
    
    def get_average(self, last_n: Optional[int] = None) -> float:
        """
        Calculate average over history.
        
        Args:
            last_n: Number of recent values to average (None = all)
            
        Returns:
            Average value
        """
        if not self.history:
            return 0.0
            
        values = [v for _, v in self.history]
        if last_n:
            values = values[-last_n:]
            
        return sum(values) / len(values)
    
    def get_min_max(self) -> Tuple[float, float]:
        """
        Get min and max values from history.
        
        Returns:
            Tuple of (min, max)
        """
        if not self.history:
            return (0.0, 0.0)
            
        values = [v for _, v in self.history]
        return (min(values), max(values))


class MetricsInterface:
    """Interface for system-wide metrics collection and reporting."""
    
    def __init__(self):
        """Initialize metrics interface."""
        self.metrics: Dict[str, Metric] = {}
        
    def register_metric(self, name: str, unit: str = "", max_history: int = 100):
        """
        Register a new metric.
        
        Args:
            name: Metric name
            unit: Unit of measurement
            max_history: Maximum history size
        """
        self.metrics[name] = Metric(name, unit, max_history)
        
    def record_metric(self, name: str, value: float, timestamp: Optional[datetime] = None):
        """
        Record a metric value.
        
        Args:
            name: Metric name
            value: Metric value
            timestamp: Optional timestamp
        """
        if name not in self.metrics:
            self.register_metric(name)
            
        self.metrics[name].record(value, timestamp)
        
    def get_metric(self, name: str) -> Optional[Metric]:
        """
        Get a metric by name.
        
        Args:
            name: Metric name
            
        Returns:
            Metric object or None
        """
        return self.metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get summary of all metrics.
        
        Returns:
            Dictionary of metric summaries
        """
        summary = {}
        for name, metric in self.metrics.items():
            summary[name] = {
                'current': metric.get_current(),
                'average': metric.get_average(),
                'min_max': metric.get_min_max(),
                'unit': metric.unit,
                'last_update': metric.last_update
            }
        return summary
    
    def clear_metric(self, name: str):
        """
        Clear history for a metric.
        
        Args:
            name: Metric name
        """
        if name in self.metrics:
            self.metrics[name].history.clear()
            self.metrics[name].current_value = None
            
    def remove_metric(self, name: str):
        """
        Remove a metric entirely.
        
        Args:
            name: Metric name
        """
        if name in self.metrics:
            del self.metrics[name]
