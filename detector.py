from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from ultralytics import YOLO
import config

@dataclass
class Detection:
    bbox: tuple[int, int, int, int]
    class_id: int
    class_name: str
    confidence: float

    @property
    def center(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, y2)

    @property
    def top_center(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, y1)


class VehicleDetector:
    def __init__(self) -> None:
        self._model = YOLO(config.MODEL_PATH)
        print(f"[Detector] Model loaded from: {config.MODEL_PATH}")
        print(f"[Detector] Running on device : {config.DEVICE}")

    def detect(self, frame: np.ndarray) -> list[Detection]:
        results = self._model.predict(
            source=frame,
            conf=config.CONFIDENCE_THRESHOLD,
            iou=config.IOU_THRESHOLD,
            device=config.DEVICE,
            verbose=False,  
        )

        detections: list[Detection] = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                class_id = int(box.cls[0])

                if class_id >= len(config.CLASS_NAMES):
                    continue

                class_name = config.CLASS_NAMES[class_id]
                confidence = float(box.conf[0])

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
