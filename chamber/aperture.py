"""
Aperture Module - 360° to 180° conversion.

Converts full 360° sensing data into focused 180° awareness,
representing the transformation from observation to action.
"""

import math
from typing import Dict, List, Optional, Tuple


class ApertureConverter:
    """Converts 360° omnidirectional sensing to 180° focused awareness."""
    
    def __init__(self, focus_direction: float = 0.0):
        """
        Initialize aperture converter.
        
        Args:
            focus_direction: Primary focus direction in degrees (0-360)
        """
        self.focus_direction = focus_direction % 360
        self.aperture_width = 180
        
    def convert(self, sensor_data: Dict[float, float]) -> Dict[float, float]:
        """
        Convert 360° sensor data to 180° focused data.
        
        Args:
            sensor_data: Dictionary mapping angles (0-360) to values
            
        Returns:
            Dictionary mapping angles within 180° focus range to values
        """
        focused_data = {}
        half_aperture = self.aperture_width / 2
        
        for angle, value in sensor_data.items():
            # Calculate relative angle to focus direction
            relative_angle = (angle - self.focus_direction) % 360
            
            # Check if within aperture range
            if relative_angle <= half_aperture or relative_angle >= (360 - half_aperture):
                # Normalize to 0-180 range
                if relative_angle > 180:
                    normalized_angle = 360 - relative_angle
                else:
                    normalized_angle = relative_angle
                    
                focused_data[normalized_angle] = value
                
        return focused_data
    
    def get_focus_range(self) -> Tuple[float, float]:
        """
        Get the current focus range.
        
        Returns:
            Tuple of (start_angle, end_angle) in degrees
        """
        half_aperture = self.aperture_width / 2
        start = (self.focus_direction - half_aperture) % 360
        end = (self.focus_direction + half_aperture) % 360
        return (start, end)
    
    def set_focus_direction(self, direction: float):
        """
        Update the focus direction.
        
        Args:
            direction: New focus direction in degrees (0-360)
        """
        self.focus_direction = direction % 360
        
    def calculate_intensity(self, focused_data: Dict[float, float]) -> float:
        """
        Calculate overall intensity of focused data.
        
        Args:
            focused_data: Focused sensor data
            
        Returns:
            Average intensity value
        """
        if not focused_data:
            return 0.0
        return sum(focused_data.values()) / len(focused_data)
