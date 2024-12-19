from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict

# Version: 0.0.1
DATA_DEFINITIONS_VERSION = "0.0.1"


class AvailabilityEnum(str, Enum):
    unknown = "unknown"
    healthy = "healthy"
    unhealthy = "unhealthy"


class ApplicationType(str, Enum):
    drone_corridor = "drone_corridor"
    joint_delivery_highway = "joint_delivery_highway"
    joint_delivery_last_mile = "joint_delivery_last_mile"


class VersionAvailabilityRead(BaseModel):
    "A class to hold version and availability of ICDS"

    model_config = ConfigDict(json_schema_extra={"examples": [{"version": "adfgde3", "availability": "healthy"}]})
    version: str
    availability: AvailabilityEnum


class VersionAvailabilityWrite(BaseModel):
    "A class to hold version and availability information to write to the ICDS database, it is normally populated at startup time"

    id: str
    version: str
    availability: AvailabilityEnum


class DiscoveryService(BaseModel):
    "A class to hold a list of URLs and the type of service and regions"

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"application_type": "drone_corridor", "url": "https://jpn.discoveryservice.com", "region": "tokyo"}]}
    )
    application_type: ApplicationType
    url: str
    region: str


class DiscoveryServiceListRead(BaseModel):
    "A class to hold a list of URLs and the type of service"

    available_services: List[DiscoveryService]
