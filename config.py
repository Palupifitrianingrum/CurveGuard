import os

MODEL_PATH: str = os.path.join("models", "best (1).pt")

DEFAULT_VIDEO_PATH: str = os.path.join("videos", "video2.mkv")

OUTPUT_VIDEO_PATH: str | None = os.path.join("videos", "output.mp4")

CLASS_NAMES: list[str] = ["bus", "car", "motorbike", "truck"]

CONFIDENCE_THRESHOLD: float = 0.40

IOU_THRESHOLD: float = 0.45

DEVICE: str = "cpu"

TRACK_MAX_AGE: int = 30

TRACK_MIN_HITS: int = 3

TRAJECTORY_HISTORY_LENGTH: int = 30

DANGER_ZONE_POLYGON_NORM: list[tuple[float, float]] = [
    (0.30, 0.40),
    (0.70, 0.40),
    (0.70, 0.85),
    (0.30, 0.85),
]

NEAR_ZONE_PIXEL_MARGIN: int = 50

RISK_FRAME_COUNT_THRESHOLD: int = 10

WARNING_TEXT: str = "⚠ DANGER: Vehicle approaching sharp curve!"
WARNING_COLOR_BGR: tuple[int, int, int] = (0, 0, 255)   
