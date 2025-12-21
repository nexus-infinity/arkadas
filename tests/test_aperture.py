"""
Test suite for ARKADAŠ aperture sensing module
"""

import pytest
from arkadas.aperture import ApertureSensing, SensorReading


class TestApertureSensing:
    """Tests for ApertureSensing class"""
    
    def test_initialization(self):
        """Test aperture sensing initialization"""
        aperture = ApertureSensing()
        assert len(aperture.input_buffer) == 0
        assert len(aperture.output_buffer) == 0
        assert not aperture.is_active
        assert aperture.total_received == 0
        assert aperture.total_processed == 0
    
    def test_start_stop(self):
        """Test starting and stopping aperture"""
        aperture = ApertureSensing()
        
        aperture.start()
        assert aperture.is_active
        
        aperture.stop()
        assert not aperture.is_active
    
    def test_receive_360_inactive(self):
        """Test receiving when inactive"""
        aperture = ApertureSensing()
        result = aperture.receive_360(90, "test_data")
        assert result is False
        assert aperture.total_received == 0
    
    def test_receive_360_active(self):
        """Test receiving when active"""
        aperture = ApertureSensing()
        aperture.start()
        
        result = aperture.receive_360(90, "test_data", "source1")
        assert result is True
        assert aperture.total_received == 1
        assert len(aperture.input_buffer) == 1
        
        reading = aperture.input_buffer[0]
        assert reading.angle == 90
        assert reading.data == "test_data"
        assert reading.source_id == "source1"
    
    def test_angle_normalization(self):
        """Test angle normalization to 0-360 range"""
        aperture = ApertureSensing()
        aperture.start()
        
        # Test angle > 360
        aperture.receive_360(450, "data1")
        assert aperture.input_buffer[0].angle == 90  # 450 % 360
        
        # Test negative angle
        aperture.receive_360(-90, "data2")
        assert aperture.input_buffer[1].angle == 270  # -90 % 360
    
    def test_process_aperture_empty(self):
        """Test processing with empty buffer"""
        aperture = ApertureSensing()
        aperture.start()
        
        result = aperture.process_aperture()
        assert len(result) == 0
    
    def test_process_aperture_with_data(self):
        """Test processing with data"""
        aperture = ApertureSensing()
        aperture.start()
        
        # Add multiple readings
        aperture.receive_360(0, "north")
        aperture.receive_360(90, "east")
        aperture.receive_360(180, "south")
        aperture.receive_360(270, "west")
        
        result = aperture.process_aperture()
        
        assert len(result) == 4
        assert aperture.total_processed == 4
        assert len(aperture.input_buffer) == 0  # Should be cleared
        assert len(aperture.output_buffer) == 4
    
    def test_focused_output_structure(self):
        """Test structure of focused output"""
        aperture = ApertureSensing()
        aperture.start()
        
        aperture.receive_360(45, "test_data")
        result = aperture.process_aperture()
        
        assert len(result) == 1
        focused = result[0]
        
        assert "original_angle" in focused
        assert "data" in focused
        assert "timestamp" in focused
        assert "focused" in focused
        assert "upward_vector" in focused
        assert focused["focused"] is True
        assert focused["original_angle"] == 45
    
    def test_upward_vector_calculation(self):
        """Test upward vector calculation"""
        aperture = ApertureSensing()
        aperture.start()
        
        aperture.receive_360(0, "data")
        result = aperture.process_aperture()
        
        vector = result[0]["upward_vector"]
        assert "azimuth" in vector
        assert "elevation" in vector
        assert "x" in vector
        assert "y" in vector
        assert "z" in vector
        assert vector["z"] == 1.0  # Upward component
        assert vector["elevation"] == 45.0  # Default elevation
    
    def test_get_focused_output(self):
        """Test getting focused output"""
        aperture = ApertureSensing()
        aperture.start()
        
        aperture.receive_360(0, "data1")
        aperture.process_aperture()
        
        output = aperture.get_focused_output()
        assert len(output) == 1
        assert len(aperture.output_buffer) == 0  # Should be cleared
    
    def test_get_metrics(self):
        """Test metrics retrieval"""
        aperture = ApertureSensing()
        aperture.start()
        
        aperture.receive_360(0, "data1")
        aperture.receive_360(90, "data2")
        aperture.process_aperture()
        
        metrics = aperture.get_metrics()
        assert metrics["active"] is True
        assert metrics["total_received"] == 2
        assert metrics["total_processed"] == 2
        assert metrics["processing_rate"] == 1.0
    
    def test_get_status(self):
        """Test status retrieval"""
        aperture = ApertureSensing()
        assert aperture.get_status() == "INACTIVE"
        
        aperture.start()
        assert aperture.get_status() == "ACTIVE"
