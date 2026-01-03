"""
ARKADAŠ Aperture Module
========================

Transforms 360° panoramic sensing into 180° focused awareness.
Based on sacred geometry and the King's Chamber principle.

The aperture acts as a consciousness focusing mechanism, converting
omnidirectional sensing into directed attention, mirroring the
pyramid's function of concentrating cosmic energy at 1/3 height.
"""

import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import asyncio


@dataclass
class ApertureConfig:
    """Configuration for the aperture transformation system."""
    input_range: float = 360.0  # degrees
    output_range: float = 180.0  # degrees
    focal_angle: float = 90.0  # degrees (zenith)
    mode: str = "harmonic_compression"
    chamber_ratio: float = 0.333  # King's Chamber at 1/3 height


@dataclass
class SensorReading:
    """Represents a sensor reading with angle and intensity."""
    angle: float  # degrees (0-360)
    intensity: float  # normalized (0-1)
    timestamp: float = 0.0
    sensor_type: str = "generic"


@dataclass
class FocusedOutput:
    """Focused output after aperture transformation."""
    angle: float  # degrees (0-180)
    intensity: float  # normalized (0-1)
    original_angles: List[float] = field(default_factory=list)
    compression_factor: float = 1.0


class Aperture:
    """
    The Aperture transforms 360° omnidirectional sensing into 180° focused awareness.
    
    Like the King's Chamber concentrating pyramid energy, the aperture
    concentrates sensory information through harmonic compression.
    """
    
    def __init__(self, config: Optional[ApertureConfig] = None):
        """Initialize the aperture with configuration."""
        self.config = config or ApertureConfig()
        self.compression_ratio = self.config.input_range / self.config.output_range
        
    def transform_angle(self, input_angle: float) -> float:
        """
        Transform a 360° angle to 180° focused space.
        
        Uses harmonic compression centered on the focal angle.
        
        Args:
            input_angle: Input angle in degrees (0-360)
            
        Returns:
            Output angle in degrees (0-180)
        """
        # Normalize input angle to 0-360
        normalized = input_angle % 360.0
        
        # Calculate distance from focal angle
        distance = min(
            abs(normalized - self.config.focal_angle),
            abs(normalized - (self.config.focal_angle + 360))
        )
        
        # Apply harmonic compression using King's Chamber ratio
        if self.config.mode == "harmonic_compression":
            # Map 360° to 180° with emphasis on focal region
            # Use golden ratio for natural compression
            phi = 1.618033988749895
            compression = math.pow(distance / 180.0, phi)
            output = 90.0 * (1 - compression)
            
            # Apply chamber ratio for sacred geometry
            output *= (1 + self.config.chamber_ratio)
            
            return max(0.0, min(180.0, output))
        else:
            # Simple linear compression
            return (normalized / 360.0) * 180.0
    
    def compress_readings(
        self, 
        readings: List[SensorReading],
        resolution: float = 1.0
    ) -> List[FocusedOutput]:
        """
        Compress 360° sensor readings into 180° focused outputs.
        
        Args:
            readings: List of sensor readings from 360° space
            resolution: Output resolution in degrees
            
        Returns:
            List of focused outputs in 180° space
        """
        # Create bins for output angles
        num_bins = int(self.config.output_range / resolution)
        bins = [[] for _ in range(num_bins)]
        
        # Distribute readings into bins
        for reading in readings:
            output_angle = self.transform_angle(reading.angle)
            bin_idx = min(int(output_angle / resolution), num_bins - 1)
            bins[bin_idx].append(reading)
        
        # Aggregate readings in each bin
        focused_outputs = []
        for bin_idx, bin_readings in enumerate(bins):
            if not bin_readings:
                continue
                
            # Calculate weighted average intensity
            total_intensity = sum(r.intensity for r in bin_readings)
            avg_intensity = total_intensity / len(bin_readings)
            
            # Apply chamber ratio for emphasis
            enhanced_intensity = avg_intensity * (1 + self.config.chamber_ratio)
            enhanced_intensity = min(1.0, enhanced_intensity)
            
            output = FocusedOutput(
                angle=bin_idx * resolution,
                intensity=enhanced_intensity,
                original_angles=[r.angle for r in bin_readings],
                compression_factor=len(bin_readings) / 1.0
            )
            focused_outputs.append(output)
        
        return focused_outputs
    
    async def stream_transform(
        self,
        input_stream: asyncio.Queue,
        output_stream: asyncio.Queue,
        batch_size: int = 10
    ) -> None:
        """
        Asynchronously transform a stream of sensor readings.
        
        Args:
            input_stream: Queue of incoming SensorReading objects
            output_stream: Queue for outgoing FocusedOutput objects
            batch_size: Number of readings to batch process
        """
        batch = []
        
        while True:
            try:
                # Get reading with timeout
                reading = await asyncio.wait_for(
                    input_stream.get(),
                    timeout=1.0
                )
                
                if reading is None:  # Sentinel for stream end
                    break
                
                batch.append(reading)
                
                # Process batch when full
                if len(batch) >= batch_size:
                    focused = self.compress_readings(batch)
                    for output in focused:
                        await output_stream.put(output)
                    batch.clear()
                    
            except asyncio.TimeoutError:
                # Process partial batch on timeout
                if batch:
                    focused = self.compress_readings(batch)
                    for output in focused:
                        await output_stream.put(output)
                    batch.clear()
    
    def calculate_focal_efficiency(self, readings: List[SensorReading]) -> float:
        """
        Calculate how efficiently the aperture focuses energy.
        
        Uses the King's Chamber ratio (0.333) as optimal efficiency.
        
        Args:
            readings: List of sensor readings
            
        Returns:
            Efficiency score (0-1)
        """
        if not readings:
            return 0.0
        
        # Calculate concentration around focal angle
        focal_readings = [
            r for r in readings
            if abs(r.angle - self.config.focal_angle) < 45.0
        ]
        
        concentration = len(focal_readings) / len(readings)
        
        # Optimal concentration is at chamber ratio
        efficiency = 1.0 - abs(concentration - self.config.chamber_ratio)
        
        return max(0.0, min(1.0, efficiency))
    
    def get_compression_stats(self) -> dict:
        """Get statistics about the aperture configuration."""
        return {
            "input_range": self.config.input_range,
            "output_range": self.config.output_range,
            "compression_ratio": self.compression_ratio,
            "focal_angle": self.config.focal_angle,
            "chamber_ratio": self.config.chamber_ratio,
            "mode": self.config.mode
        }
