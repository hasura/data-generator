from enum import Enum
from fsi_data_generator.fsi_generators.intelligent_generators.security.agent_status import \
    AgentStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.patch_status import \
    PatchStatus

import random


class ComplianceStatus(str, Enum):
    """
    Enumeration of compliance statuses in the security schema
    as defined in the DBML
    """
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    EXCEPTION = "EXCEPTION"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def calculate(cls, patch_status: PatchStatus, agent_status: AgentStatus):
        """
        Determine compliance status based on patch and agent status
        """
        # If agent is not active, override compliance
        if agent_status != AgentStatus.ACTIVE:
            return random.choice([cls.NON_COMPLIANT, cls.UNKNOWN])

        # Compliance based on patch status
        compliance_map = {
            PatchStatus.CURRENT: [cls.COMPLIANT, cls.COMPLIANT, cls.COMPLIANT, cls.EXCEPTION],
            PatchStatus.UP_TO_DATE: [cls.COMPLIANT, cls.COMPLIANT, cls.NON_COMPLIANT, cls.EXCEPTION],
            PatchStatus.OUTDATED: [cls.NON_COMPLIANT, cls.NON_COMPLIANT, cls.EXCEPTION],
            PatchStatus.CRITICAL: [cls.NON_COMPLIANT, cls.NON_COMPLIANT, cls.NON_COMPLIANT, cls.EXCEPTION],
            PatchStatus.UNKNOWN: [cls.UNKNOWN, cls.NON_COMPLIANT]
        }

        return random.choice(compliance_map.get(patch_status, [cls.UNKNOWN]))

    def to_display_value(self):
        """
        Convert enum value to lowercase display format
        """
        display_map = {
            self.COMPLIANT: "compliant",
            self.NON_COMPLIANT: "non-compliant",
            self.EXCEPTION: "exception",
            self.UNKNOWN: "unknown"
        }
        return display_map.get(self, self.value.lower())
