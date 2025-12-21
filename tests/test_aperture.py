"""Tests for the ARKADAŠ Aperture module."""

import pytest
import asyncio
from aperture import (
    Aperture,
    ApertureConfig,
    SensorReading,
    FocusedOutput
)


class TestApertureConfig:
    """Test ApertureConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ApertureConfig()
        assert config.input_range == 360.0
        assert config.output_range == 180.0
        assert config.focal_angle == 90.0
        assert config.mode == "harmonic_compression"
        assert config.chamber_ratio == 0.333
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = ApertureConfig(
            input_range=720.0,
            output_range=90.0,
            focal_angle=45.0,
            chamber_ratio=0.5
        )
        assert config.input_range == 720.0
        assert config.output_range == 90.0
        assert config.focal_angle == 45.0
        assert config.chamber_ratio == 0.5


class TestSensorReading:
    """Test SensorReading dataclass."""
    
    def test_sensor_reading_creation(self):
        """Test creating a sensor reading."""
        reading = SensorReading(angle=45.0, intensity=0.8)
        assert reading.angle == 45.0
        assert reading.intensity == 0.8
        assert reading.timestamp == 0.0
        assert reading.sensor_type == "generic"


class TestAperture:
    """Test Aperture class."""
    
    def test_aperture_initialization(self):
        """Test aperture initialization."""
        aperture = Aperture()
        assert aperture.config.input_range == 360.0
        assert aperture.compression_ratio == 2.0
    
    def test_custom_aperture(self):
        """Test aperture with custom config."""
        config = ApertureConfig(input_range=720.0, output_range=180.0)
        aperture = Aperture(config)
        assert aperture.compression_ratio == 4.0
    
    def test_transform_angle_basic(self):
        """Test basic angle transformation."""
        aperture = Aperture()
        
        # Test focal angle (90°)
        output = aperture.transform_angle(90.0)
        assert 0.0 <= output <= 180.0
        
        # Test opposite side (270°)
        output = aperture.transform_angle(270.0)
        assert 0.0 <= output <= 180.0
    
    def test_transform_angle_wrapping(self):
        """Test angle wrapping at 360°."""
        aperture = Aperture()
        
        # Test angles beyond 360°
        output1 = aperture.transform_angle(370.0)
        output2 = aperture.transform_angle(10.0)
        assert abs(output1 - output2) < 1.0  # Should be similar
    
    def test_compress_readings_empty(self):
        """Test compressing empty readings list."""
        aperture = Aperture()
        focused = aperture.compress_readings([])
        assert len(focused) == 0
    
    def test_compress_readings_single(self):
        """Test compressing a single reading."""
        aperture = Aperture()
        readings = [SensorReading(angle=90.0, intensity=0.5)]
        focused = aperture.compress_readings(readings, resolution=10.0)
        
        assert len(focused) > 0
        assert all(isinstance(f, FocusedOutput) for f in focused)
    
    def test_compress_readings_multiple(self):
        """Test compressing multiple readings."""
        aperture = Aperture()
        
        # Create readings around the full circle
        readings = [
            SensorReading(angle=i * 30.0, intensity=0.5)
            for i in range(12)
        ]
        
        focused = aperture.compress_readings(readings, resolution=10.0)
        
        # Should have some focused outputs
        assert len(focused) > 0
        
        # All outputs should be in 0-180° range
        for output in focused:
            assert 0.0 <= output.angle < 180.0
    
    def test_compress_readings_intensity_enhancement(self):
        """Test that intensity is enhanced by chamber ratio."""
        aperture = Aperture()
        
        # Create reading with known intensity
        readings = [SensorReading(angle=90.0, intensity=0.6)]
        focused = aperture.compress_readings(readings, resolution=10.0)
        
        # Enhanced intensity should be higher than original
        if focused:
            assert focused[0].intensity >= 0.6
    
    def test_calculate_focal_efficiency(self):
        """Test focal efficiency calculation."""
        aperture = Aperture()
        
        # All readings near focal point
        readings = [
            SensorReading(angle=90.0 + i, intensity=0.5)
            for i in range(-20, 21)
        ]
        
        efficiency = aperture.calculate_focal_efficiency(readings)
        assert 0.0 <= efficiency <= 1.0
        
        # Should be high since all readings are near focal point
        assert efficiency > 0.5
    
    def test_calculate_focal_efficiency_dispersed(self):
        """Test focal efficiency with dispersed readings."""
        aperture = Aperture()
        
        # Readings spread across full circle
        readings = [
            SensorReading(angle=i * 30.0, intensity=0.5)
            for i in range(12)
        ]
        
        efficiency = aperture.calculate_focal_efficiency(readings)
        assert 0.0 <= efficiency <= 1.0
        
        # Should be lower for dispersed readings
        assert efficiency < 0.8
    
    def test_get_compression_stats(self):
        """Test getting compression statistics."""
        config = ApertureConfig(
            input_range=360.0,
            output_range=180.0,
            focal_angle=90.0
        )
        aperture = Aperture(config)
        
        stats = aperture.get_compression_stats()
        
        assert stats["input_range"] == 360.0
        assert stats["output_range"] == 180.0
        assert stats["compression_ratio"] == 2.0
        assert stats["focal_angle"] == 90.0
        assert stats["chamber_ratio"] == 0.333
        assert stats["mode"] == "harmonic_compression"


class TestApertureAsync:
    """Test async functionality of Aperture."""
    
    @pytest.mark.asyncio
    async def test_stream_transform(self):
        """Test asynchronous stream transformation."""
        aperture = Aperture()
        
        input_stream = asyncio.Queue()
        output_stream = asyncio.Queue()
        
        # Add some test readings
        for i in range(5):
            await input_stream.put(
                SensorReading(angle=i * 72.0, intensity=0.5)
            )
        
        # Add sentinel to end stream
        await input_stream.put(None)
        
        # Run transformation
        await aperture.stream_transform(
            input_stream,
            output_stream,
            batch_size=5
        )
        
        # Check output
        output_count = 0
        while not output_stream.empty():
            output = await output_stream.get()
            assert isinstance(output, FocusedOutput)
            output_count += 1
        
        # Should have at least one output
        assert output_count > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
