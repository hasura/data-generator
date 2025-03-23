import random
from enum import Enum


class SystemType(str, Enum):
    """
    Enumeration of host system types in the security schema
    as defined in the DBML
    """
    SERVER = "SERVER"
    WORKSTATION = "WORKSTATION"
    LAPTOP = "LAPTOP"
    VIRTUAL_MACHINE = "VIRTUAL_MACHINE"
    CONTAINER = "CONTAINER"
    APPLIANCE = "APPLIANCE"

    @classmethod
    def get_random(cls):
        """
        Return a random system type with realistic distribution
        """
        weights = {
            cls.SERVER: 0.3,
            cls.WORKSTATION: 0.3,
            cls.LAPTOP: 0.2,
            cls.VIRTUAL_MACHINE: 0.1,
            cls.CONTAINER: 0.05,
            cls.APPLIANCE: 0.05
        }
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]

    def to_display_value(self):
        """
        Convert enum value to lowercase display format
        """
        display_map = {
            self.SERVER: "server",
            self.WORKSTATION: "workstation",
            self.LAPTOP: "laptop",
            self.VIRTUAL_MACHINE: "virtual machine",
            self.CONTAINER: "container",
            self.APPLIANCE: "appliance"
        }
        return display_map.get(self, self.value.lower())
