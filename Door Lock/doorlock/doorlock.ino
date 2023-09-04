#include <Servo.h>

// Pin settings
const int led_locked = 3;
const int led_unlocked = 4;
const int servo_pin = 5;

// Servo settings
const int lock_pos = 20;
const int unlock_pos = 135;

Servo servo;

bool locked = false;

void setup() {
  // Initialise Serial library and configure pins.
  Serial.begin(115200);
  
  servo.attach(5);

  pinMode(led_locked, OUTPUT);
  pinMode(led_unlocked, OUTPUT);
}

void loop() {
  // Check for new Serial messages.
  while (Serial.available() > 0) {
    // Read one line (messages are one line each)
    String message = Serial.readStringUntil('\n');

    // Handle each message type.
    if (message.startsWith("set")) {
      locked = message.endsWith("1");
    } else if (message == "state") {
      Serial.println(locked ? "Locked" : "Unlocked");
    }
  }

  // Update actuators.
  if (locked) {
    digitalWrite(led_locked, HIGH);
    digitalWrite(led_unlocked, LOW);
    servo.write(lock_pos);
  } else {
    digitalWrite(led_locked, LOW);
    digitalWrite(led_unlocked, HIGH);
    servo.write(unlock_pos);
  }

  // Delay, to reduce CPU time.
  delay(100);
}
