"""
ARKADAŠ Jefferies Tubes Module
===============================

Named after the maintenance conduits in Star Trek, Jefferies Tubes
provide the data conduits for the King's Chamber system, allowing
information to flow between all components.

The tubes use async channels for high-bandwidth, low-latency data transfer.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Dict, Callable
from typing import Awaitable
from enum import Enum


class ChannelPriority(Enum):
    """Priority levels for data channels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DataPacket:
    """A packet of data flowing through the tubes."""
    source: str
    destination: str
    payload: Any
    priority: ChannelPriority = ChannelPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0


@dataclass
class TubeConfig:
    """Configuration for Jefferies Tubes system."""
    channels: int = 8
    bandwidth: str = "high"
    protocol: str = "async"
    buffer_size: int = 1000
    max_retries: int = 3


class JefferiesTubes:
    """
    Data conduit system for the King's Chamber.
    
    Provides async channels for data flow between:
    - Aperture ↔ Synchronizer
    - Synchronizer ↔ OBI-WAN
    - OBI-WAN ↔ Dojo
    - All components ↔ Train Station
    """
    
    def __init__(self, config: Optional[TubeConfig] = None):
        """
        Initialize Jefferies Tubes system.
        
        Args:
            config: Tube configuration
        """
        self.config = config or TubeConfig()
        self.channels: Dict[str, asyncio.Queue] = {}
        self.active = False
        self.handlers: Dict[str, Callable] = {}
        self.stats: Dict[str, int] = {}
        
        # Initialize channels
        for i in range(self.config.channels):
            channel_name = f"tube_{i}"
            self.channels[channel_name] = asyncio.Queue(maxsize=self.config.buffer_size)
            self.stats[channel_name] = 0
    
    def create_channel(self, name: str) -> asyncio.Queue:
        """
        Create a named channel.
        
        Args:
            name: Channel name
            
        Returns:
            Async queue for the channel
        """
        if name not in self.channels:
            self.channels[name] = asyncio.Queue(maxsize=self.config.buffer_size)
            self.stats[name] = 0
        return self.channels[name]
    
    def get_channel(self, name: str) -> Optional[asyncio.Queue]:
        """
        Get a channel by name.
        
        Args:
            name: Channel name
            
        Returns:
            Queue if exists, None otherwise
        """
        return self.channels.get(name)
    
    async def send(
        self,
        channel_name: str,
        source: str,
        destination: str,
        payload: Any,
        priority: ChannelPriority = ChannelPriority.NORMAL
    ) -> bool:
        """
        Send data through a channel.
        
        Args:
            channel_name: Name of channel to use
            source: Source component name
            destination: Destination component name
            payload: Data to send
            priority: Message priority
            
        Returns:
            True if sent successfully
        """
        channel = self.get_channel(channel_name)
        if not channel:
            return False
        
        packet = DataPacket(
            source=source,
            destination=destination,
            payload=payload,
            priority=priority,
            timestamp=asyncio.get_event_loop().time()
        )
        
        try:
            await asyncio.wait_for(channel.put(packet), timeout=1.0)
            self.stats[channel_name] += 1
            return True
        except asyncio.TimeoutError:
            return False
    
    async def receive(
        self,
        channel_name: str,
        timeout: Optional[float] = None
    ) -> Optional[DataPacket]:
        """
        Receive data from a channel.
        
        Args:
            channel_name: Name of channel to receive from
            timeout: Optional timeout in seconds
            
        Returns:
            DataPacket if available, None otherwise
        """
        channel = self.get_channel(channel_name)
        if not channel:
            return None
        
        try:
            if timeout:
                packet = await asyncio.wait_for(channel.get(), timeout=timeout)
            else:
                packet = await channel.get()
            return packet
        except asyncio.TimeoutError:
            return None
    
    def register_handler(
        self,
        channel_name: str,
        handler: Callable[[DataPacket], Awaitable[None]]
    ) -> None:
        """
        Register a handler for a channel.
        
        Args:
            channel_name: Channel to handle
            handler: Async function to handle packets
        """
        self.handlers[channel_name] = handler
    
    async def start_handlers(self) -> None:
        """Start all registered handlers."""
        self.active = True
        tasks = []
        
        for channel_name, handler in self.handlers.items():
            task = asyncio.create_task(
                self._handler_loop(channel_name, handler)
            )
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks)
    
    async def _handler_loop(
        self,
        channel_name: str,
        handler: Callable
    ) -> None:
        """
        Run handler loop for a channel.
        
        Args:
            channel_name: Channel to monitor
            handler: Handler function
        """
        while self.active:
            packet = await self.receive(channel_name, timeout=0.1)
            if packet:
                try:
                    await handler(packet)
                except Exception as e:
                    # Log error but continue
                    print(f"Handler error on {channel_name}: {e}")
    
    def stop(self) -> None:
        """Stop all handlers."""
        self.active = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tube statistics."""
        channel_stats = []
        for name, count in self.stats.items():
            channel = self.channels[name]
            channel_stats.append({
                "name": name,
                "packets_sent": count,
                "queue_size": channel.qsize(),
                "queue_full": channel.full()
            })
        
        return {
            "total_channels": len(self.channels),
            "active": self.active,
            "config": {
                "bandwidth": self.config.bandwidth,
                "protocol": self.config.protocol
            },
            "channels": channel_stats
        }
    
    def clear_channel(self, channel_name: str) -> int:
        """
        Clear all packets from a channel.
        
        Args:
            channel_name: Channel to clear
            
        Returns:
            Number of packets cleared
        """
        channel = self.get_channel(channel_name)
        if not channel:
            return 0
        
        count = 0
        while not channel.empty():
            try:
                channel.get_nowait()
                count += 1
            except asyncio.QueueEmpty:
                break
        
        return count
