"""
warning.py
----------
[STUB — Phase 6]

Responsible for:
  - Consuming RiskResult objects from the risk analyzer.
  - Deciding when to fire a warning (e.g., any HIGH-risk vehicle present).
  - Returning a WarningState consumed by the visualizer.

This stub does nothing.  It will be fully implemented in Phase 6.
"""

from __future__ import annotations

from dataclasses import dataclass

from risk_analyzer import RiskLevel, RiskResult


@dataclass
class WarningState:
    """
    Describes the current warning status for the visualizer to render.

    Attributes
    ----------
    active : bool
        True when at least one vehicle meets the warning criteria.
    message : str
        The text to display on screen when active is True.
    """
    active: bool = False
    message: str = ""


class WarningSystem:
    """
    Translates risk results into a single WarningState.
    Will be fully implemented in Phase 6.
    """

    def evaluate(self, risk_results: list[RiskResult]) -> WarningState:
        """
        Phase 6 will implement real warning logic here.
        Returns an inactive warning for now.
        """
        return WarningState(active=False)
