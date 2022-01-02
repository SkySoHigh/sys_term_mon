"""Contains enums for different proposes."""

import enum


class Thresholds(enum.Enum):
    """Metrics thresholds.

    Thresholds should be set as tuple where:
     - first value is used for warning level
     - second value is used for critical level
    """

    load_average = (10, 14)  # LA values
    virtual_memory = (80, 90)  # percent
    swap_memory = (5, 10)  # percent
    disk = (80, 95)  # percent


class ColorCodes(enum.IntEnum):
    red = 31
    green = 32
    yellow = 33
