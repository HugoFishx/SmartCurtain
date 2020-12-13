#include <MsTimer2.h>
#define dirPin 2
#define stepPin 3
#define DELAY 16*1000
#define Trig 4
#define Echo 5
// joystick
int VRx = A0;
int SW = 7;
int xPosition = 0;
int SW_state = 0;
int mapX = 0;
volatile int state = 0;
volatile int closed = 0;
volatile int counter = 6;

void setup() {
  Serial.begin(9600); 
  //joystick
  pinMode(VRx, INPUT);
  pinMode(SW, INPUT_PULLUP);
  //stepper
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  //supersonic
  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT); 
  //interrupt
  MsTimer2::set(1000, measure);
}

void loop() {
  if ( Serial.available())
    {
      //Serial.println("accepting");
      char read[1];
      Serial.readBytes(read, 1);
      //Serial.println(read);
      if('b' == read[0] && closed)
        open();
      if('a' == read[0] && !closed)
        close();
     }
   get_joystick();
   if (SW_state == 0)
    joy_stick_mode();
}

int get_joystick() {
  xPosition = analogRead(VRx);
  SW_state = digitalRead(SW);
  mapX = map(xPosition, 0, 1023, -512, 512);
  return mapX;
  }

void joy_stick_mode() {
  //Serial.println("enter joystick mode");
  delay(1000);
  get_joystick();
  while (SW_state == 1) {
    int dir = get_joystick();
    //Serial.println(measure());
    if (dir > 30) {
      digitalWrite(dirPin, LOW);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
    }
    else if (dir < 0) {
      digitalWrite(dirPin, HIGH);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
    }
  }
  Serial.println("quit joystick mode");
  delay(1000);
}

void open() {
  long time = millis();
  //Serial.println("open");
  digitalWrite(dirPin, LOW);
  while(millis() - time < DELAY) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
  closed = 0;
}


void close() {
  long time = millis();
  //Serial.println("open");
  digitalWrite(dirPin, HIGH);
  while(millis() - time < DELAY) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
  closed = 1;
}

void open_sonic() {
  counter = 6;
  MsTimer2::start();
  //Serial.println("open");
  digitalWrite(dirPin, LOW);
  state = 1;
  while(state) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
  MsTimer2::stop();
}

void close_sonic() {
  counter = 6;
  MsTimer2::start();
  //Serial.println("close");
  digitalWrite(dirPin, HIGH);
  state = 1;
  while (state) {
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
  }
  MsTimer2::stop();
}

float measure() {
  digitalWrite(Trig, LOW); //给Trig发送一个低电平
  delayMicroseconds(2);    //等待 2微妙
  digitalWrite(Trig,HIGH); //给Trig发送一个高电平
  delayMicroseconds(10);    //等待 10微妙
  digitalWrite(Trig, LOW); //给Trig发送一个低电平
  
  float temp = float(pulseIn(Echo, HIGH)); //存储回波等待时间,
  //pulseIn函数会等待引脚变为HIGH,开始计算时间,再等待变为LOW并停止计时
  //返回脉冲的长度
  
  //声速是:340m/1s 换算成 34000cm / 1000000μs => 34 / 1000
  //因为发送到接收,实际是相同距离走了2回,所以要除以2
  //距离(厘米)  =  (回波时间 * (34 / 1000)) / 2
  //简化后的计算公式为 (回波时间 * 17)/ 1000
  
  float cm = (temp * 17 )/1000; //把回波时间换算成cm
  //Serial.println(cm);
  if (cm < 50 & cm > 22) {
    state = 1;
  }
   else {
    counter = counter - 1;
      if (counter == 0)
        state = 0;
   }
}
