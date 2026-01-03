"""Tests for the ARKADAŠ Synchronizer module."""

import pytest
import asyncio
import time
from synchronizer import (
    Synchronizer,
    SynchronizerConfig,
    Pulse,
    RhythmType,
    SyncState
)


class TestSynchronizerConfig:
    """Test SynchronizerConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = SynchronizerConfig()
        assert config.organic_rate == 60.0
        assert config.digital_rate == 1000.0
        assert config.sync_ratio == 0.333
        assert config.buffer_size == 1024
        assert config.overlap == 0.5
        assert config.base_frequency == 528.0
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = SynchronizerConfig(
            organic_rate=30.0,
            digital_rate=500.0,
            sync_ratio=0.5,
            base_frequency=440.0
        )
        assert config.organic_rate == 30.0
        assert config.digital_rate == 500.0
        assert config.sync_ratio == 0.5
        assert config.base_frequency == 440.0


class TestPulse:
    """Test Pulse dataclass."""
    
    def test_pulse_creation(self):
        """Test creating a pulse."""
        pulse = Pulse(
            timestamp=time.time(),
            value=42,
            rhythm_type=RhythmType.ORGANIC,
            frequency=60.0
        )
        assert pulse.value == 42
        assert pulse.rhythm_type == RhythmType.ORGANIC
        assert pulse.frequency == 60.0


class TestSynchronizer:
    """Test Synchronizer class."""
    
    def test_synchronizer_initialization(self):
        """Test synchronizer initialization."""
        sync = Synchronizer()
        assert sync.config.organic_rate == 60.0
        assert sync.config.digital_rate == 1000.0
        assert len(sync.organic_buffer) == 0
        assert len(sync.digital_buffer) == 0
        assert sync.state.organic_count == 0
        assert sync.state.digital_count == 0
    
    def test_add_organic_pulse(self):
        """Test adding organic pulses."""
        sync = Synchronizer()
        
        sync.add_organic_pulse(1.0)
        sync.add_organic_pulse(2.0)
        
        assert len(sync.organic_buffer) == 2
        assert sync.state.organic_count == 2
        assert sync.organic_buffer[0].value == 1.0
        assert sync.organic_buffer[0].rhythm_type == RhythmType.ORGANIC
    
    def test_add_digital_pulse(self):
        """Test adding digital pulses."""
        sync = Synchronizer()
        
        sync.add_digital_pulse(10.0)
        sync.add_digital_pulse(20.0)
        sync.add_digital_pulse(30.0)
        
        assert len(sync.digital_buffer) == 3
        assert sync.state.digital_count == 3
        assert sync.digital_buffer[0].value == 10.0
        assert sync.digital_buffer[0].rhythm_type == RhythmType.DIGITAL
    
    def test_buffer_size_limit(self):
        """Test that buffers respect size limits."""
        config = SynchronizerConfig(buffer_size=10)
        sync = Synchronizer(config)
        
        # Add more pulses than buffer can hold
        for i in range(20):
            sync.add_organic_pulse(float(i))
        
        # Buffer should be limited
        assert len(sync.organic_buffer) == 10
        # But count should be accurate
        assert sync.state.organic_count == 20
    
    def test_calculate_sync_ratio_no_digital(self):
        """Test sync ratio calculation with no digital pulses."""
        sync = Synchronizer()
        sync.add_organic_pulse(1.0)
        
        ratio = sync.calculate_sync_ratio()
        assert ratio == 0.0
    
    def test_calculate_sync_ratio_with_pulses(self):
        """Test sync ratio calculation with both pulse types."""
        sync = Synchronizer()
        
        # Add pulses
        for i in range(10):
            sync.add_organic_pulse(float(i))
        
        for i in range(100):
            sync.add_digital_pulse(float(i))
        
        ratio = sync.calculate_sync_ratio()
        assert 0.0 <= ratio <= 1.0
    
    def test_synchronize_empty_buffers(self):
        """Test synchronization with empty buffers."""
        sync = Synchronizer()
        unified = sync.synchronize()
        assert len(unified) == 0
    
    def test_synchronize_only_organic(self):
        """Test synchronization with only organic pulses."""
        sync = Synchronizer()
        
        for i in range(5):
            sync.add_organic_pulse(float(i))
        
        unified = sync.synchronize()
        # Should be empty without digital pulses
        assert len(unified) == 0
    
    def test_synchronize_both_types(self):
        """Test synchronization with both pulse types."""
        sync = Synchronizer()
        
        current_time = time.time()
        
        # Add synchronized pulses
        for i in range(5):
            ts = current_time + i * 0.01
            sync.add_organic_pulse(10.0 + i, timestamp=ts)
            sync.add_digital_pulse(20.0 + i, timestamp=ts)
        
        unified = sync.synchronize()
        
        # Should create unified pulses
        assert len(unified) > 0
        assert all(p.rhythm_type == RhythmType.UNIFIED for p in unified)
    
    def test_synchronize_chamber_ratio_weighting(self):
        """Test that synchronization uses chamber ratio for weighting."""
        sync = Synchronizer()
        
        current_time = time.time()
        
        # Add pulses with known values
        sync.add_organic_pulse(100.0, timestamp=current_time)
        sync.add_digital_pulse(200.0, timestamp=current_time)
        
        unified = sync.synchronize()
        
        if unified:
            # Unified value should be weighted average
            # organic_weight = 0.333, digital_weight = 0.667
            expected = 0.333 * 100.0 + 0.667 * 200.0
            # Allow some tolerance
            assert abs(unified[0].value - expected) < 10.0
    
    def test_calculate_harmonic_resonance_empty(self):
        """Test harmonic resonance with empty buffer."""
        sync = Synchronizer()
        resonance = sync.calculate_harmonic_resonance()
        assert resonance == 0.0
    
    def test_calculate_harmonic_resonance_with_data(self):
        """Test harmonic resonance calculation."""
        sync = Synchronizer()
        
        current_time = time.time()
        
        # Add pulses at regular intervals
        for i in range(10):
            ts = current_time + i * 0.01
            sync.add_organic_pulse(1.0, timestamp=ts)
            sync.add_digital_pulse(1.0, timestamp=ts)
        
        unified = sync.synchronize()
        
        if len(unified) >= 2:
            resonance = sync.calculate_harmonic_resonance()
            assert 0.0 <= resonance <= 1.0
    
    def test_get_sync_stats(self):
        """Test getting synchronization statistics."""
        sync = Synchronizer()
        
        sync.add_organic_pulse(1.0)
        sync.add_digital_pulse(2.0)
        
        stats = sync.get_sync_stats()
        
        assert "organic_count" in stats
        assert "digital_count" in stats
        assert "unified_count" in stats
        assert "sync_ratio" in stats
        assert "harmonic_resonance" in stats
        assert "buffer_sizes" in stats
        
        assert stats["organic_count"] == 1
        assert stats["digital_count"] == 1
    
    def test_reset(self):
        """Test resetting the synchronizer."""
        sync = Synchronizer()
        
        # Add some data
        sync.add_organic_pulse(1.0)
        sync.add_digital_pulse(2.0)
        sync.synchronize()
        
        # Reset
        sync.reset()
        
        # Everything should be cleared
        assert len(sync.organic_buffer) == 0
        assert len(sync.digital_buffer) == 0
        assert len(sync.unified_buffer) == 0
        assert sync.state.organic_count == 0
        assert sync.state.digital_count == 0
        assert sync.state.unified_count == 0
    
    def test_stop(self):
        """Test stopping the synchronizer."""
        sync = Synchronizer()
        sync._running = True
        sync.stop()
        assert sync._running is False


class TestSynchronizerAsync:
    """Test async functionality of Synchronizer."""
    
    @pytest.mark.asyncio
    async def test_sync_stream_basic(self):
        """Test basic stream synchronization."""
        sync = Synchronizer()
        
        organic_input = asyncio.Queue()
        digital_input = asyncio.Queue()
        unified_output = asyncio.Queue()
        
        # Add some test pulses
        for i in range(3):
            await organic_input.put(float(i))
            await digital_input.put(float(i * 10))
        
        # Run for a short time
        sync_task = asyncio.create_task(
            sync.sync_stream(organic_input, digital_input, unified_output)
        )
        
        # Let it run briefly
        await asyncio.sleep(0.2)
        
        # Stop and cancel
        sync.stop()
        sync_task.cancel()
        
        try:
            await sync_task
        except asyncio.CancelledError:
            pass
        
        # Should have processed some pulses
        assert sync.state.organic_count > 0 or sync.state.digital_count > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
