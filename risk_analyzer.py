"""
risk_analyzer.py
----------------
[STUB — Phase 5]

Responsible for:
  - Applying explainable rule-based risk analysis.
  - Receiving tracked vehicles and danger-zone data.
  - Returning a RiskResult for each vehicle, which includes:
      • a risk level  (LOW / MEDIUM / HIGH)
      • a list of triggered rules
      • a human-readable reasoning string

This stub does nothing.  It will be fully implemented in Phase 5.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    LOW    = "LOW"
    MEDIUM = "MEDIUM"
    HIGH   = "HIGH"


@dataclass
class RiskResult:
    """
    The output of one risk evaluation for a single tracked vehicle.

    Attributes
    ----------
    track_id : int
        The ByteTrack ID of the vehicle.
    level : RiskLevel
        Overall risk classification.
    triggered_rules : list[str]
        Human-readable list of rules that fired (empty when level is LOW).
    reasoning : str
        One-sentence summary suitable for logging or display.
    """
    track_id: int
    level: RiskLevel = RiskLevel.LOW
    triggered_rules: list[str] = field(default_factory=list)
    reasoning: str = ""


class RiskAnalyzer:
    """
    Applies explainable rules to tracked vehicles.
    Will be fully implemented in Phase 5.
    """

    def analyze(self, tracked_vehicles: list, danger_zone) -> list[RiskResult]:
        """
        Phase 5 will implement real rule evaluation here.
        Returns an empty list for now.
        """
        return []
