#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
 
char ssid[] = "wifi name";
char password[] = "wifi pw";
const char* mqtt_server = "localhost"; //broker

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup_wifi() {
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
 
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

//메세지를 받으면(Sub) 실행되는 함수
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  String msg = "";
  
  for (int i = 0; i < length; i++) {
    msg +=(char)payload[i];
  }
  
  Serial.print(msg);
  Serial.println();
}
 
void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
 
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  
  float val;
  
  char buf[16];
  
  val = analogRead(0); //A0핀의 값
  
  float temp = (3.3f * val * 100.0f) / 1024.0f; // 3.3v에 연결했으므로 3.3으로 계산한다.
  
  client.loop();
  
  dtostrf(temp, 4, 2, buf); // float to String 함수
  
  Serial.print("Publish message: ");
  Serial.println(buf);
  
  client.publish("temp", buf); //메세지 Publish

  delay(60000*60); //지연시간
}
