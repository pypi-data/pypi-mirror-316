"""
This module provides types used for NATS messages.

It allows for python NATS clients to validate the messages they send and receive.
"""

from .message_schemas import Profile, VlanType, L2VNLogical, L2VNCreateRequest

__version__ = "0.0.2"