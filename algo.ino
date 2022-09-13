//#include <b64.h>
#include <HttpClient.h>

/////////////////////////////////
// Generated with a lot of love//
// with TUNIOT FOR ESP8266     //
// Website: Easycoding.tn      //
/////////////////////////////////
#include <ESP8266WiFi.h>

#include <ESP8266HTTPClient.h>
#include <Servo_ESP8266.h>
#include <DMotor_mod.h>
#include <InterpolationLib.h>

#define ledPin D2             // for the low battery warning
//#define voltagePin D6 D0        // for the battery voltage detection
#define servoPin D9           // for the use of a servo motor
#define sensorPin A0          // for the use of a analog sensor

// The motors are created with the use of the libraries:
AF_Stepper motorR(256, 1);    // Right motor  (stepper)
AF_Stepper motorL(256, 2);    // Left  motor  (stepper)
Servo_ESP8266 sensorServo;    // Sensor motor (servo)

int n_orders=100;//Maximum number of oreders that the LLUBot may execute 
char orders[100];//Orders executed
int distances[100];//Distances moved in each order
int next_order=0;//the next order and distance to fill

// Physical data of the LLUBot:
float wheelRadius = 3.2;      // in cm, check this distance with the physical LLUBot
float wheelsAxisDis = 16.0;   // in cm, check this distance with the physical LLUBot
int stepperResolution = 256;  // 8 bits
int stepToMicrostep = 8;      // 8 microsteps are 1 step within the stepper structure 
float twoPi = 2 * 3.1416;     // geometry use of 2 * pi in the perimeter of a circle
int chosenSpeed = 100;        // in percentage
float chosenLenght = 19.5;    // for activity 3
float chosenAngle = 90;       // for activity 3
float servoAngle = 90.0;      // initial position
String ultMensaje = "";
// We initialize the battery voltage reading:
int sensorVal = 1;            // for initial state of charged

// Initialize the LLUBot's movement variables according to selected activity:
int valueA1 = 0;              // initialization value for Roomba in activity 1
int valueA2 = 0;              // initialization value for activity 2
float calculatedSteps = 0;    // steps for activity 3
char chosenDirection = 0;     // direction for activities 2 and 3

// Interpolation for the IR sensor
const int tableEntries = 10;  // number of entries for the interpolation table
const int mVinterval  = 100;  // value of the intervals in milivolts
static float sensorDistance[tableEntries] = {80.0,70.0,60.0,50.0,40.0,30.0,25.0,20.0,15.0,10.0};

const int numValues = 8;
double xValues[8] = { 400,  600,  750,  900, 1100, 1300, 1650, 2300};
double yValues[8] = {80.0, 50.0, 40.0, 30.0, 25.0, 20.0, 15.0, 10.0};
String mensajeGlobal = "0011000111001110";
float nopeAngles[42] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

const String Ip = "192.168.1.46:8080";
IPAddress staticIP773_10(192,168,1,11);
IPAddress gateway773_10(192,168,1,1);
IPAddress subnet773_10(255,255,255,0);

String  httpurl = "http://192.168.1.46:8080/";
String  TheHiddenAnswerOfClient;
HTTPClient http;
WiFiClient client;
float algo;
float otro = 0.0;
void setup()
{

  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
   WiFi.begin("MOVISTAR_7EF0","apbhKSiWXaiBoLSa7mFx");
  while ((!(WiFi.status() == WL_CONNECTED))){
    delay(300);
    Serial.print("..");

  }
  Serial.begin(9600); 
enviarMensaje();
 
}
void enviarMensaje() {
  while (true) {
   
    String orden = WaitForAnswer(httpurl + mensajeGlobal);
  Serial.print("Recibido: ");
    //if (orden == "" || orden == "00110001"){     
   for(int i=0; i<orden.length(); i++) {
      Serial.print(orden.charAt(i));
    }
    ultMensaje = mensajeGlobal;
    mensajeGlobal = "0011000111001110";
      realizaFuncion(orden);
    
              delay(9000);

  }
}

void esperarOrden() {
  String Orden = "";
  while (Orden == "1" || Orden == ""){
    Orden = traducirOrdenRec(WaitForAnswer(httpurl));
        delay(1000);

    realizaFuncion(Orden);
        delay(1000);

  }
}
void loop()
 {
 

}
