"""
OBI-WAN Network Module
======================

The mesh network that connects all sensor nodes and coordinates
their collective sensing capabilities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
import asyncio
from enum import Enum

from .sensor_node import SensorNode, SensorReading, SensorType


class NetworkTopology(Enum):
    """Network topology types."""
    MESH = "mesh"
    STAR = "star"
    RING = "ring"


@dataclass
class NetworkConfig:
    """Configuration for the OBI-WAN network."""
    topology: NetworkTopology = NetworkTopology.MESH
    num_nodes: int = 8  # Octagonal arrangement
    auto_discover: bool = True
    heartbeat_interval: float = 1.0  # seconds


class ObiWanNetwork:
    """
    The OBI-WAN mesh network coordinating collective intelligence.
    
    Connects multiple sensor nodes in an octagonal arrangement for
    complete 360° coverage with redundancy.
    """
    
    def __init__(self, config: Optional[NetworkConfig] = None):
        """
        Initialize the OBI-WAN network.
        
        Args:
            config: Network configuration
        """
        self.config = config or NetworkConfig()
        self.nodes: Dict[str, SensorNode] = {}
        self.connections: Dict[str, Set[str]] = {}
        self.active = False
        
    def register_node(self, node: SensorNode) -> None:
        """
        Register a sensor node in the network.
        
        Args:
            node: SensorNode to register
        """
        self.nodes[node.node_id] = node
        self.connections[node.node_id] = set()
        
        # Auto-connect in mesh topology
        if self.config.topology == NetworkTopology.MESH:
            self._mesh_connect(node.node_id)
    
    def _mesh_connect(self, node_id: str) -> None:
        """
        Connect a node to all other nodes in mesh topology.
        
        Args:
            node_id: ID of node to connect
        """
        for other_id in self.nodes.keys():
            if other_id != node_id:
                self.connections[node_id].add(other_id)
                self.connections[other_id].add(node_id)
    
    def unregister_node(self, node_id: str) -> None:
        """
        Unregister a node from the network.
        
        Args:
            node_id: ID of node to unregister
        """
        if node_id in self.nodes:
            # Remove connections
            for other_id in self.connections[node_id]:
                self.connections[other_id].discard(node_id)
            
            del self.nodes[node_id]
            del self.connections[node_id]
    
    def get_node(self, node_id: str) -> Optional[SensorNode]:
        """
        Get a sensor node by ID.
        
        Args:
            node_id: Node identifier
            
        Returns:
            SensorNode if found, None otherwise
        """
        return self.nodes.get(node_id)
    
    def get_nodes_by_type(self, sensor_type: SensorType) -> List[SensorNode]:
        """
        Get all nodes of a specific sensor type.
        
        Args:
            sensor_type: Type of sensor to filter by
            
        Returns:
            List of matching SensorNode objects
        """
        return [
            node for node in self.nodes.values()
            if node.config.sensor_type == sensor_type
        ]
    
    def collect_readings(
        self,
        sensor_type: Optional[SensorType] = None,
        angle_range: Optional[tuple] = None
    ) -> List[SensorReading]:
        """
        Collect readings from all nodes, optionally filtered.
        
        Args:
            sensor_type: Optional sensor type filter
            angle_range: Optional (min, max) angle range in degrees
            
        Returns:
            List of SensorReading objects
        """
        readings = []
        
        for node in self.nodes.values():
            # Filter by sensor type
            if sensor_type and node.config.sensor_type != sensor_type:
                continue
            
            # Get recent readings
            node_readings = node.get_recent_readings(count=10)
            
            # Filter by angle range
            if angle_range:
                min_angle, max_angle = angle_range
                node_readings = [
                    r for r in node_readings
                    if min_angle <= r.angle <= max_angle
                ]
            
            readings.extend(node_readings)
        
        return readings
    
    async def broadcast_message(self, message: Dict) -> None:
        """
        Broadcast a message to all nodes in the network.
        
        Args:
            message: Message dictionary to broadcast
        """
        # In a real implementation, this would send messages to nodes
        # For now, we simulate by logging
        await asyncio.sleep(0.01)  # Simulate network delay
    
    async def heartbeat_loop(self) -> None:
        """
        Maintain network health with periodic heartbeats.
        
        Runs continuously while network is active.
        """
        while self.active:
            await asyncio.sleep(self.config.heartbeat_interval)
            
            # Check node health
            for node_id, node in list(self.nodes.items()):
                if not node.active:
                    # Node is inactive, could trigger alert
                    pass
    
    def start(self) -> None:
        """Activate the network."""
        self.active = True
    
    def stop(self) -> None:
        """Deactivate the network."""
        self.active = False
    
    def get_network_stats(self) -> Dict:
        """Get network statistics."""
        active_nodes = sum(1 for node in self.nodes.values() if node.active)
        total_readings = sum(node.total_readings for node in self.nodes.values())
        
        sensor_distribution = {}
        for node in self.nodes.values():
            sensor_type = node.config.sensor_type.value
            sensor_distribution[sensor_type] = sensor_distribution.get(sensor_type, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "topology": self.config.topology.value,
            "total_readings": total_readings,
            "sensor_distribution": sensor_distribution,
            "network_active": self.active
        }
    
    def get_coverage_map(self, resolution: float = 10.0) -> Dict[float, int]:
        """
        Get a coverage map showing sensor density by angle.
        
        Args:
            resolution: Angular resolution in degrees
            
        Returns:
            Dictionary mapping angles to sensor count
        """
        coverage = {}
        num_bins = int(360.0 / resolution)
        
        for i in range(num_bins):
            angle = i * resolution
            coverage[angle] = 0
        
        # Count sensors covering each angle
        for node in self.nodes.values():
            if not node.active:
                continue
            
            # Each sensor covers its full range
            for angle in coverage.keys():
                # Simplified: assume full 360° coverage for each node
                if node.config.range >= 360:
                    coverage[angle] += 1
        
        return coverage
