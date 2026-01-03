"""
Train Station Module - Downward to Train Station.

Provides interface for downward integration to the Train Station layer,
handling data flow and coordination with lower system components.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TrainType(Enum):
    """Types of data trains."""
    EXPRESS = "express"      # High priority, direct
    LOCAL = "local"          # Regular priority
    FREIGHT = "freight"      # Bulk data transfer
    MAINTENANCE = "maintenance"  # System maintenance


class Train:
    """Represents a data train for transport."""
    
    def __init__(self, 
                 train_id: str,
                 train_type: TrainType,
                 payload: Any,
                 destination: str):
        """
        Initialize a train.
        
        Args:
            train_id: Unique train identifier
            train_type: Type of train
            payload: Data payload
            destination: Target destination
        """
        self.train_id = train_id
        self.train_type = train_type
        self.payload = payload
        self.destination = destination
        self.departure_time = datetime.now()
        self.arrival_time = None
        self.status = "pending"
        
    def depart(self):
        """Mark train as departed."""
        self.status = "in_transit"
        self.departure_time = datetime.now()
        
    def arrive(self):
        """Mark train as arrived."""
        self.status = "arrived"
        self.arrival_time = datetime.now()
        
    def get_travel_time(self) -> Optional[float]:
        """Get travel time in seconds."""
        if self.arrival_time and self.departure_time:
            return (self.arrival_time - self.departure_time).total_seconds()
        return None


class TrainStationInterface:
    """Interface for downward communication to Train Station."""
    
    def __init__(self, station_name: str = "Kings_Chamber_Station"):
        """
        Initialize train station interface.
        
        Args:
            station_name: Name of this station
        """
        self.station_name = station_name
        self.active_trains: Dict[str, Train] = {}
        self.departed_trains: List[Train] = []
        self.arrival_queue: List[Train] = []
        self.track_count = 4
        
    def dispatch_train(self, 
                      payload: Any,
                      destination: str,
                      train_type: TrainType = TrainType.LOCAL) -> Train:
        """
        Dispatch a train with payload to destination.
        
        Args:
            payload: Data to send
            destination: Target destination
            train_type: Type of train
            
        Returns:
            Created Train object
        """
        train_id = f"train_{len(self.departed_trains) + 1:04d}"
        train = Train(train_id, train_type, payload, destination)
        
        self.active_trains[train_id] = train
        train.depart()
        
        return train
    
    def receive_train(self, train: Train):
        """
        Receive an incoming train.
        
        Args:
            train: Arriving train
        """
        train.arrive()
        self.arrival_queue.append(train)
        
        if train.train_id in self.active_trains:
            self.departed_trains.append(self.active_trains[train.train_id])
            del self.active_trains[train.train_id]
            
    def get_next_arrival(self) -> Optional[Train]:
        """
        Get next train from arrival queue.
        
        Returns:
            Next Train or None
        """
        if self.arrival_queue:
            return self.arrival_queue.pop(0)
        return None
    
    def send_to_lower_layer(self, data: Dict[str, Any], priority: str = "normal") -> str:
        """
        Send data to lower system layer.
        
        Args:
            data: Data to send
            priority: Priority level
            
        Returns:
            Train ID for tracking
        """
        train_type = TrainType.EXPRESS if priority == "high" else TrainType.LOCAL
        train = self.dispatch_train(data, "lower_layer", train_type)
        return train.train_id
    
    def receive_from_lower_layer(self) -> Optional[Dict[str, Any]]:
        """
        Receive data from lower layer.
        
        Returns:
            Data payload or None
        """
        train = self.get_next_arrival()
        if train:
            return {
                'payload': train.payload,
                'train_id': train.train_id,
                'type': train.train_type.value,
                'travel_time': train.get_travel_time()
            }
        return None
    
    def get_station_status(self) -> Dict[str, Any]:
        """
        Get current station status.
        
        Returns:
            Station status information
        """
        return {
            'station_name': self.station_name,
            'active_trains': len(self.active_trains),
            'departed_trains': len(self.departed_trains),
            'arrival_queue': len(self.arrival_queue),
            'track_count': self.track_count,
            'average_travel_time': self._calculate_average_travel_time()
        }
    
    def _calculate_average_travel_time(self) -> float:
        """Calculate average train travel time."""
        times = [t.get_travel_time() for t in self.departed_trains if t.get_travel_time()]
        return sum(times) / len(times) if times else 0.0
    
    def clear_departed_trains(self):
        """Clear history of departed trains."""
        self.departed_trains.clear()
        
    def emergency_stop_all(self):
        """Emergency stop all active trains."""
        for train in self.active_trains.values():
            train.status = "stopped"
