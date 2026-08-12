import time
import serial


class ArduinoController:
    def __init__(self, port: str, baudrate: int = 9600) -> None:
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=1,
        )

        time.sleep(2)

        print(f"[Arduino] Connected to {port}")

    def send_command(self, command: str) -> None:
        command = command.strip().upper()

        self.serial.write((command + "\n").encode("utf-8"))

        print(f"[Arduino] Sent: {command}")

    def vehicle(self) -> None:
        self.send_command("VEHICLE")

    def large_vehicle(self) -> None:
        self.send_command("LARGE")

    def off(self) -> None:
        self.send_command("OFF")

    def close(self) -> None:
        if self.serial.is_open:
            self.off()
            self.serial.close()
            print("[Arduino] Disconnected")