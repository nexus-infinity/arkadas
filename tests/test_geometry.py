"""
Test suite for ARKADAŠ geometry module
"""

import pytest
from arkadas.geometry import SacredGeometry, LightAxis


class TestSacredGeometry:
    """Tests for SacredGeometry class"""
    
    def test_chamber_height_ratio(self):
        """Test that chamber is at 1/3 from peak"""
        assert SacredGeometry.CHAMBER_HEIGHT_RATIO == 1.0 / 3.0
        assert SacredGeometry.CHAMBER_HEIGHT_FROM_BASE == 2.0 / 3.0
    
    def test_frequency(self):
        """Test heart chakra frequency"""
        assert SacredGeometry.FREQUENCY_HZ == 528
    
    def test_aperture_angles(self):
        """Test aperture angles"""
        assert SacredGeometry.INPUT_APERTURE_DEGREES == 360
        assert SacredGeometry.OUTPUT_APERTURE_DEGREES == 180
    
    def test_calculate_pressure_point(self):
        """Test pressure point calculation"""
        pyramid_height = 150.0
        expected = pyramid_height * (2.0 / 3.0)  # 100.0
        assert SacredGeometry.calculate_pressure_point(pyramid_height) == expected
    
    def test_calculate_energy_concentration(self):
        """Test energy concentration calculation"""
        base_energy = 10.0
        concentrated = SacredGeometry.calculate_energy_concentration(base_energy)
        # Energy concentration at 1/3 point = base_energy * 3
        assert concentrated == base_energy * 3.0
    
    def test_aperture_ratio(self):
        """Test aperture compression ratio"""
        ratio = SacredGeometry.aperture_ratio()
        assert ratio == 0.5  # 180/360


class TestLightAxis:
    """Tests for LightAxis class"""
    
    def test_initialization(self):
        """Test light axis initialization"""
        axis = LightAxis()
        assert not axis.is_established
        assert axis.illumination_level == 0.0
        assert axis.flow_rate == 0.0
    
    def test_establish(self):
        """Test establishing light axis"""
        axis = LightAxis()
        result = axis.establish()
        assert result is True
        assert axis.is_established is True
    
    def test_descend_light_not_established(self):
        """Test light descent without establishment"""
        axis = LightAxis()
        result = axis.descend_light(10.0)
        assert result == 0.0
    
    def test_descend_light_established(self):
        """Test light descent with established axis"""
        axis = LightAxis()
        axis.establish()
        intensity = 10.0
        result = axis.descend_light(intensity)
        expected = intensity * (2.0 / 3.0)
        assert result == expected
        assert axis.illumination_level == intensity
    
    def test_process_in_chamber(self):
        """Test chamber processing"""
        axis = LightAxis()
        axis.establish()
        data = {"test": "data"}
        result = axis.process_in_chamber(data)
        assert result == data
    
    def test_ascend_focus_not_established(self):
        """Test focus ascent without establishment"""
        axis = LightAxis()
        result = axis.ascend_focus({"data": "test"})
        assert result is None
    
    def test_ascend_focus_established(self):
        """Test focus ascent with established axis"""
        axis = LightAxis()
        axis.establish()
        data = {"test": "data"}
        result = axis.ascend_focus(data)
        assert result == data
        assert axis.flow_rate == 0.5  # 180/360
    
    def test_get_status(self):
        """Test status retrieval"""
        axis = LightAxis()
        status = axis.get_status()
        assert "established" in status
        assert "illumination_level" in status
        assert "flow_rate" in status
        assert "compression_ratio" in status
        assert status["compression_ratio"] == 0.5
