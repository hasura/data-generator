from enum import Enum


class AutoName(Enum):
    # Automatically use name as value
    def _generate_next_value_(name, start, count, last_values):
        return name  # Use the member name as the value
