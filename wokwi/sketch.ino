#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#define DHTPIN 15
#define DHTTYPE DHT22
#define TRIG_PIN 5
#define ECHO_PIN 18
#define RAIN_PIN 34
DHT dht(DHTPIN,DHTTYPE);
const char* WIFI_SSID="Wokwi-GUEST";
const char* WIFI_PASSWORD="";
const char* SERVER_URL="https://YOUR-PUBLIC-HTTPS-TUNNEL/api/sensor";
const char* API_KEY="change-this-demo-key";
float waterDistance(){
 digitalWrite(TRIG_PIN,LOW);delayMicroseconds(2);digitalWrite(TRIG_PIN,HIGH);delayMicroseconds(10);digitalWrite(TRIG_PIN,LOW);
 long duration=pulseIn(ECHO_PIN,HIGH,30000);if(duration==0)return 400.0;return duration*0.0343/2.0;
}
void setup(){Serial.begin(115200);pinMode(TRIG_PIN,OUTPUT);pinMode(ECHO_PIN,INPUT);dht.begin();
 WiFi.begin(WIFI_SSID,WIFI_PASSWORD,6);while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}Serial.println("WiFi connected");}
void loop(){if(WiFi.status()==WL_CONNECTED){
 float t=dht.readTemperature(),h=dht.readHumidity(),w=waterDistance();
 float rain=analogRead(RAIN_PIN)*100.0/4095.0; // potentiometer simulates rain input
 if(!isnan(t)&&!isnan(h)){String body="{\"station_id\":\"station-01\",\"station_name\":\"Wokwi ESP32 Station\",\"latitude\":19.076,\"longitude\":72.8777,\"temperature\":"+String(t,1)+",\"humidity\":"+String(h,1)+",\"water_distance_cm\":"+String(w,1)+",\"rainfall_percent\":"+String(rain,1)+"}";
 HTTPClient http;http.begin(SERVER_URL);http.addHeader("Content-Type","application/json");http.addHeader("X-API-Key",API_KEY);
 int code=http.POST(body);Serial.printf("HTTP status: %d\\n",code);Serial.println(http.getString());http.end();
 }else Serial.println("DHT read failed");
 }else{Serial.println("WiFi disconnected");WiFi.reconnect();}delay(5000);}
