"""
Chamber Module - Core chamber logic for organic-digital synchronization.

The chamber represents the King's Chamber in the pyramid geometry,
positioned at 1/3 height for optimal resonance and synchronization.
"""

from .aperture import ApertureConverter
from .synchronizer import OrganicDigitalSync
from .light_axis import LightAxis

__all__ = ['ApertureConverter', 'OrganicDigitalSync', 'LightAxis']
