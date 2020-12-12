#define dirPin 2
#define stepPin 3
#define DELAY 3*1000
// joystick
int VRx = A0;
int SW = 2;
int xPosition = 0;
int SW_state = 0;
int mapX = 0;

void setup() {
  Serial.begin(9600); 
  //joystick
  //pinMode(VRx, INPUT);
  //pinMode(SW, INPUT_PULLUP); 
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(4, INPUT_PULLUP);
  pinMode(7,OUTPUT);
  
  
  
}

void loop() {
  if ( Serial.available())
    {
      long recv = Serial.println(Serial.read());
      if('open' == recv)
        open();
      else if ('close' == recv)
        close();
     }
}

int get_joystick() {
  xPosition = analogRead(VRx);
  SW_state = digitalRead(SW);
  mapX = map(xPosition, 0, 1023, -512, 512);
  return mapX;
  }
  
void open() {
  long timestamp = millis();
  Serial.println(timestamp);
  digitalWrite(dirPin, LOW);
  while (millis() - timestamp < DELAY) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
}

void close() {
  long timestamp = millis();
  digitalWrite(dirPin, HIGH);
  while (millis() - timestamp < DELAY) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
}
