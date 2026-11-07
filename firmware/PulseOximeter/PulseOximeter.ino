/*
  Wi-Fi pulse oximeter — educational prototype
  ESP8266 + MAX30100 + I2C OLED + Blynk

  Maintained by Sai Tanveesh.
  Reworked from the repository's earlier tutorial-based example.
  See docs/PROVENANCE.md before reuse or redistribution.

  Not a medical device. Not suitable for clinical decisions.
*/

// Copy secrets.example.h to secrets.h and supply your own values.
// The actual secrets.h must never be committed.
#include "secrets.h"

#include <Arduino.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <MAX30100_PulseOximeter.h>
#include <OakOLED.h>

namespace {
constexpr uint32_t kReportPeriodMs = 1000;
constexpr uint32_t kReconnectPeriodMs = 10000;
constexpr uint32_t kBlynkConnectTimeoutMs = 100;

PulseOximeter sensor;
OakOLED display;
uint32_t lastReportMs = 0;
uint32_t lastReconnectMs = 0;

bool validReading(float bpm, float spo2) {
  // Reject the sensor's uninitialized/empty readings, not medical conditions.
  return bpm > 0.0f && spo2 > 0.0f && spo2 <= 100.0f;
}

void showReadings(float bpm, float spo2, bool valid) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(1);
  display.setCursor(0, 0);
  display.println("Wi-Fi Pulse Oximeter");

  display.setCursor(0, 20);
  display.print("Pulse: ");
  if (valid) {
    display.print(bpm, 0);
    display.println(" BPM");
  } else {
    display.println("-- BPM");
  }

  display.setCursor(0, 38);
  display.print("SpO2: ");
  if (valid) {
    display.print(spo2, 0);
    display.println(" %");
  } else {
    display.println("-- %");
  }
  display.display();
}

void serviceCloud(uint32_t now) {
  if (WiFi.status() != WL_CONNECTED) {
    return;
  }

  if (Blynk.connected()) {
    Blynk.run();
    return;
  }

  if (now - lastReconnectMs >= kReconnectPeriodMs) {
    lastReconnectMs = now;
    // A short attempt lets local sampling continue without Blynk connectivity.
    Blynk.connect(kBlynkConnectTimeoutMs);
  }
}
}  // namespace

void setup() {
  Serial.begin(115200);

  // ESP8266 NodeMCU: D2 = SDA, D1 = SCL. Shared with the OLED.
  Wire.begin(D2, D1);
  display.begin();
  showReadings(0, 0, false);

  if (!sensor.begin()) {
    Serial.println("MAX30100 initialization failed; check I2C wiring.");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Sensor init failed");
    display.display();
    while (true) {
      delay(1000);
    }
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Blynk.config(BLYNK_AUTH_TOKEN);
  Serial.println("MAX30100 ready; local readings available without cloud.");
}

void loop() {
  // MAX30100 processing must run frequently; avoid blocking delays here.
  sensor.update();

  const uint32_t now = millis();
  serviceCloud(now);
  if (now - lastReportMs < kReportPeriodMs) {
    return;
  }
  lastReportMs = now;

  const float bpm = sensor.getHeartRate();
  const float spo2 = sensor.getSpO2();
  const bool valid = validReading(bpm, spo2);

  showReadings(bpm, spo2, valid);
  if (!valid) {
    Serial.println("Waiting for a stable sensor reading");
    return;
  }

  Serial.print("Pulse: ");
  Serial.print(bpm);
  Serial.print(" BPM | SpO2: ");
  Serial.print(spo2);
  Serial.println(" %");

  if (Blynk.connected()) {
    Blynk.virtualWrite(V7, bpm);
    Blynk.virtualWrite(V8, spo2);
  }
}
