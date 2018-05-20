/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int pinLF = 5;
int pinLB = 6;
int pinRF = 10;
int pinRB = 11;
int valL = 0;
int valR = 0;
int valL_old = 0;
int valR_old = 0;
char cbuf[4] = "";
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(pinLF, OUTPUT);
  pinMode(pinRF, OUTPUT);
  pinMode(pinLB, OUTPUT);
  pinMode(pinRB, OUTPUT);
  
  Serial.begin(9600);
  inputString.reserve(200);
  
  analogWrite(pinLF, 0);
  analogWrite(pinRF, 0);
  analogWrite(pinLB, 0);
  analogWrite(pinRB, 0);
}

// the loop routine runs over and over again forever:
void loop() {

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
  
    // print the string when a newline arrives:
  if (stringComplete) {
    
    Serial.print("ACK:");

    char header = *inputString.c_str();
    switch (header) {
      case 'a':
        valL = atoi(inputString.substring(1,5).c_str());
        valR = atoi(inputString.substring(5,9).c_str());
        if ( valL > 0 ^ valL_old > 0 ) {
          // Stop Mode for 100us
          analogWrite(pinLF, 0);
          analogWrite(pinLB, 0);
          delayMicroseconds(100);
          Serial.print("L>stop");
        } else {
          Serial.print("L>    ");
        }
        if ( valR > 0 ^ valR_old > 0 ) {
          // Stop Mode for 100us
          analogWrite(pinRF, 0);
          analogWrite(pinRB, 0);
          delayMicroseconds(100);
          Serial.print(" R>stop");
        } else {
          Serial.print(" R>    ");
        }
        if ( valL > 0 ) {
          analogWrite(pinLF, +valL);
          analogWrite(pinLB, 0);
          Serial.print(" LF>");
        } else {
          analogWrite(pinLF, 0);
          analogWrite(pinLB, -valL);
          Serial.print(" LB>");
        }
        sprintf(cbuf, "%4d", valL);
        Serial.print(cbuf);
        if ( valR > 0 ) {
          analogWrite(pinRF, +valR);
          analogWrite(pinRB, 0);
          Serial.print(" RF>");
        } else {
          analogWrite(pinRF, 0);
          analogWrite(pinRB, -valR);
          Serial.print(" RB>");
        }
        sprintf(cbuf, "%4d", valR);
        Serial.print(cbuf);
        valL_old = valL;
        valR_old = valR;
        break;
      case 'c':
        // Stop Mode
        analogWrite(pinLF, 0);
        analogWrite(pinLB, 0);
        analogWrite(pinRF, 0);
        analogWrite(pinRB, 0);
        break;
      default:
        break;
    }
    
    Serial.println(" >end");
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  
  delay(10);               // wait for a second
}
