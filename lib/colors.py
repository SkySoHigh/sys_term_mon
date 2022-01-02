"""Provides access to metrics value colorization by thresholds."""

from typing import Any

from lib.enums import ColorCodes, Thresholds


class Colorize:
    """
    Colorize the text according to the specified threshold
    """

    @staticmethod
    def _colorize_text(text: str, color: ColorCodes) -> str:
        return "\033[{color_code}m {text}\033[0m".format(color_code=color.value, text=text)

    @staticmethod
    def by_thresholds(metric: Any, threshold: Thresholds) -> str:
        """
        Colorize text according to the specified threshold.
        Args:
            metric: Metric to colorize
            threshold: Enum with values for warning and critical thresholds

        Returns: Colorized value as str
        """

        try:
            metric = float(metric)
        except TypeError:
            return metric

        warning, critical = threshold.value

        if float(critical) <= metric:
            return Colorize._colorize_text(str(metric), color=ColorCodes.red)
        elif float(warning) <= metric <= float(critical):
            return Colorize._colorize_text(str(metric), color=ColorCodes.yellow)
        else:
            return Colorize._colorize_text(str(metric), color=ColorCodes.green)
