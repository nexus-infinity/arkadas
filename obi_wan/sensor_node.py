"""
OBI-WAN Sensor Node Module
===========================

Individual sensor nodes that form the collective intelligence network.
Each node provides omnidirectional sensing in its domain.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List
import time
import math


class SensorType(Enum):
    """Types of sensors in the OBI-WAN network."""
    ELECTROMAGNETIC = "electromagnetic"
    ACOUSTIC = "acoustic"
    THERMAL = "thermal"
    PROXIMITY = "proximity"
    CHEMICAL = "chemical"


@dataclass
class SensorReading:
    """A reading from a sensor node."""
    sensor_id: str
    sensor_type: SensorType
    angle: float  # degrees (0-360)
    value: float  # sensor-specific units
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SensorConfig:
    """Configuration for a sensor node."""
    sensor_type: SensorType
    range: float = 360.0  # degrees
    resolution: float = 1.0  # degrees
    frequency_range: Optional[tuple] = None  # For acoustic sensors
    sample_rate: float = 60.0  # Hz
    calibration_offset: float = 0.0


class SensorNode:
    """
    A single sensor node in the OBI-WAN network.
    
    Each node provides omnidirectional sensing and contributes to the
    collective intelligence of the network.
    """
    
    def __init__(
        self,
        node_id: str,
        config: SensorConfig,
        position: Optional[tuple] = None
    ):
        """
        Initialize a sensor node.
        
        Args:
            node_id: Unique identifier for this node
            config: Sensor configuration
            position: Optional (x, y, z) position in space
        """
        self.node_id = node_id
        self.config = config
        self.position = position or (0.0, 0.0, 0.0)
        self.active = True
        self.readings_buffer: List[SensorReading] = []
        self.total_readings = 0
        
    def sense(self, angle: float, value: float, **metadata) -> SensorReading:
        """
        Create a sensor reading at a specific angle.
        
        Args:
            angle: Direction in degrees (0-360)
            value: Sensed value
            **metadata: Additional metadata for the reading
            
        Returns:
            SensorReading object
        """
        # Apply calibration offset
        calibrated_value = value + self.config.calibration_offset
        
        # Calculate confidence based on sensor characteristics
        confidence = self._calculate_confidence(angle, calibrated_value)
        
        reading = SensorReading(
            sensor_id=self.node_id,
            sensor_type=self.config.sensor_type,
            angle=angle % 360.0,
            value=calibrated_value,
            timestamp=time.time(),
            confidence=confidence,
            metadata=metadata
        )
        
        self.readings_buffer.append(reading)
        self.total_readings += 1
        
        # Maintain buffer size
        if len(self.readings_buffer) > 1000:
            self.readings_buffer.pop(0)
        
        return reading
    
    def sense_omnidirectional(self, values: Dict[float, float]) -> List[SensorReading]:
        """
        Create sensor readings for all directions.
        
        Args:
            values: Dictionary mapping angles to values
            
        Returns:
            List of SensorReading objects
        """
        readings = []
        for angle, value in values.items():
            reading = self.sense(angle, value)
            readings.append(reading)
        return readings
    
    def _calculate_confidence(self, angle: float, value: float) -> float:
        """
        Calculate confidence level for a reading.
        
        Confidence may vary based on sensor type and characteristics.
        
        Args:
            angle: Direction angle
            value: Sensed value
            
        Returns:
            Confidence level (0-1)
        """
        # Base confidence
        confidence = 1.0
        
        # Reduce confidence at extremes for certain sensor types
        if self.config.sensor_type == SensorType.ELECTROMAGNETIC:
            # EM sensors may have blind spots
            if angle > 350 or angle < 10:
                confidence *= 0.9
        
        # Value-based confidence (assuming normalized 0-1 values)
        if value < 0 or value > 1:
            confidence *= 0.8
        
        return max(0.0, min(1.0, confidence))
    
    def get_recent_readings(self, count: int = 10) -> List[SensorReading]:
        """
        Get the most recent sensor readings.
        
        Args:
            count: Number of readings to retrieve
            
        Returns:
            List of recent SensorReading objects
        """
        return self.readings_buffer[-count:]
    
    def get_reading_statistics(self) -> Dict[str, Any]:
        """Get statistics about sensor readings."""
        if not self.readings_buffer:
            return {
                "total_readings": self.total_readings,
                "buffer_size": 0,
                "avg_confidence": 0.0,
                "sensor_type": self.config.sensor_type.value
            }
        
        avg_confidence = sum(r.confidence for r in self.readings_buffer) / len(self.readings_buffer)
        avg_value = sum(r.value for r in self.readings_buffer) / len(self.readings_buffer)
        
        return {
            "total_readings": self.total_readings,
            "buffer_size": len(self.readings_buffer),
            "avg_confidence": avg_confidence,
            "avg_value": avg_value,
            "sensor_type": self.config.sensor_type.value,
            "position": self.position,
            "active": self.active
        }
    
    def calibrate(self, offset: float) -> None:
        """
        Calibrate the sensor with a new offset.
        
        Args:
            offset: Calibration offset to apply
        """
        self.config.calibration_offset = offset
    
    def reset(self) -> None:
        """Reset the sensor node."""
        self.readings_buffer.clear()
        self.total_readings = 0
