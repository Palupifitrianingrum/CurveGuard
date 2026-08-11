"""
visualizer.py
-------------
Responsible for all OpenCV drawing operations.

This module is the ONLY place where cv2 drawing functions are called.
It receives a frame and structured data, draws everything, and returns
the annotated frame.  It does not run any detection, tracking, or logic.

Phase 1 draws:
  - bounding boxes, coloured by vehicle class
  - class label + confidence score
  - FPS counter

Later phases will add:
  - tracking ID and trajectory lines  (Phase 2)
  - danger-zone polygon               (Phase 3)
  - warning banner                    (Phase 6)
"""

from __future__ import annotations

import cv2
import numpy as np

from detector import Detection

# ---------------------------------------------------------------------------
# Colour palette — one BGR colour per vehicle class (bus/car/motorbike/truck)
# ---------------------------------------------------------------------------
_CLASS_COLORS: dict[str, tuple[int, int, int]] = {
    "bus":       (0,   165, 255),   # orange
    "car":       (0,   255,   0),   # green
    "motorbike": (255,   0, 255),   # magenta
    "truck":     (255, 165,   0),   # blue-ish
}
_DEFAULT_COLOR: tuple[int, int, int] = (200, 200, 200)   # grey fallback


def _get_class_color(class_name: str) -> tuple[int, int, int]:
    return _CLASS_COLORS.get(class_name, _DEFAULT_COLOR)


# ---------------------------------------------------------------------------
# Phase 1 drawing helpers
# ---------------------------------------------------------------------------

def draw_detections(
    frame: np.ndarray,
    detections: list[Detection],
) -> np.ndarray:
    """
    Draw bounding boxes and labels for a list of detections.

    Parameters
    ----------
    frame : np.ndarray
        The frame to draw onto (will be modified in-place).
    detections : list[Detection]
        Detections produced by VehicleDetector.detect().

    Returns
    -------
    np.ndarray
        The same frame with annotations drawn on it.
    """
    for det in detections:
        x1, y1, x2, y2 = det.bbox
        color = _get_class_color(det.class_name)

        # Bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=2)

        # Label: "car 0.87"
        label = f"{det.class_name} {det.confidence:.2f}"
        _draw_label(frame, label, x1, y1, color)

    return frame


def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    """
    Draw the FPS counter in the top-left corner.

    Parameters
    ----------
    frame : np.ndarray
        The frame to draw onto (modified in-place).
    fps : float
        Current frames-per-second value.

    Returns
    -------
    np.ndarray
        Annotated frame.
    """
    text = f"FPS: {fps:.1f}"
    cv2.putText(
        frame, text,
        org=(10, 28),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.8,
        color=(0, 255, 255),
        thickness=2,
        lineType=cv2.LINE_AA,
    )
    return frame


# ---------------------------------------------------------------------------
# Internal utility
# ---------------------------------------------------------------------------

def _draw_label(
    frame: np.ndarray,
    text: str,
    x: int,
    y: int,
    color: tuple[int, int, int],
) -> None:
    """
    Draw a filled rectangle behind the text so it is always readable.
    The label is placed just above the top-left corner of the bounding box.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    thickness = 1

    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Position the label above the box; clamp to frame top if needed.
    label_y = max(y - 4, text_h + baseline + 4)

    # Background rectangle
    cv2.rectangle(
        frame,
        (x, label_y - text_h - baseline - 2),
        (x + text_w + 2, label_y + 2),
        color,
        thickness=cv2.FILLED,
    )

    # Text in black so it contrasts against any coloured background
    cv2.putText(
        frame,
        text,
        org=(x + 1, label_y - baseline),
        fontFace=font,
        fontScale=font_scale,
        color=(0, 0, 0),
        thickness=thickness,
        lineType=cv2.LINE_AA,
    )
