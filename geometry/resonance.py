"""
Resonance Module - Frequency/chakra alignment.

Manages frequency resonance patterns and chakra energy alignment
within the pyramid geometry.
"""

import math
from typing import Dict, List, Optional, Tuple
from enum import Enum


class Chakra(Enum):
    """Seven primary chakras with associated frequencies."""
    ROOT = ("root", 396, "red")           # Muladhara
    SACRAL = ("sacral", 417, "orange")    # Svadhisthana
    SOLAR_PLEXUS = ("solar_plexus", 528, "yellow")  # Manipura
    HEART = ("heart", 639, "green")       # Anahata
    THROAT = ("throat", 741, "blue")      # Vishuddha
    THIRD_EYE = ("third_eye", 852, "indigo")  # Ajna
    CROWN = ("crown", 963, "violet")      # Sahasrara
    
    def __init__(self, name: str, frequency: float, color: str):
        self.chakra_name = name
        self.base_frequency = frequency
        self.color = color


class FrequencyResonance:
    """Manages frequency resonance and chakra alignment."""
    
    def __init__(self, base_frequency: float = 432.0):
        """
        Initialize frequency resonance system.
        
        Args:
            base_frequency: Base resonance frequency in Hz (default: 432 Hz)
        """
        self.base_frequency = base_frequency
        self.active_frequencies: Dict[float, float] = {}
        self.resonance_threshold = 0.05  # 5% tolerance for resonance
        
    def add_frequency(self, frequency: float, amplitude: float = 1.0):
        """
        Add a frequency to the resonance field.
        
        Args:
            frequency: Frequency in Hz
            amplitude: Amplitude/strength of frequency
        """
        self.active_frequencies[frequency] = amplitude
        
    def remove_frequency(self, frequency: float):
        """
        Remove a frequency from the field.
        
        Args:
            frequency: Frequency to remove
        """
        self.active_frequencies.pop(frequency, None)
        
    def calculate_resonance(self, target_frequency: float) -> float:
        """
        Calculate resonance strength at target frequency.
        
        Args:
            target_frequency: Frequency to measure resonance at
            
        Returns:
            Resonance strength (0-1)
        """
        if not self.active_frequencies:
            return 0.0
            
        total_resonance = 0.0
        
        for freq, amplitude in self.active_frequencies.items():
            # Calculate how close this frequency is to target
            ratio = freq / target_frequency if target_frequency > 0 else 0
            
            # Resonance occurs at harmonics (1:1, 1:2, 1:3, etc.)
            closest_harmonic = round(ratio)
            if closest_harmonic == 0:
                continue
                
            harmonic_error = abs(ratio - closest_harmonic) / closest_harmonic
            
            # If within threshold, add to resonance
            if harmonic_error <= self.resonance_threshold:
                resonance_strength = (1.0 - harmonic_error / self.resonance_threshold) * amplitude
                total_resonance += resonance_strength
                
        return min(total_resonance, 1.0)
    
    def find_harmonics(self, fundamental: float, num_harmonics: int = 7) -> List[float]:
        """
        Find harmonic frequencies of a fundamental.
        
        Args:
            fundamental: Fundamental frequency
            num_harmonics: Number of harmonics to generate
            
        Returns:
            List of harmonic frequencies
        """
        return [fundamental * (i + 1) for i in range(num_harmonics)]
    
    def align_to_chakra(self, chakra: Chakra) -> Dict[str, any]:
        """
        Align resonance system to chakra frequency.
        
        Args:
            chakra: Target chakra
            
        Returns:
            Alignment information
        """
        target_freq = chakra.base_frequency
        current_resonance = self.calculate_resonance(target_freq)
        
        # Calculate harmonics of chakra frequency
        harmonics = self.find_harmonics(target_freq, 3)
        
        return {
            'chakra': chakra.chakra_name,
            'target_frequency': target_freq,
            'current_resonance': current_resonance,
            'color': chakra.color,
            'harmonics': harmonics,
            'aligned': current_resonance >= 0.5
        }
    
    def get_dominant_chakra(self) -> Optional[Chakra]:
        """
        Determine which chakra has strongest resonance.
        
        Returns:
            Dominant chakra or None
        """
        max_resonance = 0.0
        dominant = None
        
        for chakra in Chakra:
            resonance = self.calculate_resonance(chakra.base_frequency)
            if resonance > max_resonance:
                max_resonance = resonance
                dominant = chakra
                
        return dominant if max_resonance > 0.1 else None
    
    def calculate_coherence(self) -> float:
        """
        Calculate overall frequency coherence.
        
        Returns:
            Coherence score (0-1)
        """
        if not self.active_frequencies:
            return 0.0
            
        # Check if frequencies are in harmonic relationship
        frequencies = sorted(self.active_frequencies.keys())
        if len(frequencies) < 2:
            return 1.0
            
        fundamental = frequencies[0]
        harmonic_matches = 0
        
        for freq in frequencies[1:]:
            ratio = freq / fundamental
            closest_integer = round(ratio)
            error = abs(ratio - closest_integer) / closest_integer
            
            if error <= self.resonance_threshold:
                harmonic_matches += 1
                
        coherence = harmonic_matches / (len(frequencies) - 1)
        return coherence
    
    def tune_to_432hz(self, frequency: float) -> float:
        """
        Convert frequency to 432 Hz tuning (from standard 440 Hz).
        
        Args:
            frequency: Input frequency in 440 Hz tuning
            
        Returns:
            Frequency in 432 Hz tuning
        """
        return frequency * (432.0 / 440.0)
    
    def get_resonance_map(self) -> Dict[str, any]:
        """
        Get comprehensive resonance state.
        
        Returns:
            Dictionary with resonance information
        """
        chakra_resonances = {
            chakra.chakra_name: self.calculate_resonance(chakra.base_frequency)
            for chakra in Chakra
        }
        
        return {
            'base_frequency': self.base_frequency,
            'active_frequencies': dict(self.active_frequencies),
            'coherence': self.calculate_coherence(),
            'chakra_resonances': chakra_resonances,
            'dominant_chakra': self.get_dominant_chakra().chakra_name if self.get_dominant_chakra() else None
        }
    
    def create_standing_wave(self, frequency: float, nodes: int = 3) -> List[float]:
        """
        Create standing wave pattern with given nodes.
        
        Args:
            frequency: Wave frequency
            nodes: Number of nodes in standing wave
            
        Returns:
            List of node positions (0-1 normalized)
        """
        # Nodes occur at integer fractions along wave
        return [i / (nodes - 1) for i in range(nodes)]
