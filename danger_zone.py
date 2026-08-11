"""
danger_zone.py
--------------
[STUB — Phase 3]

Responsible for:
  - Holding the configurable danger-zone polygon.
  - Exposing point-in-zone and distance-to-zone queries.
  - Converting normalised coordinates to pixel coordinates.

This stub does nothing.  It will be fully implemented in Phase 3.
"""

from __future__ import annotations

import numpy as np


class DangerZone:
    """
    Represents the dangerous curve section as a convex or concave polygon.

    Coordinates are stored normalised ([0,1] range) and converted to pixels
    on demand, so the zone works correctly regardless of video resolution.

    Will be fully implemented in Phase 3.
    """

    def is_inside(self, point: tuple[int, int], frame_shape: tuple) -> bool:
        """Returns True when the given pixel point is inside the zone."""
        return False   # stub

    def distance_to_boundary(self, point: tuple[int, int], frame_shape: tuple) -> float:
        """Returns the approximate pixel distance from a point to the nearest zone edge."""
        return float("inf")   # stub
