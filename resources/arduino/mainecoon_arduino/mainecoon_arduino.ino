/***
 * 
 * @file:     mainecoon_arduino
 * 
 * @brief:    Simple arduino firmware to read data 
 *            from serial input
 * 
 * @author:   Gabriel Conrado
 * 
 * @project:  MaineCoon
 */

#include <LiquidCrystal.h>

// Initialize the LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int BLUE_LED = 6;
const int YELLOW_LED = 7;

bool blue_led_state = false;
bool yellow_led_state = false;

void setup() {
  // Set the communication up
  Serial.begin(9600);
  // Signals the client that the arduino is ready do receive data
  lcd.begin(16, 2);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  Serial.println("Ready");
}

void loop() {
  // Read data only if there is data available
  if(Serial.available()){
    // Reads a full string from the buffer
    String input = Serial.readString();
    char command = input.charAt(0);
    switch(command){
    case '0':
      toggleLed(BLUE_LED, blue_led_state);
      break;
    case '1':
      toggleLed(YELLOW_LED, yellow_led_state);
      break;
    case '2':
      lcd.clear();
      lcd.print(input.substring(1));
      break;
    default:
      break;
    }
  Serial.println("Command done");
  }
}

void toggleLed(int led, bool state){
  switch(led){
    case BLUE_LED:
      if(blue_led_state)
        digitalWrite(BLUE_LED, LOW);
      else
        digitalWrite(BLUE_LED, HIGH);
      blue_led_state = !blue_led_state;
      break;
    case YELLOW_LED:
      if(yellow_led_state)
        digitalWrite(YELLOW_LED, LOW);
      else
        digitalWrite(YELLOW_LED, HIGH);
      yellow_led_state = !yellow_led_state;
      break;
    default:
      break;
  }
}

