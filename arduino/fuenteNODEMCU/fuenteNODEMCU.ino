#include "DHT.h"
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <PubSubClient.h>

#define DHTTYPE DHT11   // DHT 22  (AM2302), AM2321
#define LED_BUILTIN 2

const char* ssid = "CoopenetFIBRA-6858513";
const char* password = "dni18233328";

//Nombre o IP del servidor mosquitto
const char* mosquitto_user = "";
const char* mosquitto_password = "";
const char* mqtt_server = "192.168.1.17";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[500];
int value = 0;

//iniciamos el cliente udp para su uso con el server NTP
WiFiUDP ntpUDP;

// cuando creamos el cliente NTP podemos especificar el servidor al // que nos vamos a conectar en este caso
// 0.south-america.pool.ntp.org SudAmerica
// también podemos especificar el offset en segundos para que nos
// muestre la hora según nuestra zona horaria en este caso
// restamos -10800 segundos ya que estoy en argentina.
// y por ultimo especificamos el intervalo de actualización en
// mili segundos en este caso 6000

NTPClient timeClient(ntpUDP, "0.south-america.pool.ntp.org", -10800, 6000);



const int DHTPin = 14;     // what digital pin we're connected to
DHT dht(DHTPin, DHTTYPE);







void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str()),mosquitto_user,mosquitto_password) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}





void setup() {
  Serial.begin(9600);
  Serial.println("DHTxx test!");
  dht.begin();
  pinMode(LED_BUILTIN, OUTPUT);

  WiFi.begin(ssid, password); // nos conectamos al wifi

  // Esperamos hasta que se establezca la conexión wifi
  while ( WiFi.status() != WL_CONNECTED ) {
    delay ( 500 );
    Serial.print ( "." );
  }

  timeClient.begin();


  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
void clima() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  timeClient.update(); //sincronizamos con el server NTP

  time_t rawtime = timeClient.getEpochTime();
  struct tm * ti;
  ti = localtime (&rawtime);

  uint16_t year = ti->tm_year + 1900;
  String yearStr = String(year);

  uint8_t month = ti->tm_mon + 1;
  String monthStr = month < 10 ? "0" + String(month) : String(month);

  uint8_t day = ti->tm_mday;
  String dayStr = day < 10 ? "0" + String(day) : String(day);




  Serial.println("{'ano': '" + String(yearStr) + "','mes': '" + String(monthStr) + "','dia': '" + String( dayStr) + "','hora': '" + String( timeClient.getHours()) + "','temp': '" + String(t) + "', 'humidity': '" + String(h) + "', 'location_id': '1'}");

}
void loop() {

 float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  timeClient.update(); //sincronizamos con el server NTP

  time_t rawtime = timeClient.getEpochTime();
  struct tm * ti;
  ti = localtime (&rawtime);

  uint16_t year = ti->tm_year + 1900;
  String yearStr = String(year);

  uint8_t month = ti->tm_mon + 1;
  String monthStr = month < 10 ? "0" + String(month) : String(month);

  uint8_t day = ti->tm_mday;
  String dayStr = day < 10 ? "0" + String(day) : String(day);
  

 String msge = "{\"ano\": \"" + String(yearStr) + "\",\"mes\": \"" + String(monthStr) + "\",\"dia\": \"" + String( dayStr) + "\",\"hora\": \"" + String( timeClient.getHours()) + "\",\"temp\": \"" + String(t) + "\", \"humidity\": \"" + String(h) + "\", \"location_id\": \"1\"}";


  char* mensaje;
  int msg_len = msge.length() + 1;
  char msg_array[msg_len];
  msge.toCharArray(msg_array, msg_len);









  // Encender el LED (Está conectado con una resistencia pull-up,
  // por eso se enciende si el pin está a nivel bajo)
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000); // Esperar un segundo
  // Apagar el LED
  digitalWrite(LED_BUILTIN, HIGH);


  // Wait a few seconds between measurements.
  delay(20000);
  clima();
  
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    Serial.print("Publish message: ");
    Serial.println(msg_array);
    client.publish("clima", msg_array);
  }
}
