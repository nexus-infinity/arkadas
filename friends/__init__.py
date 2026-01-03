"""
Friends Module - Polymorphic friend network.

Implements distributed friend intelligence with trust relationships
and collective emergence capabilities.
"""

from .dal_friend import DALFriend
from .trust_web import TrustWeb
from .emergence import CollectiveIntelligence

__all__ = ['DALFriend', 'TrustWeb', 'CollectiveIntelligence']
