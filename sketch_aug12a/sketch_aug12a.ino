#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4

#define CS_PIN 10
#define LED_PIN 7

MD_MAX72XX matrix = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

const uint8_t warningIcon[8] = {
  B00011000,
  B00111100,
  B01111110,
  B11011011,
  B11011011,
  B11111111,
  B00011000,
  B00011000
};

void showWarning() {
  matrix.clear();

  for (uint8_t row = 0; row < 8; row++) {
    for (uint8_t col = 0; col < 8; col++) {
      bool on = warningIcon[row] & (1 << (7 - col));

      if (on) {
        matrix.setPoint(row, col + 12, true);
      }
    }
  }

  matrix.update();
}

void allOff() {
  digitalWrite(LED_PIN, LOW);
  matrix.clear();
  matrix.update();
}

void vehicleDetected() {
  digitalWrite(LED_PIN, HIGH);
  matrix.clear();
  matrix.update();
}

void largeVehicleDetected() {
  digitalWrite(LED_PIN, HIGH);
  showWarning();
}

void processCommand(String command) {
  command.trim();
  command.toUpperCase();

  if (command == "OFF") {
    allOff();
    Serial.println("OK: OFF");
  }
  else if (command == "VEHICLE") {
    vehicleDetected();
    Serial.println("OK: VEHICLE");
  }
  else if (command == "LARGE") {
    largeVehicleDetected();
    Serial.println("OK: LARGE");
  }
  else {
    Serial.print("ERROR: UNKNOWN COMMAND: ");
    Serial.println(command);
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(9600);

  matrix.begin();
  matrix.control(MD_MAX72XX::INTENSITY, 5);
  matrix.clear();
  matrix.update();

  digitalWrite(LED_PIN, LOW);

  Serial.println("CurveGuard Arduino Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }
}