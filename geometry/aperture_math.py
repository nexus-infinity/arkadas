"""
Aperture Math Module - 360° to 180° transforms.

Mathematical transformations for converting omnidirectional (360°)
data to focused directional (180°) representations.
"""

import math
from typing import List, Tuple, Dict, Optional
import numpy as np


class ApertureTransforms:
    """Mathematical transforms for aperture conversions."""
    
    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians."""
        return math.radians(degrees)
    
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees."""
        return math.degrees(radians)
    
    @staticmethod
    def normalize_angle(angle: float) -> float:
        """
        Normalize angle to 0-360 range.
        
        Args:
            angle: Input angle in degrees
            
        Returns:
            Normalized angle
        """
        return angle % 360
    
    @staticmethod
    def angular_distance(angle1: float, angle2: float) -> float:
        """
        Calculate shortest angular distance between two angles.
        
        Args:
            angle1: First angle in degrees
            angle2: Second angle in degrees
            
        Returns:
            Shortest distance (0-180)
        """
        diff = abs(angle1 - angle2) % 360
        return min(diff, 360 - diff)
    
    @staticmethod
    def project_to_180(angle: float, center: float = 0.0) -> Optional[float]:
        """
        Project 360° angle onto 180° aperture.
        
        Args:
            angle: Input angle (0-360)
            center: Center direction of aperture
            
        Returns:
            Projected angle (0-180) or None if outside aperture
        """
        relative = (angle - center) % 360
        
        # Check if within 180° range
        if relative <= 180:
            return relative
        elif relative >= 180:
            # Outside aperture
            return None
        
    @staticmethod
    def convert_360_to_180(data_360: Dict[float, float], 
                          focus_direction: float = 0.0) -> Dict[float, float]:
        """
        Convert 360° data distribution to 180° focused view.
        
        Args:
            data_360: Dictionary of angle -> value for full 360°
            focus_direction: Center of 180° aperture
            
        Returns:
            Dictionary of angle -> value for 180° range
        """
        data_180 = {}
        
        for angle, value in data_360.items():
            # Calculate relative angle to focus direction
            relative = (angle - focus_direction) % 360
            
            # Keep only angles within front 180°
            if relative <= 90 or relative >= 270:
                # Map to 0-180 range
                if relative >= 270:
                    mapped_angle = 360 - relative
                else:
                    mapped_angle = relative
                data_180[mapped_angle] = value
                
        return data_180
    
    @staticmethod
    def calculate_aperture_bounds(center: float, aperture_width: float = 180) -> Tuple[float, float]:
        """
        Calculate angular bounds of aperture.
        
        Args:
            center: Center direction
            aperture_width: Width of aperture in degrees
            
        Returns:
            Tuple of (start_angle, end_angle)
        """
        half_width = aperture_width / 2
        start = (center - half_width) % 360
        end = (center + half_width) % 360
        return (start, end)
    
    @staticmethod
    def is_within_aperture(angle: float, center: float, aperture_width: float = 180) -> bool:
        """
        Check if angle is within aperture bounds.
        
        Args:
            angle: Angle to check
            center: Aperture center
            aperture_width: Aperture width
            
        Returns:
            True if angle is within aperture
        """
        half_width = aperture_width / 2
        distance = ApertureTransforms.angular_distance(angle, center)
        return distance <= half_width
    
    @staticmethod
    def weighted_angular_average(angles: List[float], weights: Optional[List[float]] = None) -> float:
        """
        Calculate weighted average of angles (handling circular nature).
        
        Args:
            angles: List of angles in degrees
            weights: Optional weights for each angle
            
        Returns:
            Average angle in degrees
        """
        if not angles:
            return 0.0
            
        if weights is None:
            weights = [1.0] * len(angles)
            
        # Convert to unit vectors
        x_sum = sum(w * math.cos(math.radians(a)) for a, w in zip(angles, weights))
        y_sum = sum(w * math.sin(math.radians(a)) for a, w in zip(angles, weights))
        
        # Calculate average angle
        avg_rad = math.atan2(y_sum, x_sum)
        avg_deg = math.degrees(avg_rad)
        
        return avg_deg % 360
    
    @staticmethod
    def calculate_focus_quality(data_180: Dict[float, float]) -> float:
        """
        Calculate quality metric for focused data.
        
        Args:
            data_180: Focused 180° data
            
        Returns:
            Focus quality score (0-1)
        """
        if not data_180:
            return 0.0
            
        # Higher concentration of energy = better focus
        values = list(data_180.values())
        avg = sum(values) / len(values)
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        
        # Normalize variance to 0-1 quality score
        # High variance = poor focus, low variance = good focus
        max_variance = avg ** 2  # Maximum possible variance
        if max_variance == 0:
            return 0.0
            
        quality = 1.0 - min(variance / max_variance, 1.0)
        return quality
