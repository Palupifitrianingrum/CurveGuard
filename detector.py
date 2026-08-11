"""
detector.py
-----------
Responsible for:
  - Loading the YOLOv8 model once at startup.
  - Running inference on a single video frame.
  - Returning structured Detection objects.

This module does NOT know about tracking, danger zones, or risk.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ultralytics import YOLO

import config


@dataclass
class Detection:
    """
    Represents a single vehicle detection in one frame.

    Attributes
    ----------
    bbox : tuple[int, int, int, int]
        Bounding box in pixel coordinates: (x1, y1, x2, y2).
    class_id : int
        Integer class index, corresponding to config.CLASS_NAMES.
    class_name : str
        Human-readable class label (bus / car / motorbike / truck).
    confidence : float
        Detection confidence score in [0, 1].
    """

    bbox: tuple[int, int, int, int]
    class_id: int
    class_name: str
    confidence: float

    @property
    def center(self) -> tuple[int, int]:
        """Bottom-center point of the bounding box (useful for ground-plane position)."""
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, y2)

    @property
    def top_center(self) -> tuple[int, int]:
        """Top-center point of the bounding box."""
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, y1)


class VehicleDetector:
    """
    Wraps a YOLOv8 model and exposes a single `detect()` method.

    Usage
    -----
        detector = VehicleDetector()
        detections = detector.detect(frame)
    """

    def __init__(self) -> None:
        """Load the model from the path defined in config.MODEL_PATH."""
        self._model = YOLO(config.MODEL_PATH)
        print(f"[Detector] Model loaded from: {config.MODEL_PATH}")
        print(f"[Detector] Running on device : {config.DEVICE}")

    def detect(self, frame: np.ndarray) -> list[Detection]:
        """
        Run YOLOv8 inference on a single BGR frame (as returned by cv2).

        Parameters
        ----------
        frame : np.ndarray
            A single video frame in BGR format (H, W, 3).

        Returns
        -------
        list[Detection]
            All detections whose confidence exceeds config.CONFIDENCE_THRESHOLD,
            filtered to only the four target vehicle classes.
        """
        results = self._model.predict(
            source=frame,
            conf=config.CONFIDENCE_THRESHOLD,
            iou=config.IOU_THRESHOLD,
            device=config.DEVICE,
            verbose=False,   # suppress per-frame console output
        )

        detections: list[Detection] = []

        # results is a list with one element per image; we pass one frame at a time.
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                class_id = int(box.cls[0])

                # Guard: only accept classes that are in our target list.
                if class_id >= len(config.CLASS_NAMES):
                    continue

                class_name = config.CLASS_NAMES[class_id]
                confidence = float(box.conf[0])

                # Bounding box in xyxy pixel format, cast to int.
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                bbox = (int(x1), int(y1), int(x2), int(y2))

                detections.append(
                    Detection(
                        bbox=bbox,
                        class_id=class_id,
                        class_name=class_name,
                        confidence=confidence,
                    )
                )

        return detections
