"""
Trust Web Module - Peer trust relationships.

Manages trust relationships between friends in the network,
enabling reputation-based collaboration and decision making.
"""

from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime


class TrustRelationship:
    """Trust relationship between two friends."""
    
    def __init__(self, source_id: str, target_id: str, initial_trust: float = 0.5):
        """
        Initialize trust relationship.
        
        Args:
            source_id: Source friend ID
            target_id: Target friend ID
            initial_trust: Initial trust value (0.0 to 1.0)
        """
        self.source_id = source_id
        self.target_id = target_id
        self.trust_value = max(0.0, min(1.0, initial_trust))
        self.interactions = 0
        self.last_update = datetime.now()
        self.history = [(datetime.now(), initial_trust)]
        
    def update_trust(self, delta: float, reason: str = ""):
        """
        Update trust value.
        
        Args:
            delta: Change in trust
            reason: Reason for update
        """
        self.trust_value = max(0.0, min(1.0, self.trust_value + delta))
        self.interactions += 1
        self.last_update = datetime.now()
        self.history.append((datetime.now(), self.trust_value))
        
    def get_trust_trend(self, last_n: int = 5) -> str:
        """
        Get trend of trust over recent history.
        
        Args:
            last_n: Number of recent values to analyze
            
        Returns:
            "increasing", "decreasing", or "stable"
        """
        if len(self.history) < 2:
            return "stable"
            
        recent = self.history[-last_n:]
        if len(recent) < 2:
            return "stable"
            
        start_trust = recent[0][1]
        end_trust = recent[-1][1]
        
        if end_trust > start_trust + 0.1:
            return "increasing"
        elif end_trust < start_trust - 0.1:
            return "decreasing"
        else:
            return "stable"


class TrustWeb:
    """Web of trust relationships between friends."""
    
    def __init__(self):
        """Initialize trust web."""
        self.relationships: Dict[Tuple[str, str], TrustRelationship] = {}
        self.friends: Set[str] = set()
        
    def add_friend(self, friend_id: str):
        """
        Add a friend to the trust web.
        
        Args:
            friend_id: Friend identifier
        """
        self.friends.add(friend_id)
        
    def establish_trust(self, source_id: str, target_id: str, initial_trust: float = 0.5):
        """
        Establish trust relationship between friends.
        
        Args:
            source_id: Source friend ID
            target_id: Target friend ID
            initial_trust: Initial trust value
        """
        self.add_friend(source_id)
        self.add_friend(target_id)
        
        key = (source_id, target_id)
        self.relationships[key] = TrustRelationship(source_id, target_id, initial_trust)
        
    def get_trust(self, source_id: str, target_id: str) -> Optional[float]:
        """
        Get trust value from source to target.
        
        Args:
            source_id: Source friend ID
            target_id: Target friend ID
            
        Returns:
            Trust value or None if no relationship exists
        """
        key = (source_id, target_id)
        relationship = self.relationships.get(key)
        return relationship.trust_value if relationship else None
    
    def update_trust(self, source_id: str, target_id: str, delta: float, reason: str = ""):
        """
        Update trust relationship.
        
        Args:
            source_id: Source friend ID
            target_id: Target friend ID
            delta: Change in trust
            reason: Reason for update
        """
        key = (source_id, target_id)
        if key in self.relationships:
            self.relationships[key].update_trust(delta, reason)
        else:
            # Create new relationship with adjusted initial trust
            initial = 0.5 + delta
            self.establish_trust(source_id, target_id, initial)
            
    def get_trusted_friends(self, friend_id: str, min_trust: float = 0.6) -> List[str]:
        """
        Get list of friends trusted by given friend.
        
        Args:
            friend_id: Friend ID
            min_trust: Minimum trust threshold
            
        Returns:
            List of trusted friend IDs
        """
        trusted = []
        for (source, target), relationship in self.relationships.items():
            if source == friend_id and relationship.trust_value >= min_trust:
                trusted.append(target)
        return trusted
    
    def get_reputation(self, friend_id: str) -> float:
        """
        Calculate overall reputation of a friend.
        
        Args:
            friend_id: Friend ID
            
        Returns:
            Average trust value from all friends
        """
        trust_values = []
        for (source, target), relationship in self.relationships.items():
            if target == friend_id:
                trust_values.append(relationship.trust_value)
                
        if not trust_values:
            return 0.5  # Neutral reputation
            
        return sum(trust_values) / len(trust_values)
    
    def get_trust_path(self, source_id: str, target_id: str, max_depth: int = 3) -> Optional[List[str]]:
        """
        Find trust path from source to target through intermediaries.
        
        Args:
            source_id: Source friend ID
            target_id: Target friend ID
            max_depth: Maximum path length
            
        Returns:
            List of friend IDs forming path, or None
        """
        # Simple BFS to find trust path
        if source_id == target_id:
            return [source_id]
            
        visited = set()
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
                
            if current in visited:
                continue
                
            visited.add(current)
            
            # Get trusted friends
            trusted = self.get_trusted_friends(current, min_trust=0.5)
            
            for friend in trusted:
                if friend == target_id:
                    return path + [friend]
                    
                if friend not in visited:
                    queue.append((friend, path + [friend]))
                    
        return None
    
    def get_network_stats(self) -> Dict[str, any]:
        """
        Get statistics about the trust network.
        
        Returns:
            Dictionary of network statistics
        """
        total_trust = sum(r.trust_value for r in self.relationships.values())
        avg_trust = total_trust / len(self.relationships) if self.relationships else 0.0
        
        return {
            'total_friends': len(self.friends),
            'total_relationships': len(self.relationships),
            'average_trust': avg_trust,
            'max_trust': max((r.trust_value for r in self.relationships.values()), default=0.0),
            'min_trust': min((r.trust_value for r in self.relationships.values()), default=0.0)
        }
