// joystick
int VRx = A0;
int SW = 2;
int xPosition = 0;
int SW_state = 0;
int mapX = 0;

void setup() {
  Serial.begin(9600); 
  //joystick
  pinMode(VRx, INPUT);
  pinMode(SW, INPUT_PULLUP); 
  
}

void loop() {
  Serial.println(get_joystick());
}

int get_joystick() {
  xPosition = analogRead(VRx);
  SW_state = digitalRead(SW);
  mapX = map(xPosition, 0, 1023, -512, 512);
  return mapX;
  }
