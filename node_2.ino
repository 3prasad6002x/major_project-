#include <SPI.h>
 #include <printf.h>
 #include <nRF24L01.h>
 #include <RF24.h>
 #define CE_PIN 9
 #define CSN_PIN 8
 //#define INTERVAL_MESSAGE3 4000
 #define INTERVAL_MESSAGE1 3300


 
unsigned long time_1 = 0;
//unsigned long time_3 = 0; 
const uint64_t send_node_2 = 0xE8E8F0F0E1EE;
//const uint64_t receive_node_3 = 0xE8E8F0F0E1LL;
 
RF24 radio(CE_PIN, CSN_PIN);
float data;
//float data1[2];
 
void setup()
 {
 Serial.begin(1000000);
 radio.begin();
 printf_begin();
  
 radio.printPrettyDetails();
 bool chip=radio.isChipConnected();
 Serial.println(chip);
 bool valid=radio.isValid();
 Serial.println(valid);
 
}
 
void loop()
 {
  //data1[1]=data3();
  data=analogRead(A5);
  radio.stopListening();
 radio.openWritingPipe(send_node_2);
  if(millis() > time_1 + INTERVAL_MESSAGE1){
        time_1 = millis();
        
    bool ok=radio.write(&data,sizeof(data));
    Serial.println(ok);
    Serial.println(data);
    
  }
 }
/* float data3()
 {
   if(millis() > time_3 + INTERVAL_MESSAGE3){
        time_3 = millis();
        Serial.println("time_3");
  radio.openReadingPipe(0,receive_node_3);
  radio.startListening();
  if(radio.available()){
    Serial.print(".");
     
    radio.read(&data,sizeof(data));
    Serial.print(data);
  return data;
     }
  }
 }
 */


  
   
