# CurveGuard by Modal Bismillah 

> Smart City Road Safety System for Extreme Curves

CurveGuard is a Smart City project developed to improve road safety on extreme and potentially dangerous curves.

The system uses computer vision and YOLOv8 to detect vehicles from video footage. The detected vehicle information will later be used as part of a larger road-risk analysis and warning system.

## Current Development

### Phase 1 — Vehicle Detection

Current pipeline:

VIDEO → OpenCV → YOLOv8 → Vehicle Detection → Visualization

The current model detects four vehicle classes:

- Bus
- Car
- Motorbike
- Truck

The system can:

- Read video input using OpenCV
- Detect vehicles using YOLOv8
- Display bounding boxes
- Display vehicle class
- Display detection confidence
- Display processing FPS
- Save the processed video

## Project Structure

```text
curveguard/
├── main.py
├── config.py
├── detector.py
├── visualizer.py
├── tracker.py
├── danger_zone.py
├── risk_analyzer.py
├── warning.py
├── requirements.txt
├── models/
│   └── best.pt
└── videos/1`
    └── input.mkv
```
## Requirements

- Python 3.10+
- OpenCV
- Ultralytics
- PyTorch
- YOLOv8-compatible model

Install the dependencies:

```bash
pip install -r requirements.txt
```

Teammates :

Rakan Hendian Ramadhan

Rida Larasati

Palupi Fitria Ningrum

