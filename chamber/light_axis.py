"""
Light Axis Module - Vertical flow between peak and chamber.

Manages the vertical energy flow along the pyramid's light axis,
connecting the peak (highest consciousness) with the chamber (1/3 height).
"""

from typing import Dict, Optional, List
from enum import Enum


class FlowDirection(Enum):
    """Direction of energy flow along the light axis."""
    UPWARD = "upward"
    DOWNWARD = "downward"
    BALANCED = "balanced"


class LightAxis:
    """Manages vertical energy flow along the pyramid's light axis."""
    
    def __init__(self, chamber_height_ratio: float = 1/3):
        """
        Initialize light axis.
        
        Args:
            chamber_height_ratio: Position of chamber as ratio of pyramid height
        """
        self.chamber_height_ratio = chamber_height_ratio
        self.peak_energy = 0.0
        self.chamber_energy = 0.0
        self.flow_direction = FlowDirection.BALANCED
        self.flow_rate = 0.0
        
    def set_peak_energy(self, energy: float):
        """
        Set energy level at pyramid peak.
        
        Args:
            energy: Energy value at peak
        """
        self.peak_energy = max(0.0, energy)
        self._update_flow()
        
    def set_chamber_energy(self, energy: float):
        """
        Set energy level at chamber.
        
        Args:
            energy: Energy value at chamber
        """
        self.chamber_energy = max(0.0, energy)
        self._update_flow()
        
    def _update_flow(self):
        """Update flow direction and rate based on energy differential."""
        energy_diff = self.peak_energy - self.chamber_energy
        
        if abs(energy_diff) < 0.01:
            self.flow_direction = FlowDirection.BALANCED
            self.flow_rate = 0.0
        elif energy_diff > 0:
            self.flow_direction = FlowDirection.DOWNWARD
            self.flow_rate = energy_diff
        else:
            self.flow_direction = FlowDirection.UPWARD
            self.flow_rate = abs(energy_diff)
            
    def get_flow_state(self) -> Dict[str, any]:
        """
        Get current flow state.
        
        Returns:
            Dictionary containing flow information
        """
        return {
            'peak_energy': self.peak_energy,
            'chamber_energy': self.chamber_energy,
            'flow_direction': self.flow_direction.value,
            'flow_rate': self.flow_rate,
            'chamber_position': self.chamber_height_ratio
        }
    
    def balance_energy(self) -> float:
        """
        Balance energy between peak and chamber.
        
        Returns:
            Balanced energy level
        """
        balanced = (self.peak_energy + self.chamber_energy) / 2
        self.peak_energy = balanced
        self.chamber_energy = balanced
        self._update_flow()
        return balanced
    
    def propagate_upward(self, amount: float):
        """
        Propagate energy upward from chamber to peak.
        
        Args:
            amount: Amount of energy to transfer
        """
        transfer = min(amount, self.chamber_energy)
        self.chamber_energy -= transfer
        self.peak_energy += transfer
        self._update_flow()
        
    def propagate_downward(self, amount: float):
        """
        Propagate energy downward from peak to chamber.
        
        Args:
            amount: Amount of energy to transfer
        """
        transfer = min(amount, self.peak_energy)
        self.peak_energy -= transfer
        self.chamber_energy += transfer
        self._update_flow()
