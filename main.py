"""
main.py
-------
Pipeline orchestrator — Phase 1.

Phase 1 pipeline:
    VIDEO → OpenCV → YOLOv8 detection → Visualization

Usage
-----
    # Use the default video path from config.py:
    python main.py

    # Pass a custom video file:
    python main.py --video path/to/video.mp4

    # Use webcam (device index 0):
    python main.py --video 0

    # Disable the output window (headless mode, e.g. on a server):
    python main.py --no-display

    # Save processed video to a file:
    python main.py --save
"""

from __future__ import annotations

import argparse
import sys
import time

import cv2

import config
from detector import VehicleDetector
from visualizer import draw_detections, draw_fps


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smart City Road Safety — Phase 1: Detection + Visualization"
    )
    parser.add_argument(
        "--video",
        type=str,
        default=config.DEFAULT_VIDEO_PATH,
        help=(
            "Path to the input video file, or an integer device index for webcam. "
            f"Default: {config.DEFAULT_VIDEO_PATH}"
        ),
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Run without opening a display window (useful on headless machines).",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help=(
            "Save the annotated video to the path defined in "
            "config.OUTPUT_VIDEO_PATH."
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Video I/O helpers
# ---------------------------------------------------------------------------

def _open_video(source: str) -> cv2.VideoCapture:
    """
    Open a VideoCapture from a file path or webcam index.
    Exits with a clear error message if the source cannot be opened.
    """
    # Allow passing '0', '1', etc. as strings to mean webcam index.
    try:
        index = int(source)
        cap = cv2.VideoCapture(index)
        label = f"webcam {index}"
    except ValueError:
        cap = cv2.VideoCapture(source)
        label = source

    if not cap.isOpened():
        print(f"[ERROR] Could not open video source: {label}")
        print("        Make sure the file exists or the webcam is connected.")
        sys.exit(1)

    return cap


def _create_writer(
    cap: cv2.VideoCapture,
    output_path: str,
) -> cv2.VideoWriter:
    """Create a VideoWriter that matches the source video's resolution and FPS."""
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not writer.isOpened():
        print(f"[WARNING] Could not create output writer at: {output_path}")
        print("          Output will not be saved.")
        return None

    print(f"[Main] Saving output to: {output_path}")
    return writer


# ---------------------------------------------------------------------------
# Main pipeline loop
# ---------------------------------------------------------------------------

def run(args: argparse.Namespace) -> None:
    # --- Initialise detector (loads the model once) ---
    detector = VehicleDetector()

    # --- Open video source ---
    cap = _open_video(args.video)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    src_fps      = cap.get(cv2.CAP_PROP_FPS) or 30.0

    print(f"[Main] Source : {args.video}")
    print(f"[Main] Resolution : {width}×{height}  |  FPS: {src_fps:.1f}  |  Frames: {total_frames}")

    # --- Optional output writer ---
    writer: cv2.VideoWriter | None = None
    if args.save and config.OUTPUT_VIDEO_PATH:
        writer = _create_writer(cap, config.OUTPUT_VIDEO_PATH)

    # --- FPS measurement ---
    fps_display  = 0.0
    frame_count  = 0
    t_start      = time.perf_counter()

    print("[Main] Starting Phase 1 pipeline.  Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Main] End of video stream.")
            break

        frame_count += 1

        # ----------------------------------------------------------------
        # STAGE 1 — YOLOv8 vehicle detection
        # ----------------------------------------------------------------
        detections = detector.detect(frame)

        # ----------------------------------------------------------------
        # STAGE 2 — Visualization
        # (Phase 2+ stages are not active yet — stubs are imported but
        #  not called, so there is zero overhead)
        # ----------------------------------------------------------------
        draw_detections(frame, detections)
        draw_fps(frame, fps_display)

        # ----------------------------------------------------------------
        # Output
        # ----------------------------------------------------------------
        if writer is not None:
            writer.write(frame)

        if not args.no_display:
            cv2.imshow("Smart City Road Safety — Phase 1", frame)
            # Press 'q' or Esc to quit early
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                print("[Main] User requested exit.")
                break

        # Update FPS every second
        elapsed = time.perf_counter() - t_start
        if elapsed >= 1.0:
            fps_display = frame_count / elapsed
            frame_count = 0
            t_start     = time.perf_counter()

    # --- Cleanup ---
    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

    print("[Main] Done.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run(_parse_args())
