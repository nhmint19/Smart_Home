#include <IRremote.hpp>
#include <Dictionary.h>

const int IR_RECEIVE_PIN = 7;
const Dictionary *BUTTONS = new Dictionary(21);

// Read the signal and return the button value of the remote
void readSignal() {
  if (IrReceiver.decode()){
      String hexcode = String(IrReceiver.decodedIRData.decodedRawData, HEX); // decode the code to hex
      if (hexcode != "0") { // only return the correct code
          hexcode.toUpperCase(); // turn hexcode to uppercase
          Serial.println((BUTTONS->search(hexcode))); // print the button name to serial
      }
      IrReceiver.resume();
  }
}

void setup(){
  Serial.begin(9600);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
  // Dictionary of all remote code
  BUTTONS->insert("FF00BF00", "POWER");
  BUTTONS->insert("FE01BF00", "VOLUP");
  BUTTONS->insert("FD02BF00", "STOP");
  BUTTONS->insert("FB04BF00", "BACKWARD");
  BUTTONS->insert("FA05BF00", "PLAY");
  BUTTONS->insert("F906BF00", "FORWARD");
  BUTTONS->insert("F708BF00", "DOWN");
  BUTTONS->insert("F609BF00", "VOLDOWN");
  BUTTONS->insert("F50ABF00", "UP");
  BUTTONS->insert("F30CBF00", "0");
  BUTTONS->insert("F20DBF00", "EQ");
  BUTTONS->insert("F10EBF00", "REPT");
  BUTTONS->insert("EF10BF00", "1");
  BUTTONS->insert("EE11BF00", "2");
  BUTTONS->insert("ED12BF00", "3");
  BUTTONS->insert("EB14BF00", "4");
  BUTTONS->insert("EA15BF00", "5");
  BUTTONS->insert("E916BF00", "6");
  BUTTONS->insert("E718BF00", "7");
  BUTTONS->insert("E619BF00", "8");
  BUTTONS->insert("E51ABF00", "9");
}

void loop(){
  readSignal();
}
