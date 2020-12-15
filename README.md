# <center>SP21 CS498 IoT Final Project Report</center>

## <center>Shiqi Yu</center>

- ### Motivation

  I live in an apartment whose window faces the garden, and there is a streetlight outside. Every night when I try to sleep, the streetlight keeps bothering me. Shuttering the shades does not help at all because the light goes through the chinks. To avoid having dark circles every day, I bought a tension rod and a curtain to block it. Here comes another issue. I always forget to close the curtain before going to the bed and I do not want to get up to close the curtain. Thus, I decide to make a remotely controlled curtain which can automatically close and open based on my instruction and outside lightning condition. When I am in bed at night, what I need to do is to simply click my phone for just one time. Then my light will go off, which is achieved by buying IoT Homekit devices on Amazon, and my curtain will close for me. In the morning, if it is sunny, the curtain will open so that I can see the bright sunshine which will makes me feel refreshed and relaxed. If it is rainy, for the love of god just do not wake me up please. I am excited about this project because this is the reason why I choose this course. I want to make life better, even a little bit, with what I have learned in school.

- ### Technical Approach

  This project includes three parts. The first part is motor & sensor module which is responsible for **physically opening and closing the curtain**. The second part is a **people detection** module that interference if there is anyone outside. The third part is center control unit which is in charge of **communication and logic**.

  ![](C:\Users\Hugo\Downloads\layout.png)

  <center>Figure 1. Project Layout</center>

  

  |                 Equipment List                  |
  | :---------------------------------------------: |
  |                 Raspberry Pi 4B                 |
  |                 Google Edge TPU                 |
  |                   Arduino Uno                   |
  |        TB6600 Stepper Motor Driver Board        |
  |              NEMA23 Stepper Motor               |
  | Raspberry Pi Camera Module V2-8 Megapixel,1080p |
  |              Joystick for Arduino               |
  |            HC-SR04 Ultrasonic Sensor            |
  |                   Tension Rod                   |
  |                  Curtain cloth                  |
  |                 3D printer gear                 |
  |                   Cotton wire                   |
  |                    Zip-ties                     |
  |                   Jump wires                    |

  #### 1. Motor & Sensor Module

  The motor I use is NEMA23 stepper motor. It is much more powerful than the regular stepper motors that come with the Arduino kit. Also I have a motor driver board TB6600 that works with the motor.

  <img src="C:\Users\Hugo\Desktop\final report\motor.png" style="zoom:27%;" />

  <center>Figure 2. NEMA23 </center>

  <img src="C:\Users\Hugo\Desktop\final report\driver.png" style="zoom: 50%;" />

  <center>Figure 3. TB6600 Driver Board</center>

  The motor is connected to the board and the board is connected to an Arduino Uno. The Arduino receives instruction from Raspberry Pi via serial port, translates it to digital signal, and then sends the signal to the driver board.

  <img src="C:\Users\Hugo\Desktop\final report\arduino.png" style="zoom:75%;" />

​                                                                                                                       

<center>Figure 4. Arduino</center>

There is a ultrasonic sensor that is connected to Arduino. It is responsible for measuring the distance between curtain cloth and the wall. If the distance is out of range, the curtain will stop moving. 

![](C:\Users\Hugo\Desktop\final report\ultrasonic.png)

<center>Figure 5. Ultrasonic Sensor</center>

#### 2. People Detection Module

Due to the limited computation power of Raspberry Pi, I decide to use a Google Edge TPU board which is specially designed for accelerating the computation of machine learning technique. The TPU receives the capture that is taken by camera on Raspberry Pi and sent via socket ,and then it inputs the image into the object detection model to see if there is anyone outside the window. Then it returns the result via socket connection to Raspberry Pi.

<img src="C:\Users\Hugo\Desktop\final report\TPU.png" style="zoom:80%;" />

<center>Figure 6. Google Edge TPU</center>

#### 3. Center Control Unit

The center control unit is a Raspberry Pi 4B. It is responsible for running a web server that works as interface, communicating with Edge TPU, and sending instruction to Arduino. There is a specially designed camera connected to it.

<img src="C:\Users\Hugo\Desktop\final report\Raspi.png" style="zoom: 50%;" />

<center>Figure 7. Raspberry Pi 4B</center>

<img src="C:\Users\Hugo\Desktop\final report\camera.png" style="zoom: 33%;" />

<center>Figure 8. Pi Camera</center>

- ### Implementation details

  #### 1. Motor & Motor Driver

  The motor is controlled by Arduino. The DIR pins take digital signal as input and they determine the rotation direction of stepper motor. The PUL pins determine step of the motor. A and B pins are the wires from coils of stepper motor. 

  <img src="C:\Users\Hugo\AppData\Roaming\Typora\typora-user-images\image-20201214192010009.png" alt="image-20201214192010009" style="zoom:67%;" />

<center>Figure 9. Motor Connection</center>

Below is a code snippet of functions that control the motor. Setup and define is available in the GitHub repo.

```java
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
```

Reference: https://www.makerguides.com/tb6600-stepper-motor-driver-arduino-tutorial/)

#### 2.Ultrasonic Sensor

Ultrasonic sensor uses the time interval between sending and receiving sound wave to measure the distance between the sensor and object. Below is a code snipper of the measure function. I add a counter here to make the result more stable because it sometimes return out-of-range values.

```java
float measure() {
  digitalWrite(Trig, LOW);
  delayMicroseconds(2);
  digitalWrite(Trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig, LOW);
  
  float temp = float(pulseIn(Echo, HIGH))；
  
  float cm = (temp * 17 )/1000;
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
```

At first, I used the measure function in every loop of while loop in open() and close(). However it turned out that the motor will stop working because the signal is not continuous enough with measuring in high frequency. Then I lowered the measuring frequency but the motor still did not work well. Then I use software interrupt supported by Arduino. As you can see, I set the measure() as interuppt handler and it runs every 1000ms. This does not influence the function of stepper motor.

```java
MsTimer2::set(1000, measure);
```

Reference: https://www.arduino.cc/reference/en/language/functions/interrupts/interrupts/

#### 3. Joystick

Officially this works as debug mode (The actual reason is that I think it is really fun to manually control like this).

```java
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
  //Serial.println("quit joystick mode");
  delay(1000);
}
```

#### 4. Edge TPU Object Detection

The object detection function is borrowed from the object detection example of Edge TPU. It uses a pretrained TFLite ssd_mobilenet_v2 model to interference. The setup process is way too complicated to explain here. More details of this are available on the GitHub repo.

Reference: https://coral.ai/examples/, https://coral.ai/docs/dev-board/get-started

#### 5. Socket Communication Between Raspberry Pi and Edge TPU

To simulate the scenario that I have a cloud platform for Machine Learning Computation, I connect TPU and Pi with socket. The socket server runs on TPU which waits for external connection. After setting up connection, it will receive and store the data sent from Pi for interference. Below is the code snippet running on Edge TPU.

```python
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('192.168.50.248', 12345))
        # s.bind(('localhost', 12346))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print ("Waiting...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    while 1:
        fileinfo_size = struct.calcsize('128sq')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.strip(str.encode('\00'))
            recvd_size = 0
            fp = open('pic.jpg', 'wb')
            print ("start receiving...")
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
        print('start interferencing')
        try:
            detected =  detect_image.detect_func()
        except OSError:
            detected = 0
        if detected:
            conn.send(b'1')
            result='Detected!'
        else: 
            conn.send(b'0')
            result='Not Detected!'
        print('result sent:'+result)

        conn.close()
        break
```

Below is the code snippet running on Raspberry Pi. It takes a picture using Pi camera and sent it to TPU. After that it waits until it receives result.

```python
def socket_client(camera):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = 'cap.jpeg'
        s.connect(('192.168.50.248',12345))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        camera.capture('cap.jpeg')
        sleep(2)
        # filepath = '/Users/yushiqi/Documents/GitHub/SmartCurtain/file'
        if os.path.isfile(filepath):
            fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size)
            s.send(fhead)
            print ('client filepath: {0}'.format(filepath))
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        print('send completed, wating for result')
        if s.recv(1024) == b'1':
            print('BB here!')
            people_detected = 1
        else:
            print('BB not here!')
            people_detected = 0
        s.close()
        break
    return people_detected
```

#### 6. Web Server

I use a Tornado, a light but powerful framework of web server, to build the web interface. I set several URLs and their corresponding handlers for main page, open, close, and request for picture. Due to limited power of Raspberry, I failed to stream the scene outside the window on the server. Instead, I set it to automatically refresh every 5 seconds. It is not perfect but it works. Below is code snippet of web server and handlers. In the handler, Pi sends instructions to Arduino.

```python
def web_server():
	settings = {"debug": True,}
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

```python
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        status = 'Choose your operation'
        self.render('index.html', status=status)

class CurtainOpenHandler(tornado.web.RequestHandler):
    def get(self):
        curtain_open()
        status = 'Curtain has been opened!'
        self.render('index.html', status=status)

class CurtainCloseHandler(tornado.web.RequestHandler):
    def get(self):
        curtain_close()
        status = 'Curtain is now closed!'
        self.render('index.html', status=status)

class ImageHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")
        
urls = [(r"/", IndexHandler),(r"/open", CurtainOpenHandler),(r"/close", CurtainCloseHandler),(r"/(cap.jpeg)", ImageHandler, {'path':'./'}),]
```

Here is a snapshot of the website.

![](C:\Users\Hugo\Desktop\final report\interface.png)

Reference: https://www.tornadoweb.org/en/stable/

#### 7. Communication Between Pi and Arduino

At first, I tired to use GPIO on Pi but it was broken somehow. The I decided to use serial communication instead. To be able to communicate with Arduino via serial port, I install minicom, a text-based serial port communications program. The content of communication is really simple. I just send corresponding character to Arduino to control. The port that Arduino uses on Pi is not fixed so I use try to get rid of setting the port manually every time they connect. Below is code snippet on Pi.

```python
try:
    ser = serial.Serial('/dev/ttyACM1', 9600,timeout=1)   #open named port at 9600,1s timeout
except:
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1)
    
def curtain_close():
    global ser
    ser.write(str.encode('a'))#writ a string to port
    return 0

def curtain_open():
    global ser
    ser.write(str.encode('b'))#writ a string to port
    return 0
```

Below is code snippet on Arduino. It checks the character that Pi sends and then calls function accordingly.

```java
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
```

Reference: https://help.ubuntu.com/community/Minicom

#### 8. Multiprocessing on Pi

Raspberry Pi is responsible for hosting the server and communicating with Edge TPU so I use multiprocessing to run them simultaneously. At first I used manager module in Python to share a object between processes. However there is bug in current version of it so I move the logic part to Arduino.

```python
def edge_tpu():
        camera = PiCamera()
        while 1:
            if socket_client(camera):
                curtain_close()
```

```python
if __name__ == '__main__':
    manager = Manager()
    # curtain_dict = manager.dict()
    # curtain_dict['open'] = 0
    # curtain_dict['busy'] = 0
    edge_tpu_process = Process(target=edge_tpu)
    server_process = Process(target=web_server)
    edge_tpu_process.start()
    server_process.start()
    edge_tpu_process.join()
    server_process.join()
```

#### 9. Mechanical Part

Unfortunately I do not have access to any 3D printer which helps me DIY the component. My first choice was the belt that people use on 3D printer. In my imagination it will work like the tank track that carries the curtain cloth. However the belt it self is not connected. It took me lot of effort to connect its ends because of its reinforced surface. The more unlucky thing is there is not enough tension to hold the belt. It kept conflicting with itself. 

<img src="C:\Users\Hugo\Desktop\final report\belt.png" style="zoom: 80%;" />

Fortunately I find the gears are compatible with my tension rod and I replace belt with cotton wire in the kitchen. To avoid entangling the strings, I add two plastic pieces. Besides, I tape to string to the gear to force them to go the right direction. Here is a snapshot of the final setup of mechanical part. It is more clear in the presentation video.

<img src="C:\Users\Hugo\OneDrive\IMG_4584.PNG" style="zoom:33%;" />

<img src="C:\Users\Hugo\OneDrive\IMG_4585.PNG" alt="IMG_4585" style="zoom:33%;" />

<img src="C:\Users\Hugo\OneDrive\IMG_4586.PNG" alt="IMG_4586" style="zoom:33%;" />

- ### Result

The project works well and is more robust than I expected. The response is swift and the interface is easy to use. The people detection is very precise and responds in short time period. I can control the curtain with just one click on my phone or computer and I do not need to worry about someone outside looking into my room anymore.

There are several drawback I want to mention too. Firstly, I think encapsulating the components is necessary because my cat climbed onto the table and destroyed my Raspberry Pi one day before the deadline. Secondly, the gears are not steadily fixed to the tension rod which may result in slipping. Thirdly,   the devices are too expensive. The Raspberry Pi, Edge TPU, Arduino are respectively 50$, 130$, 30$. I need cheaper computation source to lower the cost, like cloud platform.

The project does extend my skill sets. I learn about socket, multiprocessing, and filtering. Meanwhile I also gain more experience in web, Arduino programing, and Linux-like system usage.

This project is pretty new and the reason why I do this is I did not find similar product in the market. Building this project bring what I learned in the class into real life and indeed make my life better. I hope someday it will be fully developed and used by more people who need such curtain.



Video Link: https://www.youtube.com/watch?v=eYzChnQJ5sk&t=38s&ab_channel=喻世琦

GitHub Repo Link: https://github.com/HugoFishx/SmartCurtain