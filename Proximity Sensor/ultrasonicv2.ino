#define ECHO 6 // The echo pin
#define TRIG 7 // The trig pin
#define CALIBRATION 20 // Amount of times to pass for average calibration
#define THRESHOLD 10 // Threshold between activity and calibration value

int average;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  Serial.begin(9600); 
  average = calibration();
}

int calibration() {
  long duration;
  int distance;
  int sum = 0;
  int average;
  Serial.println("Calibrating initial distance");

  int i = 1;
  
  while (i < CALIBRATION + 1) {
    distance = calculateDistance();
    if (distance < 2000) { // Check if not bad read
      Serial.print("Pass: ");
      Serial.print(i);
      Serial.print("x | Distance: ");
      Serial.println(distance);
      sum = sum + distance;
      i++;
      delay(100);
    }
  }

  average = sum / CALIBRATION;
  return average;
  
}

int calculateDistance() {
  long duration;
  int distance;

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duration = pulseIn(ECHO, HIGH);

  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  return distance;
}

void loop() {
  int distance = calculateDistance();
  if (distance < average - THRESHOLD) { // Leeway for noise in reading, discards inaccurate reads
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" cm, ");
    Serial.print("Activity: ");
    Serial.println("1");
  } else if (distance < average + THRESHOLD) {
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" cm, ");
    Serial.print("Activity: ");
    Serial.println("0");
  }

  if (Serial.available()>0) {
    String value = Serial.readStringUntil('\n');
    if (value == "calibrate") {
      average = calibration();
    }
  }

  delay(1000);
}
