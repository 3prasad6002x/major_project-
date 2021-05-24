#include <SPI.h>
 #include <printf.h>
 #include <nRF24L01.h>
 #include <RF24.h>
 #define CE_PIN 9
 #define CSN_PIN 8
 #define INTERVAL_MESSAGE1 2000
 #include <dht.h>
#define dht_apin A0

dht DHT;
 
 
unsigned long time_1 = 0;  
const uint64_t receive_node_1 = 0xE8E8F0F0E1AA;
 
RF24 radio(CE_PIN, CSN_PIN);
float data1[3];
 
void setup()
 {
 Serial.begin(1000000);
 radio.begin();
 printf_begin();
 radio.openWritingPipe(receive_node_1);
 radio.printPrettyDetails();
 radio.setDataRate(RF24_1MBPS);
 bool chip=radio.isChipConnected();
 Serial.println(chip);
 bool Valid=radio.isValid();
 Serial.println(Valid);
 }
 
void loop()
 {

  if(millis() > time_1 + INTERVAL_MESSAGE1){
        time_1 = millis();
         DHT.read11(dht_apin);
        data1[0]=DHT.humidity;
        data1[1]=DHT.temperature;
        data1[2]=analogRead(A5);
        bool ok=radio.write(&data1,sizeof(data1));
        if (ok) Serial.println("Success");
        Serial.println(data1[0]);
        Serial.println(data1[1]);
        Serial.println(data1[2]);
        
     } 
  }
  
