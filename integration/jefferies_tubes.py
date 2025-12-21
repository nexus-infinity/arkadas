"""
Jefferies Tubes Module - Pulse sync channels.

Provides synchronization channels for pulse-based communication,
inspired by Star Trek's utility conduits for system-wide coordination.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import time


class Pulse:
    """Represents a synchronization pulse."""
    
    def __init__(self, pulse_id: str, data: Any, priority: int = 5):
        """
        Initialize a pulse.
        
        Args:
            pulse_id: Unique pulse identifier
            data: Pulse data payload
            priority: Priority level (1-10, higher = more priority)
        """
        self.pulse_id = pulse_id
        self.data = data
        self.priority = priority
        self.timestamp = datetime.now()
        self.propagation_count = 0
        
    def propagate(self):
        """Record pulse propagation."""
        self.propagation_count += 1


class SyncChannel:
    """Individual synchronization channel."""
    
    def __init__(self, channel_id: str, bandwidth: int = 100):
        """
        Initialize sync channel.
        
        Args:
            channel_id: Channel identifier
            bandwidth: Maximum pulses per second
        """
        self.channel_id = channel_id
        self.bandwidth = bandwidth
        self.pulse_queue: List[Pulse] = []
        self.subscribers: List[Callable] = []
        self.active = True
        self.pulses_sent = 0
        
    def send_pulse(self, pulse: Pulse):
        """
        Send a pulse through the channel.
        
        Args:
            pulse: Pulse to send
        """
        if not self.active:
            return
            
        # Add to queue sorted by priority
        self.pulse_queue.append(pulse)
        self.pulse_queue.sort(key=lambda p: p.priority, reverse=True)
        
        # Limit queue size based on bandwidth
        if len(self.pulse_queue) > self.bandwidth:
            self.pulse_queue = self.pulse_queue[:self.bandwidth]
            
    def subscribe(self, callback: Callable):
        """
        Subscribe to channel pulses.
        
        Args:
            callback: Function to call on pulse receipt
        """
        self.subscribers.append(callback)
        
    def broadcast_next_pulse(self):
        """Broadcast next pulse to subscribers."""
        if not self.pulse_queue or not self.active:
            return
            
        pulse = self.pulse_queue.pop(0)
        pulse.propagate()
        self.pulses_sent += 1
        
        for subscriber in self.subscribers:
            try:
                subscriber(pulse)
            except Exception as e:
                # Don't let subscriber errors break the channel
                pass
                
    def get_status(self) -> Dict[str, Any]:
        """Get channel status."""
        return {
            'channel_id': self.channel_id,
            'active': self.active,
            'queue_length': len(self.pulse_queue),
            'bandwidth': self.bandwidth,
            'pulses_sent': self.pulses_sent,
            'subscriber_count': len(self.subscribers)
        }


class PulseSyncChannels:
    """Manages multiple pulse synchronization channels."""
    
    def __init__(self):
        """Initialize pulse sync system."""
        self.channels: Dict[str, SyncChannel] = {}
        self.global_pulse_count = 0
        self.sync_frequency = 1.0  # Hz
        
    def create_channel(self, channel_id: str, bandwidth: int = 100) -> SyncChannel:
        """
        Create a new sync channel.
        
        Args:
            channel_id: Channel identifier
            bandwidth: Channel bandwidth
            
        Returns:
            Created SyncChannel
        """
        channel = SyncChannel(channel_id, bandwidth)
        self.channels[channel_id] = channel
        return channel
    
    def send_pulse(self, channel_id: str, data: Any, priority: int = 5) -> Optional[str]:
        """
        Send a pulse through specified channel.
        
        Args:
            channel_id: Target channel
            data: Pulse data
            priority: Pulse priority
            
        Returns:
            Pulse ID or None
        """
        if channel_id not in self.channels:
            return None
            
        pulse_id = f"pulse_{self.global_pulse_count:06d}"
        self.global_pulse_count += 1
        
        pulse = Pulse(pulse_id, data, priority)
        self.channels[channel_id].send_pulse(pulse)
        
        return pulse_id
    
    def broadcast_to_all_channels(self, data: Any, priority: int = 5):
        """
        Broadcast pulse to all channels.
        
        Args:
            data: Pulse data
            priority: Pulse priority
        """
        for channel_id in self.channels:
            self.send_pulse(channel_id, data, priority)
            
    def subscribe_to_channel(self, channel_id: str, callback: Callable):
        """
        Subscribe to a channel.
        
        Args:
            channel_id: Channel to subscribe to
            callback: Callback function
        """
        if channel_id in self.channels:
            self.channels[channel_id].subscribe(callback)
            
    def process_pulses(self):
        """Process pending pulses in all channels."""
        for channel in self.channels.values():
            if channel.active and channel.pulse_queue:
                channel.broadcast_next_pulse()
                
    def sync_tick(self):
        """
        Perform a synchronization tick.
        Processes pulses across all channels.
        """
        self.process_pulses()
        
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status.
        
        Returns:
            System status information
        """
        total_queue = sum(len(c.pulse_queue) for c in self.channels.values())
        total_sent = sum(c.pulses_sent for c in self.channels.values())
        active_channels = sum(1 for c in self.channels.values() if c.active)
        
        return {
            'total_channels': len(self.channels),
            'active_channels': active_channels,
            'total_queue_depth': total_queue,
            'total_pulses_sent': total_sent,
            'sync_frequency': self.sync_frequency,
            'global_pulse_count': self.global_pulse_count
        }
    
    def activate_channel(self, channel_id: str):
        """
        Activate a channel.
        
        Args:
            channel_id: Channel to activate
        """
        if channel_id in self.channels:
            self.channels[channel_id].active = True
            
    def deactivate_channel(self, channel_id: str):
        """
        Deactivate a channel.
        
        Args:
            channel_id: Channel to deactivate
        """
        if channel_id in self.channels:
            self.channels[channel_id].active = False
            
    def clear_channel(self, channel_id: str):
        """
        Clear pulse queue in channel.
        
        Args:
            channel_id: Channel to clear
        """
        if channel_id in self.channels:
            self.channels[channel_id].pulse_queue.clear()
            
    def emergency_broadcast(self, data: Any):
        """
        Send emergency high-priority broadcast.
        
        Args:
            data: Emergency data
        """
        self.broadcast_to_all_channels(data, priority=10)
