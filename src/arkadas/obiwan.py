"""
OBI-WAN Network Module
Observer + Being + Interface | Wide Area Network
Distributed friend network with polymorphic intelligence
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class NodeStatus(Enum):
    """Status of a friend node"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    OBSERVING = "observing"
    CONTRIBUTING = "contributing"


@dataclass
class Observation:
    """Represents an observation from a friend node"""
    node_id: str
    metric_name: str
    value: Any
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class FriendNode:
    """
    Friend Node - Individual member of the OBI-WAN network
    Polymorphic, adaptive intelligence with trust-based relationships
    """
    
    def __init__(self, node_id: Optional[str] = None, name: Optional[str] = None):
        self.node_id = node_id or str(uuid.uuid4())
        self.name = name or f"Friend-{self.node_id[:8]}"
        self.status = NodeStatus.INACTIVE
        self.trust_level = 0.0  # 0.0 to 1.0
        self.observations: List[Observation] = []
        self.connections: Set[str] = set()  # Connected friend node IDs
        self.capabilities: Set[str] = set()
        self.created_at = time.time()
        
    def activate(self) -> None:
        """Activate this friend node"""
        self.status = NodeStatus.ACTIVE
        
    def deactivate(self) -> None:
        """Deactivate this friend node"""
        self.status = NodeStatus.INACTIVE
        
    def start_observing(self) -> None:
        """Start observing the field"""
        if self.status != NodeStatus.INACTIVE:
            self.status = NodeStatus.OBSERVING
            
    def contribute(self, metric_name: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> Observation:
        """
        Contribute an observation to the network
        
        Args:
            metric_name: Name of the metric being observed
            value: Observed value
            metadata: Optional additional metadata
            
        Returns:
            The created Observation
        """
        observation = Observation(
            node_id=self.node_id,
            metric_name=metric_name,
            value=value,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self.observations.append(observation)
        self.status = NodeStatus.CONTRIBUTING
        
        return observation
    
    def connect_to(self, other_node_id: str) -> None:
        """
        Establish peer connection to another friend node
        
        Args:
            other_node_id: ID of the node to connect to
        """
        self.connections.add(other_node_id)
        
    def add_capability(self, capability: str) -> None:
        """
        Add a capability to this node
        
        Args:
            capability: Capability identifier
        """
        self.capabilities.add(capability)
        
    def get_info(self) -> Dict[str, Any]:
        """
        Get node information
        
        Returns:
            Node info dictionary
        """
        return {
            "node_id": self.node_id,
            "name": self.name,
            "status": self.status.value,
            "trust_level": self.trust_level,
            "observation_count": len(self.observations),
            "connection_count": len(self.connections),
            "capabilities": list(self.capabilities),
            "uptime": time.time() - self.created_at,
        }


class ObiWanNetwork:
    """
    OBI-WAN Network
    Wide Area Network of friend nodes
    Distributed observation, sensing, and collective intelligence
    """
    
    def __init__(self):
        self.nodes: Dict[str, FriendNode] = {}
        self.observations: List[Observation] = []
        self.is_configured = False
        self.network_trust = 0.0
        self.collective_intelligence = 0.0
        
    def configure(self) -> None:
        """Configure the OBI-WAN network"""
        self.is_configured = True
        
    def deploy_node(self, node: Optional[FriendNode] = None, name: Optional[str] = None) -> FriendNode:
        """
        Deploy a new friend node to the network
        
        Args:
            node: Existing FriendNode to deploy, or None to create new
            name: Name for the node if creating new
            
        Returns:
            The deployed FriendNode
        """
        if node is None:
            node = FriendNode(name=name)
        
        self.nodes[node.node_id] = node
        node.activate()
        
        # Update network metrics
        self._update_network_metrics()
        
        return node
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node from the network
        
        Args:
            node_id: ID of node to remove
            
        Returns:
            True if removed successfully
        """
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.deactivate()
            del self.nodes[node_id]
            self._update_network_metrics()
            return True
        return False
    
    def connect_nodes(self, node_id_1: str, node_id_2: str) -> bool:
        """
        Create peer connection between two nodes
        
        Args:
            node_id_1: First node ID
            node_id_2: Second node ID
            
        Returns:
            True if connection established
        """
        if node_id_1 in self.nodes and node_id_2 in self.nodes:
            self.nodes[node_id_1].connect_to(node_id_2)
            self.nodes[node_id_2].connect_to(node_id_1)
            return True
        return False
    
    def receive_observation(self, observation: Observation) -> None:
        """
        Receive an observation from a friend node
        
        Args:
            observation: The observation to receive
        """
        self.observations.append(observation)
        
    def aggregate_metric(self, metric_name: str) -> Dict[str, Any]:
        """
        Aggregate a specific metric across all observations
        
        Args:
            metric_name: Name of metric to aggregate
            
        Returns:
            Aggregated metric data
        """
        relevant_obs = [obs for obs in self.observations if obs.metric_name == metric_name]
        
        if not relevant_obs:
            return {
                "metric_name": metric_name,
                "count": 0,
                "values": [],
                "contributors": [],
            }
        
        values = [obs.value for obs in relevant_obs]
        contributors = list(set(obs.node_id for obs in relevant_obs))
        
        # Calculate statistics if numeric
        try:
            numeric_values = [float(v) for v in values]
            avg = sum(numeric_values) / len(numeric_values)
            min_val = min(numeric_values)
            max_val = max(numeric_values)
            
            return {
                "metric_name": metric_name,
                "count": len(relevant_obs),
                "values": values,
                "contributors": contributors,
                "average": avg,
                "min": min_val,
                "max": max_val,
            }
        except (ValueError, TypeError):
            # Non-numeric values
            return {
                "metric_name": metric_name,
                "count": len(relevant_obs),
                "values": values,
                "contributors": contributors,
            }
    
    def measure_field_coherence(self) -> float:
        """
        Measure overall field coherence
        
        Returns:
            Coherence value (0.0 - 1.0)
        """
        if not self.nodes:
            return 0.0
        
        # Coherence based on active nodes and their connections
        active_count = sum(1 for node in self.nodes.values() if node.status != NodeStatus.INACTIVE)
        total_connections = sum(len(node.connections) for node in self.nodes.values())
        
        # Maximum possible connections in a fully connected graph
        max_possible = len(self.nodes) * (len(self.nodes) - 1)
        
        if max_possible == 0:
            return 0.0
        
        coherence = (total_connections / max_possible) * (active_count / len(self.nodes))
        return min(1.0, coherence)
    
    def detect_drift(self) -> float:
        """
        Detect network drift/desynchronization
        
        Returns:
            Drift value (0.0 = no drift)
        """
        # Simplified drift detection based on inactive nodes
        if not self.nodes:
            return 0.0
        
        inactive_count = sum(1 for node in self.nodes.values() if node.status == NodeStatus.INACTIVE)
        drift = inactive_count / len(self.nodes)
        
        return drift
    
    def _update_network_metrics(self) -> None:
        """Update network-level metrics"""
        if not self.nodes:
            self.network_trust = 0.0
            self.collective_intelligence = 0.0
            return
        
        # Network trust is average of all node trust levels
        self.network_trust = sum(node.trust_level for node in self.nodes.values()) / len(self.nodes)
        
        # Collective intelligence based on active nodes and observations
        active_nodes = sum(1 for node in self.nodes.values() if node.status != NodeStatus.INACTIVE)
        total_observations = sum(len(node.observations) for node in self.nodes.values())
        
        self.collective_intelligence = min(1.0, (active_nodes * total_observations) / max(1, len(self.nodes) * 100))
    
    def get_network_status(self) -> Dict[str, Any]:
        """
        Get overall network status
        
        Returns:
            Status dictionary
        """
        return {
            "configured": self.is_configured,
            "node_count": len(self.nodes),
            "active_nodes": sum(1 for node in self.nodes.values() if node.status != NodeStatus.INACTIVE),
            "total_observations": len(self.observations),
            "network_trust": self.network_trust,
            "collective_intelligence": self.collective_intelligence,
            "field_coherence": self.measure_field_coherence(),
            "drift": self.detect_drift(),
        }
    
    def get_nodes(self) -> List[FriendNode]:
        """
        Get all nodes in the network
        
        Returns:
            List of FriendNode objects
        """
        return list(self.nodes.values())
