from __future__ import annotations

import argparse
import sys
import time

import cv2

import config
from detector import VehicleDetector
from visualizer import draw_detections, draw_fps
from arduino_controller import ArduinoController


ARDUINO_PORT = "COM3"
ARDUINO_BAUDRATE = 9600
LARGE_VEHICLES = {"bus", "truck"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CurveGuard — Vehicle Detection + Arduino Warning"
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
        help="Run without opening a display window.",
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


def _open_video(source: str) -> cv2.VideoCapture:
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

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        print(f"[WARNING] Could not create output writer at: {output_path}")
        print("          Output will not be saved.")
        return None

    print(f"[Main] Saving output to: {output_path}")
    return writer


def _get_vehicle_status(detections) -> str:
    if not detections:
        return "OFF"

    for detection in detections:
        if detection.class_name in LARGE_VEHICLES:
            return "LARGE"

    return "VEHICLE"


def run(args: argparse.Namespace) -> None:
    detector = VehicleDetector()
    arduino = None
    cap = None
    writer = None

    try:
        arduino = ArduinoController(
            port=ARDUINO_PORT,
            baudrate=ARDUINO_BAUDRATE,
        )

        cap = _open_video(args.video)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

        print(f"[Main] Source     : {args.video}")
        print(
            f"[Main] Resolution : {width}×{height} | "
            f"FPS: {src_fps:.1f} | Frames: {total_frames}"
        )
        print(f"[Main] Arduino    : {ARDUINO_PORT}")

        if args.save and config.OUTPUT_VIDEO_PATH:
            writer = _create_writer(
                cap,
                config.OUTPUT_VIDEO_PATH,
            )

        fps_display = 0.0
        frame_count = 0
        t_start = time.perf_counter()

        last_status = None

        print("[Main] Starting CurveGuard. Press 'q' to quit.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("[Main] End of video stream.")
                break

            frame_count += 1

            detections = detector.detect(frame)

            draw_detections(frame, detections)
            draw_fps(frame, fps_display)

            status = _get_vehicle_status(detections)

            if status != last_status:
                if status == "LARGE":
                    arduino.large_vehicle()

                elif status == "VEHICLE":
                    arduino.vehicle()

                else:
                    arduino.off()

                last_status = status

            if writer is not None:
                writer.write(frame)

            if not args.no_display:
                cv2.imshow(
                    "CurveGuard — Vehicle Detection",
                    frame,
                )

                key = cv2.waitKey(1) & 0xFF

                if key in (ord("q"), 27):
                    print("[Main] User requested exit.")
                    break

            elapsed = time.perf_counter() - t_start

            if elapsed >= 1.0:
                fps_display = frame_count / elapsed
                frame_count = 0
                t_start = time.perf_counter()

    except KeyboardInterrupt:
        print("\n[Main] Interrupted by user.")

    finally:
        if arduino is not None:
            arduino.off()
            arduino.close()

        if cap is not None:
            cap.release()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

        print("[Main] Done.")


if __name__ == "__main__":
    run(_parse_args())