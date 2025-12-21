"""
Tests for aperture module (360° to 180° conversion).
"""

import pytest
from chamber.aperture import ApertureConverter


class TestApertureConverter:
    """Test suite for ApertureConverter."""
    
    def test_initialization(self):
        """Test aperture converter initialization."""
        aperture = ApertureConverter(focus_direction=45.0)
        assert aperture.focus_direction == 45.0
        assert aperture.aperture_width == 180
        
    def test_normalize_direction(self):
        """Test direction normalization."""
        aperture = ApertureConverter(focus_direction=400.0)
        assert aperture.focus_direction == 40.0  # 400 % 360
        
    def test_convert_360_to_180(self):
        """Test conversion from 360° to 180°."""
        aperture = ApertureConverter(focus_direction=0.0)
        
        # Test data: full circle with values
        sensor_data = {
            0.0: 1.0,
            45.0: 0.8,
            90.0: 0.6,
            135.0: 0.4,
            180.0: 0.2,
            225.0: 0.4,
            270.0: 0.6,
            315.0: 0.8
        }
        
        focused = aperture.convert(sensor_data)
        
        # Should contain front hemisphere (roughly -90° to +90° from focus)
        assert len(focused) > 0
        assert all(0 <= angle <= 180 for angle in focused.keys())
        
    def test_get_focus_range(self):
        """Test getting focus range."""
        aperture = ApertureConverter(focus_direction=90.0)
        start, end = aperture.get_focus_range()
        
        # 90° focus with 180° aperture: 0° to 180°
        assert start == 0.0
        assert end == 180.0
        
    def test_set_focus_direction(self):
        """Test setting new focus direction."""
        aperture = ApertureConverter(focus_direction=0.0)
        aperture.set_focus_direction(180.0)
        assert aperture.focus_direction == 180.0
        
    def test_calculate_intensity(self):
        """Test intensity calculation."""
        aperture = ApertureConverter()
        
        focused_data = {
            0.0: 1.0,
            45.0: 0.8,
            90.0: 0.6
        }
        
        intensity = aperture.calculate_intensity(focused_data)
        expected = (1.0 + 0.8 + 0.6) / 3
        assert abs(intensity - expected) < 0.001
        
    def test_empty_data(self):
        """Test handling of empty data."""
        aperture = ApertureConverter()
        focused = aperture.convert({})
        assert focused == {}
        assert aperture.calculate_intensity({}) == 0.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
