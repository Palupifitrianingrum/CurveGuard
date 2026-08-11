"""
config.py
---------
Single source of truth for all configurable parameters.

Every other module imports from here instead of using magic numbers or
hard-coded paths.  Adjust these values without touching any other file.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Path to the trained YOLOv8 model weights.
# After training on Kaggle, place best.pt inside the models/ directory.
MODEL_PATH: str = os.path.join("models", "best (1).pt")

# Default input video.  Can be overridden via command-line argument in main.py.
# Set to 0 to use a webcam instead of a file.
DEFAULT_VIDEO_PATH: str = os.path.join("videos", "video2.mkv")

# Optional: path for saving the processed video.
# Set to None to disable saving.
OUTPUT_VIDEO_PATH: str | None = os.path.join("videos", "output.mp4")

# ---------------------------------------------------------------------------
# Model / detection
# ---------------------------------------------------------------------------

# Class names must match the order used during training (data.yaml).
CLASS_NAMES: list[str] = ["bus", "car", "motorbike", "truck"]

# Minimum confidence score for a detection to be accepted.
CONFIDENCE_THRESHOLD: float = 0.40

# IoU threshold used by YOLOv8 NMS.
IOU_THRESHOLD: float = 0.45

# Run inference on this device.
# "cpu"  — always works; slower.
# "cuda" — requires an NVIDIA GPU.
# "mps"  — Apple Silicon Mac.
DEVICE: str = "cpu"

# ---------------------------------------------------------------------------
# Tracker  (Phase 2 — not used yet)
# ---------------------------------------------------------------------------

# Maximum number of frames a track is kept alive without a matching detection.
TRACK_MAX_AGE: int = 30

# Minimum number of consecutive detections required before a track is confirmed.
TRACK_MIN_HITS: int = 3

# Number of recent positions to keep in a vehicle's trajectory history.
TRAJECTORY_HISTORY_LENGTH: int = 30

# ---------------------------------------------------------------------------
# Danger zone  (Phase 3 — not used yet)
# ---------------------------------------------------------------------------

# Polygon vertices defining the dangerous curve section, expressed as
# normalised (x, y) coordinates in the range [0.0, 1.0].
# Using normalised values means the polygon adapts to any video resolution.
#
# Example below forms a rough quadrilateral; replace with your actual zone.
# Vertices are listed in order (clockwise or counter-clockwise).
DANGER_ZONE_POLYGON_NORM: list[tuple[float, float]] = [
    (0.30, 0.40),
    (0.70, 0.40),
    (0.70, 0.85),
    (0.30, 0.85),
]

# ---------------------------------------------------------------------------
# Risk analysis  (Phase 5 — not used yet)
# ---------------------------------------------------------------------------

# Pixel radius (on the original frame) within which a vehicle is considered
# "near" the danger zone even if it has not entered it yet.
NEAR_ZONE_PIXEL_MARGIN: int = 50

# Number of frames a vehicle must spend near/inside the zone before the
# risk level is escalated.
RISK_FRAME_COUNT_THRESHOLD: int = 10

# ---------------------------------------------------------------------------
# Warning  (Phase 6 — not used yet)
# ---------------------------------------------------------------------------

WARNING_TEXT: str = "⚠ DANGER: Vehicle approaching sharp curve!"
WARNING_COLOR_BGR: tuple[int, int, int] = (0, 0, 255)   # Red in BGR
