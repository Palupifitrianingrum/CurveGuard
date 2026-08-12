from arduino_controller import ArduinoController

arduino = ArduinoController("COM3")

arduino.vehicle()
input("Tekan Enter untuk LARGE...")
arduino.large_vehicle()

input("Tekan Enter untuk OFF...")
arduino.off()

arduino.close()