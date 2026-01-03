"""
Aperture Sensing Module
Implements 360° → 180° aperture sensing and processing
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import math


@dataclass
class SensorReading:
    """Represents a single sensor reading from the 360° field"""
    angle: float  # Angle in degrees (0-360)
    data: Any
    timestamp: float
    source_id: Optional[str] = None


class ApertureSensing:
    """
    Aperture Sensing System
    Receives information from all directions (360° horizontal)
    Processes through chamber
    Focuses upward toward DOJO (180° sky hemisphere)
    """
    
    def __init__(self):
        self.input_buffer: List[SensorReading] = []
        self.output_buffer: List[Any] = []
        self.is_active = False
        self.total_received = 0
        self.total_processed = 0
        
    def start(self) -> None:
        """Start the aperture sensing system"""
        self.is_active = True
        
    def stop(self) -> None:
        """Stop the aperture sensing system"""
        self.is_active = False
        
    def receive_360(self, angle: float, data: Any, source_id: Optional[str] = None) -> bool:
        """
        Receive information from any direction in the 360° field
        
        Args:
            angle: Direction angle (0-360 degrees)
            data: Information received
            source_id: Optional identifier of the source
            
        Returns:
            True if successfully received
        """
        if not self.is_active:
            return False
        
        # Normalize angle to 0-360 range
        angle = angle % 360
        
        reading = SensorReading(
            angle=angle,
            data=data,
            timestamp=time.time(),
            source_id=source_id
        )
        
        self.input_buffer.append(reading)
        self.total_received += 1
        return True
    
    def process_aperture(self) -> List[Any]:
        """
        Process all readings through the aperture
        Compresses 360° input into 180° focused output
        
        Returns:
            List of processed data ready for upward focus
        """
        if not self.input_buffer:
            return []
        
        # Process all readings
        processed = []
        for reading in self.input_buffer:
            # Apply aperture compression logic
            # Focus only on upward hemisphere (0-180 degrees in vertical plane)
            focused_data = self._apply_aperture_focus(reading)
            if focused_data is not None:
                processed.append(focused_data)
                self.total_processed += 1
        
        # Clear input buffer
        self.input_buffer.clear()
        
        # Add to output buffer
        self.output_buffer.extend(processed)
        
        return processed
    
    def _apply_aperture_focus(self, reading: SensorReading) -> Optional[Any]:
        """
        Apply aperture focusing to a single reading
        Transforms 360° horizontal input to 180° upward focus
        
        Args:
            reading: Input sensor reading
            
        Returns:
            Focused data or None if filtered out
        """
        # Aperture logic: compress and focus
        # All horizontal inputs are considered and transformed
        # for upward projection toward DOJO
        
        focused = {
            "original_angle": reading.angle,
            "data": reading.data,
            "timestamp": reading.timestamp,
            "source_id": reading.source_id,
            "focused": True,
            "upward_vector": self._calculate_upward_vector(reading.angle)
        }
        
        return focused
    
    def _calculate_upward_vector(self, horizontal_angle: float) -> Dict[str, float]:
        """
        Calculate upward projection vector for a horizontal angle
        
        Args:
            horizontal_angle: Angle in horizontal plane (0-360)
            
        Returns:
            Upward vector components
        """
        # Convert horizontal angle to upward focus
        # All inputs contribute to the 180° upward hemisphere
        
        # Project onto hemisphere
        theta = horizontal_angle * math.pi / 180.0
        
        return {
            "azimuth": horizontal_angle,
            "elevation": 45.0,  # Default elevation toward peak
            "x": math.cos(theta),
            "y": math.sin(theta),
            "z": 1.0  # Upward component
        }
    
    def get_focused_output(self) -> List[Any]:
        """
        Get processed and focused output ready for DOJO
        
        Returns:
            List of focused data
        """
        output = self.output_buffer.copy()
        self.output_buffer.clear()
        return output
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get aperture sensing metrics
        
        Returns:
            Metrics dictionary
        """
        return {
            "active": self.is_active,
            "input_buffer_size": len(self.input_buffer),
            "output_buffer_size": len(self.output_buffer),
            "total_received": self.total_received,
            "total_processed": self.total_processed,
            "processing_rate": self.total_processed / max(1, self.total_received),
        }
    
    def get_status(self) -> str:
        """Get current status"""
        if self.is_active:
            return "ACTIVE"
        return "INACTIVE"
