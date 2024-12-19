from enum import Enum
from uuid import UUID
from pydantic import BaseModel

class Profile(str, Enum):
    standard = "standard"

class VlanType(str, Enum):
    baremetal = "bm"

class L2VNLogical(BaseModel):
    virtual_network_name: str
    servers: list[str]
    uplink_connection_type: str
    downlink_connection_type: str
    vlan_type: VlanType = VlanType.baremetal

class L2VNCreateRequest(BaseModel):
    id: UUID
    pod: str
    tenant_name: str
    profile: Profile = Profile.standard
    logical: list[L2VNLogical]