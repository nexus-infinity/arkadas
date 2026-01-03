"""
WAN Network Module - Wide Area Network coordination.

Coordinates distributed sensing and observation across the network,
enabling collective awareness and intelligence.
"""

from typing import Dict, List, Optional, Set, Any
from datetime import datetime


class NetworkNode:
    """Individual node in the WAN."""
    
    def __init__(self, node_id: str, location: str = ""):
        """
        Initialize network node.
        
        Args:
            node_id: Unique node identifier
            location: Physical or logical location
        """
        self.node_id = node_id
        self.location = location
        self.active = True
        self.last_heartbeat = datetime.now()
        self.data_buffer = []
        
    def heartbeat(self):
        """Update node heartbeat."""
        self.last_heartbeat = datetime.now()
        
    def is_online(self, timeout_seconds: int = 30) -> bool:
        """
        Check if node is online.
        
        Args:
            timeout_seconds: Heartbeat timeout threshold
            
        Returns:
            True if node is online
        """
        if not self.active:
            return False
            
        time_since_heartbeat = (datetime.now() - self.last_heartbeat).total_seconds()
        return time_since_heartbeat < timeout_seconds


class WANCoordinator:
    """Coordinates the Wide Area Network for distributed observation."""
    
    def __init__(self, network_name: str = "OBI-WAN"):
        """
        Initialize WAN coordinator.
        
        Args:
            network_name: Name of the network
        """
        self.network_name = network_name
        self.nodes: Dict[str, NetworkNode] = {}
        self.connections: Dict[str, Set[str]] = {}
        self.shared_data: Dict[str, Any] = {}
        
    def register_node(self, node_id: str, location: str = "") -> NetworkNode:
        """
        Register a new node in the network.
        
        Args:
            node_id: Unique node identifier
            location: Node location
            
        Returns:
            Created NetworkNode
        """
        node = NetworkNode(node_id, location)
        self.nodes[node_id] = node
        self.connections[node_id] = set()
        return node
    
    def connect_nodes(self, node_id1: str, node_id2: str):
        """
        Create bidirectional connection between nodes.
        
        Args:
            node_id1: First node ID
            node_id2: Second node ID
        """
        if node_id1 in self.nodes and node_id2 in self.nodes:
            self.connections[node_id1].add(node_id2)
            self.connections[node_id2].add(node_id1)
            
    def disconnect_nodes(self, node_id1: str, node_id2: str):
        """
        Remove connection between nodes.
        
        Args:
            node_id1: First node ID
            node_id2: Second node ID
        """
        if node_id1 in self.connections:
            self.connections[node_id1].discard(node_id2)
        if node_id2 in self.connections:
            self.connections[node_id2].discard(node_id1)
            
    def get_node_connections(self, node_id: str) -> List[str]:
        """
        Get all connections for a node.
        
        Args:
            node_id: Node identifier
            
        Returns:
            List of connected node IDs
        """
        return list(self.connections.get(node_id, set()))
    
    def broadcast_data(self, source_node_id: str, data: Any):
        """
        Broadcast data from a node to all connected nodes.
        
        Args:
            source_node_id: Source node ID
            data: Data to broadcast
        """
        if source_node_id not in self.nodes:
            return
            
        connected = self.connections.get(source_node_id, set())
        for target_id in connected:
            if target_id in self.nodes:
                self.nodes[target_id].data_buffer.append({
                    'source': source_node_id,
                    'data': data,
                    'timestamp': datetime.now()
                })
                
    def share_global_data(self, key: str, value: Any):
        """
        Share data globally across all nodes.
        
        Args:
            key: Data key
            value: Data value
        """
        self.shared_data[key] = {
            'value': value,
            'timestamp': datetime.now()
        }
        
    def get_global_data(self, key: str) -> Optional[Any]:
        """
        Retrieve globally shared data.
        
        Args:
            key: Data key
            
        Returns:
            Data value or None
        """
        data = self.shared_data.get(key)
        return data['value'] if data else None
    
    def get_network_status(self) -> Dict[str, Any]:
        """
        Get overall network status.
        
        Returns:
            Dictionary containing network information
        """
        online_nodes = sum(1 for node in self.nodes.values() if node.is_online())
        total_connections = sum(len(conns) for conns in self.connections.values()) // 2
        
        return {
            'network_name': self.network_name,
            'total_nodes': len(self.nodes),
            'online_nodes': online_nodes,
            'total_connections': total_connections,
            'shared_data_keys': list(self.shared_data.keys())
        }
    
    def deactivate_node(self, node_id: str):
        """
        Deactivate a node.
        
        Args:
            node_id: Node to deactivate
        """
        if node_id in self.nodes:
            self.nodes[node_id].active = False
            
    def activate_node(self, node_id: str):
        """
        Activate a node.
        
        Args:
            node_id: Node to activate
        """
        if node_id in self.nodes:
            self.nodes[node_id].active = True
            self.nodes[node_id].heartbeat()
