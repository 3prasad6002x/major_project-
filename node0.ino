  #define BLYNK_PRINT Serial
 #include <ESP8266WiFi.h>
 #include <BlynkSimpleEsp8266.h>
 #include <SPI.h>
 #include <printf.h>
 #include <nRF24L01.h>
 #include <RF24.h>
 
 #define CE_PIN 2
 #define CSN_PIN 4
 #define INTERVAL_MESSAGE1 2100
 #define INTERVAL_MESSAGE2 3300
 #define INTERVAL_MESSAGE4 4000
 
const char* ssid = "HOME N/W";
const char* pass = "Saiprasad@333";
unsigned long time_1 = 0;  
unsigned long time_2 = 0;
unsigned long time_4 = 0;  

int x,soil_m1,soil_m2;
BlynkTimer timer;

const uint64_t receive_node_1 = 0xE8E8F0F0E1AA;
const uint64_t receive_node_2 = 0xE8E8F0F0E1EE;

char auth[] = "oBSuD77K9-4_5bEss0x1HBRcUZiHDpiX";

 
RF24 radio(CE_PIN, CSN_PIN);
float data1[3];
float data2;
float sensor_data[4];

 void sendSensor()
 {
  radio.openReadingPipe(0,receive_node_1);
  
  radio.startListening();
   if(radio.available()){
  //delay(2000);
  if(millis() > time_1 + INTERVAL_MESSAGE1){
        time_1 = millis();

    Serial.println("receiving data1...");
    
    radio.read( &data1, sizeof(data1) );
    sensor_data[0]=data1[0];
    sensor_data[1]=data1[1];
    sensor_data[2]=data1[2];
    //radio.stopListening();
   // delay(2000);
 }
  }
 radio.openReadingPipe(1,receive_node_2);
     radio.startListening();
     //delay(3300);
     
  if(radio.available()){
    
    if(millis() > time_2 + INTERVAL_MESSAGE2){
      Serial.println("receiving data2...");
       time_2 = millis();
       radio.read( &data2, sizeof(data2) );
       sensor_data[3]=data2;
   //Serial.println(sensor_data[0]);
     //  radio.stopListening();
      // delay(2000);
    }
 } 
  if(millis() > time_4 + INTERVAL_MESSAGE4){
        time_4 = millis();  
 Serial.println((String)sensor_data[0]+(String)sensor_data[1]+(String)sensor_data[2]+(String)sensor_data[3]);
 x=(sensor_data[0]<100.00 && sensor_data[1] <50.00);
 soil_m1=(sensor_data[2]>100.00 && sensor_data[2]<1054.00);
 soil_m2=(sensor_data[3]>100.00 && sensor_data[3]<1054.00);
 Serial.println(x);
 Serial.println(soil_m1);
 Serial.println(soil_m2);
 if(x && soil_m1 &&soil_m2){
 Blynk.virtualWrite(V2, sensor_data[0]);
  Blynk.virtualWrite(V3, sensor_data[1]);
  Blynk.virtualWrite(V4, sensor_data[2]);
  Blynk.virtualWrite(V5, sensor_data[3]);
  Serial.println("Success No redundancy data sent");
  //delay(10000);
 }
 else{
  Serial.println("Redundancy data");
  }
 }
 }
void setup()
 {
 Serial.begin(1000000);
 Blynk.begin(auth, ssid, pass, IPAddress(192,168,0,165), 8080);
 Serial.println("Serial begin...");
 radio.begin();
 Serial.print("rf begin...");
 delay(4000);
 printf_begin();
 radio.setDataRate(RF24_1MBPS);
 radio.printPrettyDetails();
 bool chip=radio.isChipConnected();
  if(chip) Serial.println("chip connected  to SPI BUS...");
  delay(4000);
 bool Valid=radio.isValid();
if (Valid) Serial.println("real radio..." );
 delay(10000);
Serial.println("Hum  Tempera  SOILM1  SOILM2");
timer.setInterval(1000L, sendSensor);
 }
 
void loop()
 {

  Blynk.run();
timer.run();
  
   
  
 }
 
  
  
