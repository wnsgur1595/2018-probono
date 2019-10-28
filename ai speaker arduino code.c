//아두이노 C언어 코드

#include<Adafruit_Sensor.h>
#include <DHT.h>
//#include <DHT_U.h>
//#include "DHT.h"
#include <SoftwareSerial.h>
#define bluetoothTx 3
#define bluetoothRx 2
#define DHTPIN 4
#define MOTIONPIN_1 5
#define GASPIN 12
#define MOTIONPIN_2 6
//#define MOTIONPIN_3 7
#define PANPIN 7
#define DHTTYPE DHT22
DHT dht(DHTPIN,DHTTYPE);
SoftwareSerial bluetooth(bluetoothTx,bluetoothRx);
float humidity;
float temperature;
float gasValue;
float gasVolts;
int motion_1;
bool motion_2;                  
bool motion_3;
bool pan;
char frompi;
char topi;
int test;     //라즈베리파이가 환풍기 직접 켜달라고 요청했을때 조건에 안맞아도 강제로 키고끄려고

void setup()
{
  pinMode(MOTIONPIN_1,INPUT);        //모션센스 하나만
                                                          //pinMode(MOTIONPIN_2,INPUT);
                                                          //pinMode(MOTIONPIN_3,INPUT);
  pinMode(PANPIN,OUTPUT);            //환풍기 작동
  Serial.begin(9600);
  pinMode(GASPIN,OUTPUT); 
  pinMode(MOTIONPIN_2,OUTPUT); 
  bluetooth.begin(9600);
  dht.begin();
  pan = false;
  motion_1 = 0;
  test=1;
  frompi=0;
}
void loop()
  {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  if(bluetooth.available()){
    frompi=(char)bluetooth.read();
     Serial.print(frompi);
    }
 
  if(humidity > 70 && pan ==false)// &&test==1)          //습도가 50이상이고 팬이 꺼져있으면 자동으로 환풍기를 온시키고 라즈베리 파이에게 환풍기가 켜졌음을 알려줌.
  {
    //환풍기 on
    pan = true;
    digitalWrite(PANPIN,HIGH);
    topi = 'O'; //panon일때 보내주는거
    bluetooth.write(topi);  //라즈베리에 알림
    delay(2000);
   // test==0;
  }
  
  if(humidity<=40 && pan ==true)// &&test==0)             //50->40으로 수정          습도가 40이하이고 팬이 켜져있으면 자동으로 환풍기를 끄고 라즈베리파이에 환풍기를 껏음을 알려줌
  {
    //환풍기 off
    pan = false;
    digitalWrite(PANPIN,LOW);
    //라즈베리에 알림
    topi = 'F';//panoff
    bluetooth.write(topi);
    delay(2000);
    //test=1;
  }
  for(int i = 0; i<100; i++)                       //가스를 감지하면 라즈베리파이에 가스가 감지되었다고 알려줌
  {
    gasValue = gasValue + analogRead(0);
  }
  gasValue = gasValue /100;
  gasVolts = gasValue/1024*5.0;
  if(gasVolts >1.4)
  {    
    //라즈베리에 알림
    topi = 'G';//GAS
    bluetooth.write(topi);
     digitalWrite(GASPIN,HIGH);
    delay(3000);
    digitalWrite(GASPIN,LOW);
  }
 motion_1 = digitalRead(MOTIONPIN_1);                          //if(motion_1==true&&motion_2==false&&motion_3==false){motion_1=true}; else motion_1=0;
                                                                //motion_2 = digitalRead(MOTIONPIN_2); if(motion_1==true&&motion_2==true&&motion_3==false){motion_2=true};  else motion_2=0;
                                                                //motion_3 = digitalRead(MOTIONPIN_3); if(motion_1==true&&motion_2==true&&motion_3==true){motion_3=true}; else motion_3=0;
  if(motion_1 == 1)                                           //&& motion_2 == true && motion_3 == true)                  //모션감지하기
  {
    //암호 물어봄
    topi = 'P';//password
    bluetooth.write(topi);   
    Serial.print(motion_1);
     digitalWrite(MOTIONPIN_2,HIGH);
    motion_1=0;
   
   delay(6000);
    digitalWrite(MOTIONPIN_2,LOW);
   bluetooth.flush();
  } //분리 
                                                      //hu,panon_,panoff_ 세개 수정 해야함      11/06
  
  if(frompi == 'H')//H HUMIDITY                           //라즈베리파이가 습도를 물어보면 습도를 알려줌
  {
   
    topi = (int)humidity/10;
    bluetooth.write((int)topi);
    Serial.print(humidity);
    Serial.print("             ");
      Serial.println((int)topi);
    delay(2000);
    //습도를 라즈베리로 전달
    frompi=0;
  }

  if(frompi=='A'&& pan ==false)  //A 팬온                          //라즈베리파이에 직접 환풍기를 켜달라고 요청했을때
  {
    pan = true;
    digitalWrite(PANPIN,HIGH);
    delay(2000);
    //test=1;                                                      //팬을 켜달라고 했을때는 습도가 40이하여도 돌아가게하려고 
    frompi=0;
  }
  
  if(frompi=='B'&& pan ==true)  //B팬오프                          //라즈베리파이에 직접 환풍기를 꺼달라고 요청했을때
  {
    pan = false;
    digitalWrite(PANPIN,LOW);
    delay(1000);
    //test=0;       //팬을 꺼달라고 하면 습도가 50이상이여도 꺼짐
    frompi=0;
  }

    delay(3000);
  
}
