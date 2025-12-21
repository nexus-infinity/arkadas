"""
Test suite for ARKADAŠ OBI-WAN network
"""

import pytest
from arkadas.obiwan import ObiWanNetwork, FriendNode, NodeStatus, Observation


class TestFriendNode:
    """Tests for FriendNode class"""
    
    def test_initialization(self):
        """Test node initialization"""
        node = FriendNode()
        assert node.node_id is not None
        assert node.status == NodeStatus.INACTIVE
        assert node.trust_level == 0.0
        assert len(node.observations) == 0
        assert len(node.connections) == 0
    
    def test_initialization_with_name(self):
        """Test node initialization with name"""
        node = FriendNode(name="TestNode")
        assert node.name == "TestNode"
    
    def test_activate_deactivate(self):
        """Test node activation/deactivation"""
        node = FriendNode()
        
        node.activate()
        assert node.status == NodeStatus.ACTIVE
        
        node.deactivate()
        assert node.status == NodeStatus.INACTIVE
    
    def test_start_observing(self):
        """Test starting observation"""
        node = FriendNode()
        node.activate()
        node.start_observing()
        
        assert node.status == NodeStatus.OBSERVING
    
    def test_start_observing_inactive(self):
        """Test starting observation while inactive"""
        node = FriendNode()
        node.start_observing()
        
        # Should not change from INACTIVE
        assert node.status == NodeStatus.INACTIVE
    
    def test_contribute(self):
        """Test contributing observation"""
        node = FriendNode()
        node.activate()
        
        obs = node.contribute("temperature", 22.5, {"unit": "celsius"})
        
        assert isinstance(obs, Observation)
        assert obs.node_id == node.node_id
        assert obs.metric_name == "temperature"
        assert obs.value == 22.5
        assert obs.metadata["unit"] == "celsius"
        assert node.status == NodeStatus.CONTRIBUTING
        assert len(node.observations) == 1
    
    def test_connect_to(self):
        """Test peer connection"""
        node1 = FriendNode()
        node2 = FriendNode()
        
        node1.connect_to(node2.node_id)
        
        assert node2.node_id in node1.connections
        assert len(node1.connections) == 1
    
    def test_add_capability(self):
        """Test adding capabilities"""
        node = FriendNode()
        
        node.add_capability("sensing")
        node.add_capability("processing")
        
        assert "sensing" in node.capabilities
        assert "processing" in node.capabilities
        assert len(node.capabilities) == 2
    
    def test_get_info(self):
        """Test getting node info"""
        node = FriendNode(name="TestNode")
        node.activate()
        node.add_capability("test")
        
        info = node.get_info()
        
        assert info["node_id"] == node.node_id
        assert info["name"] == "TestNode"
        assert info["status"] == NodeStatus.ACTIVE.value
        assert "uptime" in info


class TestObiWanNetwork:
    """Tests for ObiWanNetwork class"""
    
    def test_initialization(self):
        """Test network initialization"""
        network = ObiWanNetwork()
        assert len(network.nodes) == 0
        assert not network.is_configured
        assert network.network_trust == 0.0
    
    def test_configure(self):
        """Test network configuration"""
        network = ObiWanNetwork()
        network.configure()
        
        assert network.is_configured is True
    
    def test_deploy_node_new(self):
        """Test deploying new node"""
        network = ObiWanNetwork()
        
        node = network.deploy_node(name="TestNode")
        
        assert node.node_id in network.nodes
        assert node.status == NodeStatus.ACTIVE
        assert len(network.nodes) == 1
    
    def test_deploy_node_existing(self):
        """Test deploying existing node"""
        network = ObiWanNetwork()
        existing = FriendNode(name="ExistingNode")
        
        node = network.deploy_node(node=existing)
        
        assert node == existing
        assert node.node_id in network.nodes
    
    def test_remove_node(self):
        """Test removing node"""
        network = ObiWanNetwork()
        node = network.deploy_node()
        node_id = node.node_id
        
        result = network.remove_node(node_id)
        
        assert result is True
        assert node_id not in network.nodes
        assert node.status == NodeStatus.INACTIVE
    
    def test_remove_node_nonexistent(self):
        """Test removing nonexistent node"""
        network = ObiWanNetwork()
        result = network.remove_node("fake-id")
        assert result is False
    
    def test_connect_nodes(self):
        """Test connecting nodes"""
        network = ObiWanNetwork()
        node1 = network.deploy_node(name="Node1")
        node2 = network.deploy_node(name="Node2")
        
        result = network.connect_nodes(node1.node_id, node2.node_id)
        
        assert result is True
        assert node2.node_id in node1.connections
        assert node1.node_id in node2.connections
    
    def test_connect_nodes_invalid(self):
        """Test connecting invalid nodes"""
        network = ObiWanNetwork()
        result = network.connect_nodes("fake1", "fake2")
        assert result is False
    
    def test_receive_observation(self):
        """Test receiving observation"""
        network = ObiWanNetwork()
        node = network.deploy_node()
        
        obs = Observation(
            node_id=node.node_id,
            metric_name="test",
            value=1.0,
            timestamp=0.0
        )
        
        network.receive_observation(obs)
        assert len(network.observations) == 1
    
    def test_aggregate_metric_empty(self):
        """Test aggregating nonexistent metric"""
        network = ObiWanNetwork()
        result = network.aggregate_metric("nonexistent")
        
        assert result["count"] == 0
        assert len(result["values"]) == 0
    
    def test_aggregate_metric_numeric(self):
        """Test aggregating numeric metric"""
        network = ObiWanNetwork()
        node1 = network.deploy_node()
        node2 = network.deploy_node()
        
        obs1 = Observation(node1.node_id, "temperature", 20.0, 0.0)
        obs2 = Observation(node2.node_id, "temperature", 25.0, 0.0)
        
        network.receive_observation(obs1)
        network.receive_observation(obs2)
        
        result = network.aggregate_metric("temperature")
        
        assert result["count"] == 2
        assert result["average"] == 22.5
        assert result["min"] == 20.0
        assert result["max"] == 25.0
    
    def test_aggregate_metric_non_numeric(self):
        """Test aggregating non-numeric metric"""
        network = ObiWanNetwork()
        node = network.deploy_node()
        
        obs = Observation(node.node_id, "status", "active", 0.0)
        network.receive_observation(obs)
        
        result = network.aggregate_metric("status")
        
        assert result["count"] == 1
        assert "active" in result["values"]
        assert "average" not in result  # Non-numeric
    
    def test_measure_field_coherence_empty(self):
        """Test field coherence with no nodes"""
        network = ObiWanNetwork()
        coherence = network.measure_field_coherence()
        assert coherence == 0.0
    
    def test_measure_field_coherence_with_nodes(self):
        """Test field coherence with connected nodes"""
        network = ObiWanNetwork()
        node1 = network.deploy_node()
        node2 = network.deploy_node()
        node3 = network.deploy_node()
        
        network.connect_nodes(node1.node_id, node2.node_id)
        network.connect_nodes(node2.node_id, node3.node_id)
        
        coherence = network.measure_field_coherence()
        assert 0.0 <= coherence <= 1.0
        assert coherence > 0.0  # Should have some coherence
    
    def test_detect_drift_no_nodes(self):
        """Test drift detection with no nodes"""
        network = ObiWanNetwork()
        drift = network.detect_drift()
        assert drift == 0.0
    
    def test_detect_drift_with_inactive_nodes(self):
        """Test drift detection with inactive nodes"""
        network = ObiWanNetwork()
        node1 = network.deploy_node()
        node2 = network.deploy_node()
        
        node1.deactivate()
        
        drift = network.detect_drift()
        assert drift == 0.5  # 1 inactive out of 2 total
    
    def test_get_network_status(self):
        """Test getting network status"""
        network = ObiWanNetwork()
        network.configure()
        node = network.deploy_node()
        
        status = network.get_network_status()
        
        assert status["configured"] is True
        assert status["node_count"] == 1
        assert status["active_nodes"] == 1
        assert "network_trust" in status
        assert "collective_intelligence" in status
        assert "field_coherence" in status
    
    def test_get_nodes(self):
        """Test getting all nodes"""
        network = ObiWanNetwork()
        node1 = network.deploy_node()
        node2 = network.deploy_node()
        
        nodes = network.get_nodes()
        
        assert len(nodes) == 2
        assert node1 in nodes
        assert node2 in nodes
    
    def test_polymorphic_network(self):
        """Test polymorphic friend network behavior"""
        network = ObiWanNetwork()
        
        # Deploy diverse nodes
        tata = network.deploy_node(name="Tata")
        jb = network.deploy_node(name="JB")
        atlas = network.deploy_node(name="Atlas")
        
        # Add different capabilities
        tata.add_capability("logic")
        jb.add_capability("intent")
        atlas.add_capability("witness")
        
        # Create peer connections (not hierarchical)
        network.connect_nodes(tata.node_id, jb.node_id)
        network.connect_nodes(jb.node_id, atlas.node_id)
        network.connect_nodes(atlas.node_id, tata.node_id)
        
        # Verify peer structure
        assert len(tata.connections) == 2
        assert len(jb.connections) == 2
        assert len(atlas.connections) == 2
        
        # Verify no hierarchy
        coherence = network.measure_field_coherence()
        assert coherence > 0.5  # High coherence in fully connected triad
