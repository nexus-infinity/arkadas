"""
Feedback Module - Communication layer.

Provides bidirectional communication and feedback mechanisms
for system observation and control.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum


class FeedbackType(Enum):
    """Types of feedback messages."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    QUERY = "query"


class FeedbackMessage:
    """Individual feedback message."""
    
    def __init__(self, 
                 message: str,
                 feedback_type: FeedbackType = FeedbackType.INFO,
                 source: str = "system",
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize feedback message.
        
        Args:
            message: Message content
            feedback_type: Type of feedback
            source: Source of the message
            metadata: Optional additional data
        """
        self.message = message
        self.feedback_type = feedback_type
        self.source = source
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        self.acknowledged = False
        
    def acknowledge(self):
        """Mark message as acknowledged."""
        self.acknowledged = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'message': self.message,
            'type': self.feedback_type.value,
            'source': self.source,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'acknowledged': self.acknowledged
        }


class FeedbackLayer:
    """Communication layer for system feedback and control."""
    
    def __init__(self):
        """Initialize feedback layer."""
        self.messages: List[FeedbackMessage] = []
        self.subscribers: Dict[FeedbackType, List[Callable]] = {
            feedback_type: [] for feedback_type in FeedbackType
        }
        self.max_messages = 1000
        
    def send_feedback(self,
                     message: str,
                     feedback_type: FeedbackType = FeedbackType.INFO,
                     source: str = "system",
                     metadata: Optional[Dict[str, Any]] = None) -> FeedbackMessage:
        """
        Send a feedback message.
        
        Args:
            message: Message content
            feedback_type: Type of feedback
            source: Source of message
            metadata: Optional metadata
            
        Returns:
            Created FeedbackMessage
        """
        fb_msg = FeedbackMessage(message, feedback_type, source, metadata)
        self.messages.append(fb_msg)
        
        # Trim old messages if limit exceeded
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            
        # Notify subscribers
        self._notify_subscribers(fb_msg)
        
        return fb_msg
    
    def subscribe(self, feedback_type: FeedbackType, callback: Callable):
        """
        Subscribe to feedback of a specific type.
        
        Args:
            feedback_type: Type of feedback to subscribe to
            callback: Function to call when feedback received
        """
        self.subscribers[feedback_type].append(callback)
        
    def _notify_subscribers(self, message: FeedbackMessage):
        """
        Notify subscribers of new feedback.
        
        Args:
            message: Feedback message to distribute
        """
        for callback in self.subscribers[message.feedback_type]:
            try:
                callback(message)
            except Exception as e:
                # Don't let subscriber errors break the system
                print(f"Subscriber error: {e}")
                
    def get_recent_messages(self, 
                           count: int = 10,
                           feedback_type: Optional[FeedbackType] = None) -> List[FeedbackMessage]:
        """
        Get recent feedback messages.
        
        Args:
            count: Number of messages to retrieve
            feedback_type: Optional filter by type
            
        Returns:
            List of recent messages
        """
        messages = self.messages
        
        if feedback_type:
            messages = [m for m in messages if m.feedback_type == feedback_type]
            
        return messages[-count:]
    
    def get_unacknowledged(self) -> List[FeedbackMessage]:
        """
        Get all unacknowledged messages.
        
        Returns:
            List of unacknowledged messages
        """
        return [m for m in self.messages if not m.acknowledged]
    
    def acknowledge_message(self, timestamp: datetime):
        """
        Acknowledge a message by timestamp.
        
        Args:
            timestamp: Timestamp of message to acknowledge
        """
        for message in self.messages:
            if message.timestamp == timestamp:
                message.acknowledge()
                break
                
    def clear_messages(self, acknowledged_only: bool = False):
        """
        Clear messages.
        
        Args:
            acknowledged_only: If True, only clear acknowledged messages
        """
        if acknowledged_only:
            self.messages = [m for m in self.messages if not m.acknowledged]
        else:
            self.messages.clear()
