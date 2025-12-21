"""
Pyramid Module - 1/3 height calculations.

Calculates geometric properties of pyramids, particularly focusing on
the 1/3 height position (King's Chamber location) and its significance.
"""

import math
from typing import Dict, Tuple, Optional


class PyramidGeometry:
    """Geometric calculations for pyramid structures."""
    
    def __init__(self, base_length: float, height: float):
        """
        Initialize pyramid geometry.
        
        Args:
            base_length: Length of square base
            height: Total pyramid height
        """
        self.base_length = base_length
        self.height = height
        self.chamber_ratio = 1.0 / 3.0
        
    def get_chamber_height(self) -> float:
        """
        Get the chamber height (1/3 of total height).
        
        Returns:
            Chamber height
        """
        return self.height * self.chamber_ratio
    
    def get_chamber_cross_section(self) -> float:
        """
        Get the cross-sectional area at chamber height.
        
        Returns:
            Area of pyramid cross-section at 1/3 height
        """
        # At height h, the cross-section is proportional to (H-h)/H
        remaining_height_ratio = 1.0 - self.chamber_ratio
        side_length = self.base_length * remaining_height_ratio
        return side_length ** 2
    
    def get_volume(self) -> float:
        """
        Get total pyramid volume.
        
        Returns:
            Pyramid volume
        """
        return (self.base_length ** 2 * self.height) / 3.0
    
    def get_chamber_volume(self) -> float:
        """
        Get volume from base to chamber height.
        
        Returns:
            Volume of pyramid section up to chamber
        """
        chamber_height = self.get_chamber_height()
        # Volume of truncated pyramid from base to chamber
        # This is total volume minus volume of upper pyramid
        upper_height = self.height - chamber_height
        upper_base = self.base_length * (upper_height / self.height)
        upper_volume = (upper_base ** 2 * upper_height) / 3.0
        return self.get_volume() - upper_volume
    
    def get_slant_height(self) -> float:
        """
        Get slant height of pyramid face.
        
        Returns:
            Slant height from base edge to apex
        """
        half_base = self.base_length / 2
        return math.sqrt(self.height ** 2 + half_base ** 2)
    
    def get_surface_area(self) -> float:
        """
        Get total surface area (base + 4 faces).
        
        Returns:
            Total surface area
        """
        base_area = self.base_length ** 2
        face_area = 4 * (0.5 * self.base_length * self.get_slant_height())
        return base_area + face_area
    
    def get_apex_angle(self) -> float:
        """
        Get apex angle in degrees.
        
        Returns:
            Angle at pyramid apex
        """
        half_base = self.base_length / 2
        angle_rad = math.atan(half_base / self.height)
        return math.degrees(angle_rad) * 2
    
    def get_chamber_position(self) -> Dict[str, float]:
        """
        Get detailed chamber position information.
        
        Returns:
            Dictionary with chamber geometry details
        """
        chamber_height = self.get_chamber_height()
        cross_section = self.get_chamber_cross_section()
        
        return {
            'height': chamber_height,
            'height_ratio': self.chamber_ratio,
            'cross_section_area': cross_section,
            'cross_section_side': math.sqrt(cross_section),
            'distance_from_apex': self.height - chamber_height,
            'volume_below': self.get_chamber_volume()
        }
    
    def calculate_resonance_point(self, frequency: float) -> float:
        """
        Calculate resonance point for given frequency.
        
        Args:
            frequency: Input frequency
            
        Returns:
            Height position of resonance point
        """
        # Resonance occurs at fractional heights
        # Using 1/3 as primary resonance point
        return self.height * (1.0 / frequency) if frequency > 0 else self.get_chamber_height()
    
    def get_golden_ratio_height(self) -> float:
        """
        Get height at golden ratio position.
        
        Returns:
            Height at golden ratio (φ ≈ 1.618)
        """
        phi = (1 + math.sqrt(5)) / 2
        return self.height / phi
    
    def is_at_chamber_height(self, height: float, tolerance: float = 0.01) -> bool:
        """
        Check if given height is at chamber position.
        
        Args:
            height: Height to check
            tolerance: Tolerance for comparison
            
        Returns:
            True if height is at chamber position
        """
        chamber_h = self.get_chamber_height()
        return abs(height - chamber_h) <= tolerance
