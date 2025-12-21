"""
Integration Module - Connection points.

Provides integration interfaces for connecting ARKADAŞ with
external systems and layers in the architecture.
"""

from .train_station import TrainStationInterface
from .dojo import DOJOInterface
from .jefferies_tubes import PulseSyncChannels
from .trident import TridentValidator

__all__ = ['TrainStationInterface', 'DOJOInterface', 'PulseSyncChannels', 'TridentValidator']
