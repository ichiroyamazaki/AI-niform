/*
 * Turnstile Control System for Arduino Uno
 * Features:
 * - Servo motor control for turnstile movement
 * - Serial command control ("Turnstile is Open")
 * - Automatic 5-second close timer
 * - LED status indicators
 * - Audio feedback
 * 
 * Hardware Connections:
 * - Servo Motor: Pin 9
 * - LED (Open): Pin 4
 * - LED (Closed): Pin 5
 * - Buzzer: Pin 3
 * 
 * Serial Commands:
 * - "Turnstile is Open" - Opens turnstile for 5 seconds
 * - "status" - Shows current status
 * - "help" - Shows available commands
 */

 #include <Servo.h>

 // Pin definitions
 const int SERVO_PIN = 9;
 const int LED_OPEN_PIN = 4;
 const int LED_CLOSED_PIN = 5;
 const int BUZZER_PIN = 8;
 const int BUTTON_OPEN_PIN = 2;
 const int BUTTON_CLOSE_PIN = 3;
 
 // Servo positions
 const int TURNSTILE_CLOSED_POS = 0;
 const int TURNSTILE_OPEN_POS = 90;
 
 // Timing constants
 const unsigned long TURNSTILE_MOVEMENT_TIME = 1000; // 1 second for turnstile to open/close
 const unsigned long AUTO_CLOSE_DELAY = 5000;        // 5 seconds before auto-close
 const unsigned long DEBOUNCE_DELAY = 50;            // Button debounce time
 
 // Global variables
 Servo turnstileServo;
 bool turnstileOpen = false;
 unsigned long lastMovementTime = 0;
 unsigned long autoCloseTime = 0;
 String inputString = "";
 bool stringComplete = false;
 
 // Button state variables
 bool buttonOpenPressed = false;
 bool buttonClosePressed = false;
 unsigned long lastButtonOpenPress = 0;
 unsigned long lastButtonClosePress = 0;
 
 void setup() {
   // Initialize serial communication
   Serial.begin(9600);
   Serial.println("Turnstile Control System Started");
   
   // Initialize servo
   turnstileServo.attach(SERVO_PIN);
   turnstileServo.write(TURNSTILE_CLOSED_POS);
   
   // Initialize pins
   pinMode(LED_OPEN_PIN, OUTPUT);
   pinMode(LED_CLOSED_PIN, OUTPUT);
   pinMode(BUZZER_PIN, OUTPUT);
   pinMode(BUTTON_OPEN_PIN, INPUT_PULLUP);
   pinMode(BUTTON_CLOSE_PIN, INPUT_PULLUP);
   
   // Initialize LEDs
   digitalWrite(LED_OPEN_PIN, LOW);
   digitalWrite(LED_CLOSED_PIN, HIGH);
   
   // Play startup sound
   playStartupSound();
   
   Serial.println("System initialized. Turnstile is closed.");
   Serial.println("Type 'open' to open for 5 seconds");
   Serial.println("Use OPEN button to open indefinitely");
   Serial.println("Use CLOSE button to close indefinitely");
   Serial.println("Type 'help' for available commands");
 }
 
 void loop() {
   // Check for serial input
   checkSerialInput();
   
   // Check for button presses
   checkButtons();
   
   // Process completed commands
   if (stringComplete) {
     processCommand();
     inputString = "";
     stringComplete = false;
   }
   
   // Update status LEDs
   updateStatusLEDs();
   
   // Handle auto-close timer (only for serial commands)
   handleAutoClose();
   
   // Small delay to prevent overwhelming the system
   delay(100);
 }
 
 void checkSerialInput() {
   while (Serial.available()) {
     char inChar = (char)Serial.read();
     
     if (inChar == '\n') {
       stringComplete = true;
     } else {
       inputString += inChar;
     }
   }
 }
 
 void checkButtons() {
   // Check OPEN button
   bool currentOpenButtonState = !digitalRead(BUTTON_OPEN_PIN); // Inverted because of pull-up
   
   if (currentOpenButtonState && !buttonOpenPressed && 
       (millis() - lastButtonOpenPress) > DEBOUNCE_DELAY) {
     buttonOpenPressed = true;
     lastButtonOpenPress = millis();
     
     Serial.println("OPEN button pressed - Opening turnstile indefinitely");
     openTurnstileIndefinitely();
   }
   
   if (!currentOpenButtonState) {
     buttonOpenPressed = false;
   }
   
   // Check CLOSE button
   bool currentCloseButtonState = !digitalRead(BUTTON_CLOSE_PIN); // Inverted because of pull-up
   
   if (currentCloseButtonState && !buttonClosePressed && 
       (millis() - lastButtonClosePress) > DEBOUNCE_DELAY) {
     buttonClosePressed = true;
     lastButtonClosePress = millis();
     
     Serial.println("CLOSE button pressed - Closing turnstile");
     closeTurnstileIndefinitely();
   }
   
   if (!currentCloseButtonState) {
     buttonClosePressed = false;
   }
 }
 
 void processCommand() {
   inputString.trim(); // Remove whitespace
   inputString.toLowerCase(); // Convert to lowercase for easier comparison
   
   if (inputString == "open") {
     openTurnstile();
   } else if (inputString == "status") {
     printStatus();
   } else if (inputString == "help") {
     printHelp();
   } else if (inputString == "close") {
     closeTurnstile();
   } else {
     Serial.println("Unknown command. Type 'help' for available commands.");
   }
 }
 
 void handleAutoClose() {
   if (turnstileOpen && autoCloseTime > 0 && 
       (millis() - autoCloseTime) > AUTO_CLOSE_DELAY) {
     Serial.println("Auto-closing turnstile...");
     closeTurnstile();
     autoCloseTime = 0;
   }
 }
 
 void openTurnstile() {
   if (!turnstileOpen) {
     Serial.println("Opening turnstile...");
     turnstileServo.write(TURNSTILE_OPEN_POS);
     turnstileOpen = true;
     lastMovementTime = millis();
     autoCloseTime = millis(); // Start auto-close timer
     
     // Play opening sound
     tone(BUZZER_PIN, 1000, 200);
     delay(300);
     tone(BUZZER_PIN, 1200, 200);
     
     Serial.println("Turnstile will close automatically in 5 seconds");
   } else {
     Serial.println("Turnstile is already open!");
   }
 }
 
 void closeTurnstile() {
   if (turnstileOpen) {
     Serial.println("Closing turnstile...");
     turnstileServo.write(TURNSTILE_CLOSED_POS);
     turnstileOpen = false;
     lastMovementTime = millis();
     autoCloseTime = 0; // Reset auto-close timer
     
     // Play closing sound
     tone(BUZZER_PIN, 800, 200);
     delay(300);
     tone(BUZZER_PIN, 600, 200);
   } else {
     Serial.println("Turnstile is already closed!");
   }
 }
 
 void openTurnstileIndefinitely() {
   if (!turnstileOpen) {
     Serial.println("Opening turnstile indefinitely...");
     turnstileServo.write(TURNSTILE_OPEN_POS);
     turnstileOpen = true;
     lastMovementTime = millis();
     autoCloseTime = 0; // Disable auto-close timer for button control
     
     // Play opening sound
     tone(BUZZER_PIN, 1000, 200);
     delay(300);
     tone(BUZZER_PIN, 1200, 200);
     
     Serial.println("Turnstile is now open indefinitely. Press CLOSE button to close.");
   } else {
     Serial.println("Turnstile is already open!");
   }
 }
 
 void closeTurnstileIndefinitely() {
   if (turnstileOpen) {
     Serial.println("Closing turnstile...");
     turnstileServo.write(TURNSTILE_CLOSED_POS);
     turnstileOpen = false;
     lastMovementTime = millis();
     autoCloseTime = 0; // Reset auto-close timer
     
     // Play closing sound
     tone(BUZZER_PIN, 800, 200);
     delay(300);
     tone(BUZZER_PIN, 600, 200);
     
     Serial.println("Turnstile is now closed.");
   } else {
     Serial.println("Turnstile is already closed!");
   }
 }
 
 void updateStatusLEDs() {
   if (turnstileOpen) {
     digitalWrite(LED_OPEN_PIN, HIGH);
     digitalWrite(LED_CLOSED_PIN, LOW);
   } else {
     digitalWrite(LED_OPEN_PIN, LOW);
     digitalWrite(LED_CLOSED_PIN, HIGH);
   }
 }
 
 void playStartupSound() {
   // Play startup sequence
   tone(BUZZER_PIN, 523, 200); // C5
   delay(250);
   tone(BUZZER_PIN, 659, 200); // E5
   delay(250);
   tone(BUZZER_PIN, 784, 300); // G5
   delay(350);
 }
 
 // Additional utility functions
 void printStatus() {
   Serial.println("=== Turnstile Status ===");
   Serial.print("Turnstile: ");
   Serial.println(turnstileOpen ? "OPEN" : "CLOSED");
   if (turnstileOpen && autoCloseTime > 0) {
     unsigned long timeRemaining = AUTO_CLOSE_DELAY - (millis() - autoCloseTime);
     Serial.print("Auto-close in: ");
     Serial.print(timeRemaining / 1000);
     Serial.println(" seconds");
   }
   Serial.println("========================");
 }
 
 void printHelp() {
   Serial.println("=== Available Commands ===");
   Serial.println("open - Opens turnstile for 5 seconds");
   Serial.println("close - Manually close turnstile");
   Serial.println("status - Show current status");
   Serial.println("help - Show this help message");
   Serial.println("");
   Serial.println("=== Physical Buttons ===");
   Serial.println("OPEN button (Pin 2) - Opens turnstile indefinitely");
   Serial.println("CLOSE button (Pin 3) - Closes turnstile");
   Serial.println("===========================");
 }