from enum import Enum


class PatchStatus(str, Enum):
    """
    Enumeration of host patch statuses in the security schema
    as defined in the DBML
    """
    CURRENT = "CURRENT"
    UP_TO_DATE = "UP_TO_DATE"
    OUTDATED = "OUTDATED"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_days(cls, days: int):
        """
        Calculate patch status based on days since last patch
        """
        if 0 <= days <= 7:
            return cls.CURRENT
        elif 8 <= days <= 30:
            return cls.UP_TO_DATE
        elif 31 <= days <= 90:
            return cls.OUTDATED
        elif days > 90:
            return cls.CRITICAL
        else:
            return cls.UNKNOWN

    def to_display_value(self):
        """
        Convert enum value to lowercase display format
        """
        display_map = {
            self.CURRENT: "current",
            self.UP_TO_DATE: "up-to-date",
            self.OUTDATED: "outdated",
            self.CRITICAL: "critical",
            self.UNKNOWN: "unknown"
        }
        return display_map.get(self, self.value.lower())
