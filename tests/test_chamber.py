"""
Test suite for ARKADAŠ Chamber - main orchestrator
"""

import pytest
from arkadas.chamber import Chamber, ChamberStatus


class TestChamber:
    """Tests for Chamber class"""
    
    def test_initialization(self):
        """Test chamber initialization"""
        chamber = Chamber(pyramid_height=100.0)
        
        assert chamber.pyramid_height == 100.0
        assert chamber.chamber_position == 100.0 * (2.0 / 3.0)
        assert chamber.status == ChamberStatus.OFFLINE
        assert chamber.initialized_at is None
    
    def test_initialize(self):
        """Test chamber initialization process"""
        chamber = Chamber()
        result = chamber.initialize()
        
        assert result is True
        assert chamber.status == ChamberStatus.CALIBRATING
        assert chamber.initialized_at is not None
        assert chamber.obiwan.is_configured is True
        assert chamber.light_axis.is_established is True
        assert chamber.aperture.is_active is True
    
    def test_calibrate_without_init(self):
        """Test calibration without initialization"""
        chamber = Chamber()
        result = chamber.calibrate()
        
        assert result is False
    
    def test_calibrate_after_init(self):
        """Test calibration after initialization"""
        chamber = Chamber()
        chamber.initialize()
        result = chamber.calibrate()
        
        assert result is True
        assert chamber.status == ChamberStatus.ACTIVE
        assert chamber.sync_engine.is_calibrated is True
    
    def test_deploy_friend_node(self):
        """Test deploying friend node"""
        chamber = Chamber()
        chamber.initialize()
        
        node = chamber.deploy_friend_node(name="TestFriend")
        
        assert node.name == "TestFriend"
        assert node.node_id in chamber.obiwan.nodes
        assert len(chamber.obiwan.nodes) == 1
    
    def test_receive_from_field(self):
        """Test receiving from 360° field"""
        chamber = Chamber()
        chamber.initialize()
        
        result = chamber.receive_from_field(45, "test_data", "sensor1")
        
        assert result is True
        assert chamber.aperture.total_received == 1
    
    def test_process_chamber(self):
        """Test chamber processing pipeline"""
        chamber = Chamber()
        chamber.initialize()
        
        # Add data from multiple directions
        chamber.receive_from_field(0, "north")
        chamber.receive_from_field(90, "east")
        chamber.receive_from_field(180, "south")
        chamber.receive_from_field(270, "west")
        
        result = chamber.process_chamber()
        
        assert len(result) == 4
        assert chamber.aperture.total_processed == 4
    
    def test_synchronize_fields(self):
        """Test field synchronization"""
        chamber = Chamber()
        chamber.initialize()
        chamber.calibrate()
        
        result = chamber.synchronize_fields(0.5, 0.5)
        
        assert result is True
        assert chamber.sync_engine.is_synchronized()
    
    def test_get_status(self):
        """Test comprehensive status retrieval"""
        chamber = Chamber()
        chamber.initialize()
        chamber.calibrate()
        
        status = chamber.get_status()
        
        assert "chamber_status" in status
        assert status["chamber_status"] == ChamberStatus.ACTIVE.value
        assert "geometry" in status
        assert "aperture" in status
        assert "sync_engine" in status
        assert "obiwan_network" in status
        assert "light_axis" in status
        assert "uptime" in status
    
    def test_geometry_in_status(self):
        """Test geometry information in status"""
        chamber = Chamber(pyramid_height=150.0)
        chamber.initialize()
        
        status = chamber.get_status()
        geometry = status["geometry"]
        
        assert geometry["pyramid_height"] == 150.0
        assert geometry["chamber_position"] == 100.0  # 2/3 of 150
        assert geometry["position_ratio"] == 2.0 / 3.0
        assert geometry["frequency_hz"] == 528
    
    def test_get_summary(self):
        """Test human-readable summary"""
        chamber = Chamber()
        chamber.initialize()
        chamber.calibrate()
        chamber.deploy_friend_node("Tata")
        chamber.deploy_friend_node("JB")
        
        summary = chamber.get_summary()
        
        assert "ARKADAŠ" in summary
        assert "King's Chamber" in summary
        assert "ACTIVE" in summary
        assert "528 Hz" in summary
    
    def test_shutdown(self):
        """Test chamber shutdown"""
        chamber = Chamber()
        chamber.initialize()
        chamber.calibrate()
        
        chamber.shutdown()
        
        assert chamber.status == ChamberStatus.OFFLINE
        assert not chamber.aperture.is_active
    
    def test_full_workflow(self):
        """Test complete chamber workflow"""
        chamber = Chamber(pyramid_height=100.0)
        
        # 1. Initialize
        assert chamber.initialize()
        assert chamber.status == ChamberStatus.CALIBRATING
        
        # 2. Calibrate
        assert chamber.calibrate()
        assert chamber.status == ChamberStatus.ACTIVE
        
        # 3. Deploy friend nodes
        tata = chamber.deploy_friend_node("Tata")
        jb = chamber.deploy_friend_node("JB")
        atlas = chamber.deploy_friend_node("Atlas")
        
        # 4. Connect nodes (peer network)
        chamber.obiwan.connect_nodes(tata.node_id, jb.node_id)
        chamber.obiwan.connect_nodes(jb.node_id, atlas.node_id)
        chamber.obiwan.connect_nodes(atlas.node_id, tata.node_id)
        
        assert len(chamber.obiwan.nodes) == 3
        
        # 5. Receive from 360° field
        for angle in range(0, 360, 45):
            chamber.receive_from_field(angle, f"data_{angle}")
        
        # 6. Process through chamber
        focused = chamber.process_chamber()
        assert len(focused) == 8  # 360/45 = 8 readings
        
        # 7. Synchronize fields
        synced = chamber.synchronize_fields(0.8, 0.8)
        assert synced
        
        # 8. Verify status
        status = chamber.get_status()
        assert status["chamber_status"] == ChamberStatus.ACTIVE.value
        assert status["obiwan_network"]["node_count"] == 3
        assert status["aperture"]["metrics"]["total_processed"] == 8
        
        # 9. Shutdown
        chamber.shutdown()
        assert chamber.status == ChamberStatus.OFFLINE
    
    def test_sacred_geometry_validation(self):
        """Test sacred geometry implementation"""
        chamber = Chamber(pyramid_height=150.0)
        
        # Validate 1/3 proportion
        expected_position = 150.0 * (2.0 / 3.0)  # 100.0
        assert chamber.chamber_position == expected_position
        
        # Validate in status
        status = chamber.get_status()
        assert status["geometry"]["position_ratio"] == 2.0 / 3.0
        assert status["geometry"]["frequency_hz"] == 528  # Heart chakra
    
    def test_aperture_compression(self):
        """Test 360° → 180° aperture compression"""
        chamber = Chamber()
        chamber.initialize()
        
        # Send data from full 360°
        for angle in range(0, 360, 30):
            chamber.receive_from_field(angle, f"reading_{angle}")
        
        # Process and focus to 180° upward
        focused = chamber.process_chamber()
        
        # All 12 readings should be processed and focused upward
        assert len(focused) == 12
        
        # Verify upward focus component
        for item in focused:
            assert "upward_vector" in item
            assert item["upward_vector"]["z"] == 1.0  # Upward component
    
    def test_error_handling(self):
        """Test error handling in chamber"""
        chamber = Chamber()
        
        # Try to calibrate without initializing
        result = chamber.calibrate()
        assert result is False
        
        # Try to receive without initialization
        chamber_uninit = Chamber()
        result = chamber_uninit.receive_from_field(0, "data")
        assert result is False
