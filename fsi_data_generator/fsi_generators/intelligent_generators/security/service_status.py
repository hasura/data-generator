from enum import Enum
from fsi_data_generator.fsi_generators.intelligent_generators.security.agent_status import \
    AgentStatus

import random


class ServiceStatus(str, Enum):
    """
    Enumeration of service statuses in the security schema
    """
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    STARTING = "STARTING"
    STOPPING = "STOPPING"

    @classmethod
    def get_random(cls, agent_status=None):
        """
        Return a service status with realistic distribution based on agent status
        """
        if agent_status == AgentStatus.ACTIVE:
            # Most services running when agent is active
            weights = {
                cls.RUNNING: 0.85,
                cls.STOPPED: 0.05,
                cls.PAUSED: 0.05,
                cls.STARTING: 0.03,
                cls.STOPPING: 0.02
            }
        else:
            # Most services stopped when agent is not active
            weights = {
                cls.RUNNING: 0.3,
                cls.STOPPED: 0.6,
                cls.PAUSED: 0.05,
                cls.STARTING: 0.03,
                cls.STOPPING: 0.02
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
            self.RUNNING: "running",
            self.STOPPED: "stopped",
            self.PAUSED: "paused",
            self.STARTING: "starting",
            self.STOPPING: "stopping"
        }
        return display_map.get(self, self.value.lower())
