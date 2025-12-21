"""
ARKADAŠ Train Station Module
=============================

The Train Station provides intelligent data routing and scheduling,
ensuring information arrives at the right destination at the right time.

Like a train station routing trains to platforms, this module routes
data packets through the system based on priority and destination.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time

from .jefferies_tubes import DataPacket, ChannelPriority


class RoutingStrategy(Enum):
    """Strategies for routing data."""
    ROUND_ROBIN = "round_robin"
    PRIORITY_BASED = "priority_based"
    LOAD_BALANCED = "load_balanced"
    INTELLIGENT = "intelligent"


@dataclass
class Platform:
    """A platform in the train station where data arrives/departs."""
    platform_id: int
    destination: str
    queue: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=100))
    packets_processed: int = 0
    active: bool = True


@dataclass
class StationConfig:
    """Configuration for the Train Station."""
    platforms: int = 4
    routing: str = "intelligent"
    queue_size: int = 100
    priority_levels: int = 4


class TrainStation:
    """
    Intelligent data routing and scheduling hub.
    
    Routes data packets between components:
    - Aperture readings → Synchronizer
    - Sensor data → OBI-WAN network
    - Unified data → Dojo for training
    - Status updates → Monitoring
    """
    
    def __init__(self, config: Optional[StationConfig] = None):
        """
        Initialize the Train Station.
        
        Args:
            config: Station configuration
        """
        self.config = config or StationConfig()
        self.platforms: Dict[int, Platform] = {}
        self.routes: Dict[str, List[int]] = {}  # destination -> platform_ids
        self.active = False
        self.current_platform = 0  # For round-robin
        
        # Initialize platforms
        for i in range(self.config.platforms):
            platform = Platform(
                platform_id=i,
                destination=f"platform_{i}",
                queue=asyncio.Queue(maxsize=self.config.queue_size)
            )
            self.platforms[i] = platform
    
    def register_route(self, destination: str, platform_id: int) -> None:
        """
        Register a route from destination to platform.
        
        Args:
            destination: Destination component name
            platform_id: Platform to use for this destination
        """
        if destination not in self.routes:
            self.routes[destination] = []
        
        if platform_id not in self.routes[destination]:
            self.routes[destination].append(platform_id)
            
            # Update platform destination
            if platform_id in self.platforms:
                self.platforms[platform_id].destination = destination
    
    def get_platform_for_destination(
        self,
        destination: str,
        priority: ChannelPriority = ChannelPriority.NORMAL
    ) -> Optional[int]:
        """
        Determine which platform to use for a destination.
        
        Args:
            destination: Target destination
            priority: Packet priority
            
        Returns:
            Platform ID if found
        """
        # Check if we have registered routes
        if destination in self.routes:
            platforms = self.routes[destination]
            
            if not platforms:
                return None
            
            # Select based on routing strategy
            if self.config.routing == "intelligent":
                return self._intelligent_select(platforms, priority)
            elif self.config.routing == "load_balanced":
                return self._load_balanced_select(platforms)
            elif self.config.routing == "priority_based":
                return self._priority_select(platforms, priority)
            else:  # round_robin
                return self._round_robin_select(platforms)
        
        # No registered route, use round-robin
        return self._round_robin_select(list(self.platforms.keys()))
    
    def _round_robin_select(self, platforms: List[int]) -> int:
        """Select platform using round-robin."""
        platform = platforms[self.current_platform % len(platforms)]
        self.current_platform += 1
        return platform
    
    def _load_balanced_select(self, platforms: List[int]) -> int:
        """Select least loaded platform."""
        min_load = float('inf')
        selected = platforms[0]
        
        for platform_id in platforms:
            platform = self.platforms[platform_id]
            load = platform.queue.qsize()
            
            if load < min_load:
                min_load = load
                selected = platform_id
        
        return selected
    
    def _priority_select(
        self,
        platforms: List[int],
        priority: ChannelPriority
    ) -> int:
        """Select platform based on priority."""
        # Higher priority gets first platforms
        if priority == ChannelPriority.CRITICAL:
            return platforms[0]
        elif priority == ChannelPriority.HIGH:
            return platforms[min(1, len(platforms) - 1)]
        else:
            return platforms[-1]
    
    def _intelligent_select(
        self,
        platforms: List[int],
        priority: ChannelPriority
    ) -> int:
        """
        Intelligently select platform based on multiple factors.
        
        Considers: load, priority, and historical performance.
        """
        # Score each platform
        scores = {}
        
        for platform_id in platforms:
            platform = self.platforms[platform_id]
            
            # Lower queue size is better
            load_score = 1.0 - (platform.queue.qsize() / self.config.queue_size)
            
            # Active platforms preferred
            active_score = 1.0 if platform.active else 0.0
            
            # Combine scores
            scores[platform_id] = (load_score + active_score) / 2.0
        
        # Select highest score
        return max(scores.keys(), key=lambda k: scores[k])
    
    async def route_packet(self, packet: DataPacket) -> bool:
        """
        Route a data packet to appropriate platform.
        
        Args:
            packet: Packet to route
            
        Returns:
            True if routed successfully
        """
        platform_id = self.get_platform_for_destination(
            packet.destination,
            packet.priority
        )
        
        if platform_id is None:
            return False
        
        platform = self.platforms[platform_id]
        
        try:
            await asyncio.wait_for(
                platform.queue.put(packet),
                timeout=1.0
            )
            return True
        except asyncio.TimeoutError:
            return False
    
    async def dispatch_from_platform(
        self,
        platform_id: int,
        handler: Any
    ) -> None:
        """
        Dispatch packets from a platform to a handler.
        
        Args:
            platform_id: Platform to dispatch from
            handler: Handler function for packets
        """
        if platform_id not in self.platforms:
            return
        
        platform = self.platforms[platform_id]
        
        while self.active and platform.active:
            try:
                packet = await asyncio.wait_for(
                    platform.queue.get(),
                    timeout=0.1
                )
                
                # Process packet
                await handler(packet)
                platform.packets_processed += 1
                
            except asyncio.TimeoutError:
                continue
    
    def start(self) -> None:
        """Start the train station."""
        self.active = True
    
    def stop(self) -> None:
        """Stop the train station."""
        self.active = False
    
    def get_platform_stats(self, platform_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a platform.
        
        Args:
            platform_id: Platform to query
            
        Returns:
            Statistics dictionary
        """
        if platform_id not in self.platforms:
            return None
        
        platform = self.platforms[platform_id]
        
        return {
            "platform_id": platform_id,
            "destination": platform.destination,
            "queue_size": platform.queue.qsize(),
            "packets_processed": platform.packets_processed,
            "active": platform.active
        }
    
    def get_station_stats(self) -> Dict[str, Any]:
        """Get overall station statistics."""
        total_packets = sum(
            p.packets_processed for p in self.platforms.values()
        )
        
        platform_stats = [
            self.get_platform_stats(pid)
            for pid in self.platforms.keys()
        ]
        
        return {
            "active": self.active,
            "total_platforms": len(self.platforms),
            "total_packets_processed": total_packets,
            "routing_strategy": self.config.routing,
            "registered_routes": len(self.routes),
            "platforms": platform_stats
        }
    
    def clear_platform(self, platform_id: int) -> int:
        """
        Clear all packets from a platform.
        
        Args:
            platform_id: Platform to clear
            
        Returns:
            Number of packets cleared
        """
        if platform_id not in self.platforms:
            return 0
        
        platform = self.platforms[platform_id]
        count = 0
        
        while not platform.queue.empty():
            try:
                platform.queue.get_nowait()
                count += 1
            except asyncio.QueueEmpty:
                break
        
        return count
