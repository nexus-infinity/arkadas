"""
Emergence Module - Collective intelligence.

Implements emergent collective intelligence through friend network interactions,
enabling sophisticated group behaviors and decision making.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import statistics


class EmergentBehavior:
    """Represents an emergent behavior in the collective."""
    
    def __init__(self, behavior_id: str, description: str):
        """
        Initialize emergent behavior.
        
        Args:
            behavior_id: Unique behavior identifier
            description: Description of the behavior
        """
        self.behavior_id = behavior_id
        self.description = description
        self.participants: List[str] = []
        self.strength = 0.0
        self.emergence_time = datetime.now()
        
    def add_participant(self, friend_id: str):
        """
        Add participant to behavior.
        
        Args:
            friend_id: Friend participating in behavior
        """
        if friend_id not in self.participants:
            self.participants.append(friend_id)
            self._update_strength()
            
    def remove_participant(self, friend_id: str):
        """
        Remove participant from behavior.
        
        Args:
            friend_id: Friend to remove
        """
        if friend_id in self.participants:
            self.participants.remove(friend_id)
            self._update_strength()
            
    def _update_strength(self):
        """Update behavior strength based on participants."""
        # Strength increases with more participants
        self.strength = min(1.0, len(self.participants) / 10.0)


class CollectiveIntelligence:
    """Manages collective intelligence emergence in friend network."""
    
    def __init__(self):
        """Initialize collective intelligence system."""
        self.behaviors: Dict[str, EmergentBehavior] = {}
        self.collective_memory: Dict[str, Any] = {}
        self.consensus_threshold = 0.6
        self.decision_history = []
        
    def register_behavior(self, behavior_id: str, description: str) -> EmergentBehavior:
        """
        Register a new emergent behavior.
        
        Args:
            behavior_id: Behavior identifier
            description: Behavior description
            
        Returns:
            Created EmergentBehavior
        """
        behavior = EmergentBehavior(behavior_id, description)
        self.behaviors[behavior_id] = behavior
        return behavior
    
    def contribute_to_behavior(self, behavior_id: str, friend_id: str):
        """
        Have a friend contribute to an emergent behavior.
        
        Args:
            behavior_id: Behavior to contribute to
            friend_id: Contributing friend
        """
        if behavior_id in self.behaviors:
            self.behaviors[behavior_id].add_participant(friend_id)
            
    def collective_decision(self, 
                           question: str,
                           votes: Dict[str, Any],
                           weights: Optional[Dict[str, float]] = None) -> Any:
        """
        Make a collective decision based on weighted votes.
        
        Args:
            question: Decision question
            votes: Dictionary of friend_id -> vote
            weights: Optional weights for each friend's vote
            
        Returns:
            Collective decision result
        """
        if not votes:
            return None
            
        if weights is None:
            weights = {friend_id: 1.0 for friend_id in votes.keys()}
            
        # Count weighted votes
        vote_counts: Dict[Any, float] = {}
        total_weight = 0.0
        
        for friend_id, vote in votes.items():
            weight = weights.get(friend_id, 1.0)
            vote_counts[vote] = vote_counts.get(vote, 0.0) + weight
            total_weight += weight
            
        # Find consensus
        if not vote_counts:
            return None
            
        winning_vote = max(vote_counts.items(), key=lambda x: x[1])
        consensus_strength = winning_vote[1] / total_weight if total_weight > 0 else 0
        
        decision = {
            'question': question,
            'result': winning_vote[0],
            'consensus_strength': consensus_strength,
            'reached_consensus': consensus_strength >= self.consensus_threshold,
            'timestamp': datetime.now(),
            'voter_count': len(votes)
        }
        
        self.decision_history.append(decision)
        return decision['result']
    
    def aggregate_knowledge(self, 
                           contributions: Dict[str, float],
                           aggregation_method: str = "average") -> float:
        """
        Aggregate knowledge contributions from multiple friends.
        
        Args:
            contributions: Dictionary of friend_id -> contribution value
            aggregation_method: Method to use ("average", "median", "max", "min")
            
        Returns:
            Aggregated value
        """
        if not contributions:
            return 0.0
            
        values = list(contributions.values())
        
        if aggregation_method == "average":
            return sum(values) / len(values)
        elif aggregation_method == "median":
            return statistics.median(values)
        elif aggregation_method == "max":
            return max(values)
        elif aggregation_method == "min":
            return min(values)
        else:
            return sum(values) / len(values)
            
    def store_collective_memory(self, key: str, value: Any, contributors: List[str]):
        """
        Store information in collective memory.
        
        Args:
            key: Memory key
            value: Memory value
            contributors: List of contributing friend IDs
        """
        self.collective_memory[key] = {
            'value': value,
            'contributors': contributors,
            'timestamp': datetime.now(),
            'confidence': len(contributors) / 10.0  # More contributors = higher confidence
        }
        
    def recall_collective_memory(self, key: str) -> Optional[Any]:
        """
        Recall information from collective memory.
        
        Args:
            key: Memory key
            
        Returns:
            Memory value or None
        """
        memory = self.collective_memory.get(key)
        return memory['value'] if memory else None
    
    def get_emergence_summary(self) -> Dict[str, Any]:
        """
        Get summary of collective intelligence state.
        
        Returns:
            Dictionary containing emergence statistics
        """
        active_behaviors = sum(1 for b in self.behaviors.values() if b.strength > 0.3)
        total_participants = sum(len(b.participants) for b in self.behaviors.values())
        
        return {
            'total_behaviors': len(self.behaviors),
            'active_behaviors': active_behaviors,
            'total_participants': total_participants,
            'collective_memory_size': len(self.collective_memory),
            'decisions_made': len(self.decision_history),
            'average_consensus': self._calculate_average_consensus()
        }
    
    def _calculate_average_consensus(self) -> float:
        """Calculate average consensus strength across decisions."""
        if not self.decision_history:
            return 0.0
            
        consensus_values = [d['consensus_strength'] for d in self.decision_history]
        return sum(consensus_values) / len(consensus_values)
    
    def detect_emergence(self, min_participants: int = 3, min_strength: float = 0.5) -> List[str]:
        """
        Detect strongly emergent behaviors.
        
        Args:
            min_participants: Minimum participants for emergence
            min_strength: Minimum strength threshold
            
        Returns:
            List of emergent behavior IDs
        """
        emergent = []
        for behavior_id, behavior in self.behaviors.items():
            if len(behavior.participants) >= min_participants and behavior.strength >= min_strength:
                emergent.append(behavior_id)
        return emergent
