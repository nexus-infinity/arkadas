"""
Tests for OBI-WAN observation network.
"""

import pytest
from obi_wan.sensor_array import SensorArray, Sensor
from obi_wan.metrics import MetricsInterface
from obi_wan.feedback import FeedbackLayer, FeedbackType
from obi_wan.wan_network import WANCoordinator


class TestSensor:
    """Test suite for individual Sensor."""
    
    def test_sensor_creation(self):
        """Test sensor initialization."""
        sensor = Sensor("sensor_01", 45.0, sensitivity=1.5)
        assert sensor.sensor_id == "sensor_01"
        assert sensor.angle == 45.0
        assert sensor.sensitivity == 1.5
        assert sensor.active is True
        
    def test_sensor_read(self):
        """Test sensor reading."""
        sensor = Sensor("sensor_01", 0.0, sensitivity=2.0)
        reading = sensor.read(0.5)
        assert reading == 1.0  # 0.5 * 2.0
        assert sensor.last_reading == 1.0
        
    def test_inactive_sensor(self):
        """Test inactive sensor returns 0."""
        sensor = Sensor("sensor_01", 0.0)
        sensor.active = False
        reading = sensor.read(0.5)
        assert reading == 0.0


class TestSensorArray:
    """Test suite for SensorArray."""
    
    def test_array_initialization(self):
        """Test sensor array initialization."""
        array = SensorArray(num_sensors=12)
        assert array.num_sensors == 12
        assert len(array.sensors) == 12
        
    def test_sensor_distribution(self):
        """Test sensors are evenly distributed."""
        array = SensorArray(num_sensors=36)
        angles = [s.angle for s in array.sensors]
        
        # Should be evenly spaced at 10° intervals
        assert angles[0] == 0.0
        assert abs(angles[1] - 10.0) < 0.01
        assert abs(angles[-1] - 350.0) < 0.01
        
    def test_sense_360(self):
        """Test 360° sensing."""
        array = SensorArray(num_sensors=36)
        readings = array.sense_360()
        
        assert len(readings) == 36
        assert all(0 <= angle < 360 for angle in readings.keys())
        assert all(0 <= value <= 1 for value in readings.values())
        
    def test_sense_with_environment_data(self):
        """Test sensing with provided environment data."""
        array = SensorArray(num_sensors=4)
        
        env_data = {
            0.0: 1.0,
            90.0: 0.5,
            180.0: 0.3,
            270.0: 0.7
        }
        
        readings = array.sense_360(env_data)
        assert readings[0.0] == 1.0
        assert readings[90.0] == 0.5
        
    def test_get_sensor_status(self):
        """Test getting sensor status."""
        array = SensorArray(num_sensors=4)
        status = array.get_sensor_status()
        
        assert len(status) == 4
        assert all('id' in s for s in status)
        assert all('angle' in s for s in status)
        assert all('active' in s for s in status)
        
    def test_calibrate_sensor(self):
        """Test sensor calibration."""
        array = SensorArray(num_sensors=4)
        array.calibrate_sensor("sensor_00", 2.0)
        
        assert array.sensors[0].sensitivity == 2.0
        
    def test_disable_enable_sensor(self):
        """Test disabling and enabling sensors."""
        array = SensorArray(num_sensors=4)
        
        array.disable_sensor("sensor_00")
        assert not array.sensors[0].active
        
        array.enable_sensor("sensor_00")
        assert array.sensors[0].active


class TestMetricsInterface:
    """Test suite for MetricsInterface."""
    
    def test_register_metric(self):
        """Test metric registration."""
        metrics = MetricsInterface()
        metrics.register_metric("temperature", unit="°C", max_history=50)
        
        assert "temperature" in metrics.metrics
        assert metrics.metrics["temperature"].unit == "°C"
        
    def test_record_metric(self):
        """Test recording metric values."""
        metrics = MetricsInterface()
        metrics.record_metric("temperature", 21.5)
        
        metric = metrics.get_metric("temperature")
        assert metric is not None
        assert metric.get_current() == 21.5
        
    def test_get_all_metrics(self):
        """Test getting all metrics summary."""
        metrics = MetricsInterface()
        metrics.record_metric("temp", 20.0)
        metrics.record_metric("humidity", 50.0)
        
        summary = metrics.get_all_metrics()
        assert "temp" in summary
        assert "humidity" in summary
        assert summary["temp"]["current"] == 20.0


class TestFeedbackLayer:
    """Test suite for FeedbackLayer."""
    
    def test_send_feedback(self):
        """Test sending feedback."""
        feedback = FeedbackLayer()
        
        msg = feedback.send_feedback(
            "Test message",
            FeedbackType.INFO,
            source="test"
        )
        
        assert msg.message == "Test message"
        assert msg.feedback_type == FeedbackType.INFO
        assert len(feedback.messages) == 1
        
    def test_get_recent_messages(self):
        """Test getting recent messages."""
        feedback = FeedbackLayer()
        
        for i in range(5):
            feedback.send_feedback(f"Message {i}", FeedbackType.INFO)
            
        recent = feedback.get_recent_messages(count=3)
        assert len(recent) == 3
        
    def test_message_filtering(self):
        """Test filtering messages by type."""
        feedback = FeedbackLayer()
        
        feedback.send_feedback("Info", FeedbackType.INFO)
        feedback.send_feedback("Warning", FeedbackType.WARNING)
        feedback.send_feedback("Error", FeedbackType.ERROR)
        
        warnings = feedback.get_recent_messages(
            count=10,
            feedback_type=FeedbackType.WARNING
        )
        assert len(warnings) == 1
        assert warnings[0].message == "Warning"
        
    def test_unacknowledged_messages(self):
        """Test getting unacknowledged messages."""
        feedback = FeedbackLayer()
        
        msg1 = feedback.send_feedback("Message 1", FeedbackType.INFO)
        msg2 = feedback.send_feedback("Message 2", FeedbackType.INFO)
        
        msg1.acknowledge()
        
        unack = feedback.get_unacknowledged()
        assert len(unack) == 1
        assert unack[0].message == "Message 2"


class TestWANCoordinator:
    """Test suite for WANCoordinator."""
    
    def test_coordinator_initialization(self):
        """Test WAN coordinator initialization."""
        wan = WANCoordinator("Test_WAN")
        assert wan.network_name == "Test_WAN"
        assert len(wan.nodes) == 0
        
    def test_register_node(self):
        """Test registering a node."""
        wan = WANCoordinator()
        node = wan.register_node("node_1", location="sector_a")
        
        assert node.node_id == "node_1"
        assert node.location == "sector_a"
        assert "node_1" in wan.nodes
        
    def test_connect_nodes(self):
        """Test connecting two nodes."""
        wan = WANCoordinator()
        
        wan.register_node("node_1")
        wan.register_node("node_2")
        wan.connect_nodes("node_1", "node_2")
        
        connections = wan.get_node_connections("node_1")
        assert "node_2" in connections
        
        # Should be bidirectional
        connections = wan.get_node_connections("node_2")
        assert "node_1" in connections
        
    def test_broadcast_data(self):
        """Test broadcasting data."""
        wan = WANCoordinator()
        
        wan.register_node("node_1")
        wan.register_node("node_2")
        wan.register_node("node_3")
        
        wan.connect_nodes("node_1", "node_2")
        wan.connect_nodes("node_1", "node_3")
        
        wan.broadcast_data("node_1", {"message": "test"})
        
        # Connected nodes should receive data
        assert len(wan.nodes["node_2"].data_buffer) == 1
        assert len(wan.nodes["node_3"].data_buffer) == 1
        
    def test_global_data_sharing(self):
        """Test sharing global data."""
        wan = WANCoordinator()
        
        wan.share_global_data("config", {"setting": "value"})
        data = wan.get_global_data("config")
        
        assert data == {"setting": "value"}
        
    def test_network_status(self):
        """Test getting network status."""
        wan = WANCoordinator()
        
        wan.register_node("node_1")
        wan.register_node("node_2")
        wan.connect_nodes("node_1", "node_2")
        
        status = wan.get_network_status()
        
        assert status['total_nodes'] == 2
        assert status['online_nodes'] == 2
        assert status['total_connections'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
