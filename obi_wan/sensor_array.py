"""
Sensor Array Module - 360° sensing.

Provides omnidirectional sensing capabilities for complete environmental awareness.
"""

from typing import Dict, List, Optional, Tuple
import math


class Sensor:
    """Individual sensor in the array."""
    
    def __init__(self, sensor_id: str, angle: float, sensitivity: float = 1.0):
        """
        Initialize a sensor.
        
        Args:
            sensor_id: Unique identifier for the sensor
            angle: Angular position in degrees (0-360)
            sensitivity: Sensor sensitivity multiplier
        """
        self.sensor_id = sensor_id
        self.angle = angle % 360
        self.sensitivity = sensitivity
        self.last_reading = 0.0
        self.active = True
        
    def read(self, value: float) -> float:
        """
        Take a reading.
        
        Args:
            value: Raw sensor value
            
        Returns:
            Adjusted reading based on sensitivity
        """
        if not self.active:
            return 0.0
        self.last_reading = value * self.sensitivity
        return self.last_reading


class SensorArray:
    """360° sensor array for omnidirectional sensing."""
    
    def __init__(self, num_sensors: int = 36):
        """
        Initialize sensor array.
        
        Args:
            num_sensors: Number of sensors in the array (evenly distributed)
        """
        self.num_sensors = num_sensors
        self.sensors = []
        self._initialize_sensors()
        
    def _initialize_sensors(self):
        """Initialize sensors in 360° arrangement."""
        angle_step = 360.0 / self.num_sensors
        for i in range(self.num_sensors):
            angle = i * angle_step
            sensor = Sensor(f"sensor_{i:02d}", angle)
            self.sensors.append(sensor)
            
    def sense_360(self, environment_data: Optional[Dict[float, float]] = None) -> Dict[float, float]:
        """
        Perform 360° sensing sweep.
        
        Args:
            environment_data: Optional environmental data mapped by angle
            
        Returns:
            Dictionary mapping sensor angles to readings
        """
        readings = {}
        
        for sensor in self.sensors:
            if environment_data and sensor.angle in environment_data:
                value = environment_data[sensor.angle]
            else:
                # Default sensing behavior
                value = self._default_sense(sensor.angle)
                
            readings[sensor.angle] = sensor.read(value)
            
        return readings
    
    def _default_sense(self, angle: float) -> float:
        """
        Default sensing function when no environment data provided.
        
        Args:
            angle: Sensor angle
            
        Returns:
            Default sensed value
        """
        # Simple sine wave pattern for testing
        return (math.sin(math.radians(angle)) + 1) / 2
    
    def get_sensor_status(self) -> List[Dict[str, any]]:
        """
        Get status of all sensors.
        
        Returns:
            List of sensor status dictionaries
        """
        return [
            {
                'id': sensor.sensor_id,
                'angle': sensor.angle,
                'active': sensor.active,
                'last_reading': sensor.last_reading
            }
            for sensor in self.sensors
        ]
    
    def calibrate_sensor(self, sensor_id: str, sensitivity: float):
        """
        Calibrate a specific sensor.
        
        Args:
            sensor_id: ID of sensor to calibrate
            sensitivity: New sensitivity value
        """
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.sensitivity = sensitivity
                break
                
    def disable_sensor(self, sensor_id: str):
        """
        Disable a specific sensor.
        
        Args:
            sensor_id: ID of sensor to disable
        """
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.active = False
                break
                
    def enable_sensor(self, sensor_id: str):
        """
        Enable a specific sensor.
        
        Args:
            sensor_id: ID of sensor to enable
        """
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.active = True
                break
