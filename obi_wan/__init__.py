"""
OBI-WAN: Omnidirectional Biological Intelligence - Wisdom Aggregation Network
==============================================================================

The OBI-WAN system represents a collective intelligence network that 
aggregates wisdom from multiple omnidirectional sensors, creating a 
unified field of awareness inspired by the Force.

OBI-WAN stands for:
- **O**mnidirectional
- **B**iological
- **I**ntelligence
- **W**isdom
- **A**ggregation
- **N**etwork

Like Obi-Wan Kenobi's connection to the Force, this network perceives
all directions simultaneously and synthesizes knowledge into actionable wisdom.
"""

from .sensor_node import SensorNode, SensorType
from .network import ObiWanNetwork
from .collective_intelligence import CollectiveIntelligence

__all__ = [
    'SensorNode',
    'SensorType',
    'ObiWanNetwork',
    'CollectiveIntelligence'
]

__version__ = "0.1.0"
