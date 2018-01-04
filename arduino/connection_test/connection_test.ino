/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int ledL = 10;
int ledR = 11;
int valL = 0;
int valR = 0;
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(ledL, OUTPUT);
  pinMode(ledR, OUTPUT);
  
  Serial.begin(9600);
  inputString.reserve(200);
  
  analogWrite(ledL, 0);
  analogWrite(ledR, 0);
}

// the loop routine runs over and over again forever:
void loop() {
  
    // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println("ACK:"+inputString); 
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  delay(10);               // wait for a second
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
  
  char header = *inputString.c_str();
  switch (header) {
    case 'a':
      valR = atoi(inputString.substring(1,5).c_str());
      analogWrite(ledR, valR);
      valL = atoi(inputString.substring(5,9).c_str());
      analogWrite(ledL, valL);
      break;
    default:
      break;
  }
}

