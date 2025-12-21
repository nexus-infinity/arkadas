"""
DAL Friend Module - DAL agent friend protocol.

Implements the friend protocol for DAL (Distributed Agent Learning) agents,
enabling polymorphic friend relationships and collaboration.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class FriendStatus(Enum):
    """Status of friend connection."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    PENDING = "pending"
    SUSPENDED = "suspended"


class DALFriend:
    """DAL agent implementing friend protocol."""
    
    def __init__(self, friend_id: str, capabilities: Optional[List[str]] = None):
        """
        Initialize DAL friend.
        
        Args:
            friend_id: Unique friend identifier
            capabilities: List of friend capabilities
        """
        self.friend_id = friend_id
        self.capabilities = capabilities or []
        self.status = FriendStatus.CONNECTED
        self.connections: Dict[str, 'DALFriend'] = {}
        self.shared_knowledge: Dict[str, Any] = {}
        self.interaction_history = []
        self.trust_score = 0.5  # Start neutral
        
    def add_capability(self, capability: str):
        """
        Add a capability to the friend.
        
        Args:
            capability: Capability to add
        """
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            
    def has_capability(self, capability: str) -> bool:
        """
        Check if friend has a capability.
        
        Args:
            capability: Capability to check
            
        Returns:
            True if friend has capability
        """
        return capability in self.capabilities
    
    def connect_friend(self, friend: 'DALFriend'):
        """
        Establish connection with another friend.
        
        Args:
            friend: Friend to connect with
        """
        self.connections[friend.friend_id] = friend
        self._record_interaction(f"Connected with {friend.friend_id}")
        
    def disconnect_friend(self, friend_id: str):
        """
        Disconnect from a friend.
        
        Args:
            friend_id: ID of friend to disconnect
        """
        if friend_id in self.connections:
            del self.connections[friend_id]
            self._record_interaction(f"Disconnected from {friend_id}")
            
    def share_knowledge(self, key: str, value: Any):
        """
        Share knowledge with connected friends.
        
        Args:
            key: Knowledge key
            value: Knowledge value
        """
        self.shared_knowledge[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'shared_by': self.friend_id
        }
        
        # Propagate to connected friends
        for friend in self.connections.values():
            if friend.status == FriendStatus.CONNECTED:
                friend.receive_knowledge(key, value, self.friend_id)
                
    def receive_knowledge(self, key: str, value: Any, source_id: str):
        """
        Receive knowledge from another friend.
        
        Args:
            key: Knowledge key
            value: Knowledge value
            source_id: ID of sharing friend
        """
        self.shared_knowledge[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'shared_by': source_id
        }
        self._record_interaction(f"Received knowledge '{key}' from {source_id}")
        
    def get_knowledge(self, key: str) -> Optional[Any]:
        """
        Retrieve shared knowledge.
        
        Args:
            key: Knowledge key
            
        Returns:
            Knowledge value or None
        """
        knowledge = self.shared_knowledge.get(key)
        return knowledge['value'] if knowledge else None
    
    def _record_interaction(self, description: str):
        """
        Record an interaction in history.
        
        Args:
            description: Description of interaction
        """
        self.interaction_history.append({
            'timestamp': datetime.now(),
            'description': description
        })
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get friend status summary.
        
        Returns:
            Dictionary containing friend information
        """
        return {
            'friend_id': self.friend_id,
            'status': self.status.value,
            'capabilities': self.capabilities,
            'connections': list(self.connections.keys()),
            'knowledge_keys': list(self.shared_knowledge.keys()),
            'trust_score': self.trust_score,
            'interaction_count': len(self.interaction_history)
        }
    
    def update_trust(self, delta: float):
        """
        Update trust score.
        
        Args:
            delta: Change in trust (-1.0 to 1.0)
        """
        self.trust_score = max(0.0, min(1.0, self.trust_score + delta))
        
    def suspend(self):
        """Suspend friend status."""
        self.status = FriendStatus.SUSPENDED
        
    def resume(self):
        """Resume friend status."""
        self.status = FriendStatus.CONNECTED
