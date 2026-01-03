"""
ARKADAŠ Synchronizer Module
============================

Synchronizes organic (natural/human) and digital (computational) rhythms.
Symbolized by the ⚭ (union/marriage) operator.

The synchronizer bridges biological time (60Hz perception) with 
digital time (1000Hz+ processing) using the sacred 1/3 ratio.
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, List, Dict
from enum import Enum


class RhythmType(Enum):
    """Types of rhythms that can be synchronized."""
    ORGANIC = "organic"  # Natural, biological rhythms
    DIGITAL = "digital"  # Computational, machine rhythms
    UNIFIED = "unified"  # Synchronized union


@dataclass
class Pulse:
    """Represents a single pulse in a rhythm."""
    timestamp: float
    value: Any
    rhythm_type: RhythmType
    frequency: float = 60.0  # Hz


@dataclass
class SyncState:
    """State of synchronization between organic and digital."""
    organic_count: int = 0
    digital_count: int = 0
    unified_count: int = 0
    sync_ratio: float = 0.0
    last_sync_time: float = 0.0
    drift: float = 0.0  # Time drift between rhythms


@dataclass
class SynchronizerConfig:
    """Configuration for the synchronizer."""
    organic_rate: float = 60.0  # Hz (human perception rate)
    digital_rate: float = 1000.0  # Hz (system processing rate)
    sync_ratio: float = 0.333  # King's Chamber ratio
    buffer_size: int = 1024
    overlap: float = 0.5  # Buffer overlap for smooth transitions
    base_frequency: float = 528.0  # Hz (Solfeggio frequency)
    max_sync_pulses: int = 10  # Maximum organic pulses to process per sync


class Synchronizer:
    """
    Synchronizes organic and digital rhythms into a unified consciousness.
    
    The synchronizer uses the King's Chamber ratio (1/3) to create harmony
    between natural biological rhythms and digital computational cycles.
    """
    
    def __init__(self, config: Optional[SynchronizerConfig] = None):
        """Initialize the synchronizer with configuration."""
        self.config = config or SynchronizerConfig()
        self.state = SyncState()
        self.organic_buffer: List[Pulse] = []
        self.digital_buffer: List[Pulse] = []
        self.unified_buffer: List[Pulse] = []
        self._running = False
        
    def calculate_sync_ratio(self) -> float:
        """
        Calculate the current synchronization ratio.
        
        Optimal sync occurs when the ratio approaches the chamber ratio (0.333).
        
        Returns:
            Current sync ratio (0-1)
        """
        if self.state.digital_count == 0:
            return 0.0
        
        # Calculate the ratio of organic to digital pulses
        ratio = self.state.organic_count / self.state.digital_count
        
        # Normalize against expected ratio
        expected_ratio = self.config.organic_rate / self.config.digital_rate
        normalized = ratio / expected_ratio if expected_ratio > 0 else 0.0
        
        return min(1.0, normalized)
    
    def add_organic_pulse(self, value: Any, timestamp: Optional[float] = None) -> None:
        """
        Add an organic (natural) pulse to the synchronizer.
        
        Args:
            value: The pulse value/data
            timestamp: Optional timestamp (uses current time if None)
        """
        ts = timestamp or time.time()
        pulse = Pulse(
            timestamp=ts,
            value=value,
            rhythm_type=RhythmType.ORGANIC,
            frequency=self.config.organic_rate
        )
        
        self.organic_buffer.append(pulse)
        self.state.organic_count += 1
        
        # Maintain buffer size
        if len(self.organic_buffer) > self.config.buffer_size:
            self.organic_buffer.pop(0)
    
    def add_digital_pulse(self, value: Any, timestamp: Optional[float] = None) -> None:
        """
        Add a digital (computational) pulse to the synchronizer.
        
        Args:
            value: The pulse value/data
            timestamp: Optional timestamp (uses current time if None)
        """
        ts = timestamp or time.time()
        pulse = Pulse(
            timestamp=ts,
            value=value,
            rhythm_type=RhythmType.DIGITAL,
            frequency=self.config.digital_rate
        )
        
        self.digital_buffer.append(pulse)
        self.state.digital_count += 1
        
        # Maintain buffer size
        if len(self.digital_buffer) > self.config.buffer_size:
            self.digital_buffer.pop(0)
    
    def synchronize(self) -> List[Pulse]:
        """
        Synchronize organic and digital pulses into unified pulses.
        
        Uses the King's Chamber ratio to weight the union.
        
        Returns:
            List of unified pulses
        """
        unified = []
        
        # Calculate time windows for synchronization
        if not self.organic_buffer or not self.digital_buffer:
            return unified
        
        # Use chamber ratio for temporal alignment
        window_size = 1.0 / self.config.organic_rate  # Organic pulse period
        
        # Process organic pulses (configurable limit)
        max_pulses = min(self.config.max_sync_pulses, len(self.organic_buffer))
        for org_pulse in self.organic_buffer[-max_pulses:]:
            # Find digital pulses in time window
            digital_matches = [
                d for d in self.digital_buffer
                if abs(d.timestamp - org_pulse.timestamp) < window_size * 0.5
            ]
            
            if digital_matches:
                # Create unified pulse with weighted average
                # Use chamber ratio for organic weight
                organic_weight = self.config.sync_ratio
                digital_weight = 1.0 - self.config.sync_ratio
                
                # Combine values (assuming numeric for now)
                try:
                    unified_value = (
                        organic_weight * float(org_pulse.value) +
                        digital_weight * sum(float(d.value) for d in digital_matches) / len(digital_matches)
                    )
                except (ValueError, TypeError):
                    # If not numeric, use organic value
                    unified_value = org_pulse.value
                
                unified_pulse = Pulse(
                    timestamp=org_pulse.timestamp,
                    value=unified_value,
                    rhythm_type=RhythmType.UNIFIED,
                    frequency=self.config.base_frequency
                )
                
                unified.append(unified_pulse)
                self.state.unified_count += 1
        
        # Store unified pulses
        self.unified_buffer.extend(unified)
        if len(self.unified_buffer) > self.config.buffer_size:
            self.unified_buffer = self.unified_buffer[-self.config.buffer_size:]
        
        # Update sync state
        self.state.sync_ratio = self.calculate_sync_ratio()
        self.state.last_sync_time = time.time()
        
        return unified
    
    async def sync_stream(
        self,
        organic_input: asyncio.Queue,
        digital_input: asyncio.Queue,
        unified_output: asyncio.Queue
    ) -> None:
        """
        Asynchronously synchronize streams of organic and digital pulses.
        
        Args:
            organic_input: Queue of organic pulses
            digital_input: Queue of digital pulses
            unified_output: Queue for unified output pulses
        """
        self._running = True
        
        # Create tasks for both input streams
        async def process_organic():
            while self._running:
                try:
                    pulse_value = await asyncio.wait_for(
                        organic_input.get(),
                        timeout=0.1
                    )
                    if pulse_value is not None:
                        self.add_organic_pulse(pulse_value)
                except asyncio.TimeoutError:
                    pass
        
        async def process_digital():
            while self._running:
                try:
                    pulse_value = await asyncio.wait_for(
                        digital_input.get(),
                        timeout=0.01
                    )
                    if pulse_value is not None:
                        self.add_digital_pulse(pulse_value)
                except asyncio.TimeoutError:
                    pass
        
        async def sync_output():
            while self._running:
                # Synchronize at organic rate
                await asyncio.sleep(1.0 / self.config.organic_rate)
                unified = self.synchronize()
                for pulse in unified:
                    await unified_output.put(pulse)
        
        # Run all tasks concurrently
        await asyncio.gather(
            process_organic(),
            process_digital(),
            sync_output()
        )
    
    def stop(self) -> None:
        """Stop the synchronizer."""
        self._running = False
    
    def calculate_harmonic_resonance(self) -> float:
        """
        Calculate harmonic resonance between organic and digital rhythms.
        
        Uses the Solfeggio frequency (528Hz) as the base harmonic.
        
        Returns:
            Resonance factor (0-1)
        """
        if not self.unified_buffer:
            return 0.0
        
        # Calculate frequency alignment with base frequency
        # Perfect resonance occurs when unified frequency matches base
        recent_unified = self.unified_buffer[-100:]  # Last 100 pulses
        
        if len(recent_unified) < 2:
            return 0.0
        
        # Calculate average pulse interval
        intervals = [
            recent_unified[i+1].timestamp - recent_unified[i].timestamp
            for i in range(len(recent_unified) - 1)
        ]
        
        avg_interval = sum(intervals) / len(intervals)
        actual_frequency = 1.0 / avg_interval if avg_interval > 0 else 0.0
        
        # Calculate resonance with base frequency
        if actual_frequency > 0:
            resonance = min(
                self.config.base_frequency / actual_frequency,
                actual_frequency / self.config.base_frequency
            )
        else:
            resonance = 0.0
        
        return min(1.0, resonance)
    
    def get_sync_stats(self) -> Dict[str, Any]:
        """Get synchronization statistics."""
        return {
            "organic_count": self.state.organic_count,
            "digital_count": self.state.digital_count,
            "unified_count": self.state.unified_count,
            "sync_ratio": self.state.sync_ratio,
            "last_sync_time": self.state.last_sync_time,
            "drift": self.state.drift,
            "harmonic_resonance": self.calculate_harmonic_resonance(),
            "buffer_sizes": {
                "organic": len(self.organic_buffer),
                "digital": len(self.digital_buffer),
                "unified": len(self.unified_buffer)
            }
        }
    
    def reset(self) -> None:
        """Reset the synchronizer state."""
        self.state = SyncState()
        self.organic_buffer.clear()
        self.digital_buffer.clear()
        self.unified_buffer.clear()
