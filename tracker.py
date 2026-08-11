"""
tracker.py
----------
[STUB — Phase 2]

Responsible for:
  - Wrapping the ByteTrack algorithm.
  - Accepting a list of Detection objects each frame.
  - Returning TrackedVehicle objects with persistent IDs.
  - Maintaining per-vehicle position history.

This stub does nothing.  It will be fully implemented in Phase 2.
"""

from __future__ import annotations

from detector import Detection


class TrackedVehicle:
    """
    A Detection enriched with a persistent tracking ID and position history.
    Will be fully defined in Phase 2.
    """
    pass


class VehicleTracker:
    """
    Wraps ByteTrack.  Will be fully implemented in Phase 2.
    """

    def update(self, detections: list[Detection], frame_shape: tuple) -> list[TrackedVehicle]:
        """
        Phase 2 will implement real tracking here.
        For now, returns an empty list so the rest of the pipeline
        can still import and reference this class without errors.
        """
        return []
