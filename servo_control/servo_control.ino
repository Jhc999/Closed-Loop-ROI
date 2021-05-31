#include <Servo.h>
#include <Wire.h>
Servo myservo;  // create servo object to control a servo
Servo myservo2;
byte Read = 0;
char* SET = malloc(7); //SET[7] = "999999Z"; 
char* SET1 = malloc(4);
char* SET2 = malloc(4);
int UD;
int LR;
int pos = 0;    // variable to store the servo position

void setup() {
   // put your setup code here, to run once:
   Serial.begin(19200);
   myservo.attach(9);  //SERVO
   myservo2.attach(10);  //SERVO
 }

void setservo1(int pos) { 
  myservo.write(pos);  //int from 0 to 180 
}

void setservo2(int pos){
  myservo2.write(pos);  //int from 0 to 180 
}

void loop() {
   // put your main code here, to run repeatedly:
   if (Serial.available() >= 7) {
     // Read the most recent byte
     Serial.readBytesUntil('Z', SET, 7);
     // ECHO the value that was read
     //Serial.write(SET);
     //Serial.print("\n");

     strncpy(SET1, SET, 3);
     strncpy(SET2, SET+3, 3);
     SET1[3] = '\0';
     SET2[3] = '\0';

     sscanf(SET1, "%d", &LR);
     sscanf(SET2, "%d", &UD);

     Serial.println(LR);
     Serial.println(UD);

     setservo1(LR);    
     setservo2(UD); 

   } 
 }
