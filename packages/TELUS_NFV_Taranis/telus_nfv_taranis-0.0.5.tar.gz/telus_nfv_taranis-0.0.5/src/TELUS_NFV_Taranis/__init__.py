"""
This module provides types used for NATS messages.

It allows for python NATS clients to validate the messages they send and receive.
"""

from .schemas import Environment, Type, Version, Profile, VlanType, L2VNLogical, L2VNCreateRequest, L2VNCreateResponseSuccess, \
                    L2VNCreateResponseFailure, Community, L3VNCreateRequest, L3VNCreateResponseSuccess, L3VNCreateResponseFailure, \
                    E2ECreateRequest, E2ECreateResponseSuccess, E2ECreateResponseFailure

__version__ = "0.0.5"