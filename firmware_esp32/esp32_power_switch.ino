/*
 * RemotePower - ESP32 Smart PC Power Switch Firmware
 * 
 * Bu yazılım, bilgisayar tamamen kapalıyken (S5 durumu) bile anakartın
 * POWER_SW pinlerine fiziksel basma sinyali göndererek PC'yi açar.
 * 
 * Donanım Bağlantısı:
 * - ESP32 GPIO 4 -> Optokuplör / Röle IN -> PC Anakart POWER SW (+)
 * - ESP32 GND -> PC Anakart POWER SW (-)
 * - ESP32 5V/VIN -> PC Anakart Standby 5V (veya harici USB adaptör)
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

// Wi-Fi Ayarları
const char* ssid = "WIFI_ADINIZ";
const char* password = "WIFI_SIFRENIZ";

// RemotePower Sunucu Ayarları
const char* server_host = "your-cloud-server.com"; // Bulut sunucu IP veya domaini
const int server_port = 8080;
const char* device_id = "rp_esp32_hardware_switch_01"; // Sunucudaki cihaz ID'niz

// Pin Tanımları
const int RELAY_PIN = 4; // Optokuplör / Röle kontrol pini

WebSocketsClient webSocket;

void triggerPowerButton() {
  Serial.println("[RemotePower] Power butonu tetikleniyor (500ms basılı tutuluyor)...");
  digitalWrite(RELAY_PIN, HIGH);
  delay(500); // 0.5 saniye fiziksel basma simülasyonu
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("[RemotePower] Buton bırakıldı. Bilgisayar başlatılıyor!");
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("[RemotePower] Bulut sunucusundan bağlantı kesildi!");
      break;
    case WStype_CONNECTED:
      Serial.println("[RemotePower] Bulut sunucusuna başarıyla bağlandı!");
      break;
    case WStype_TEXT: {
      Serial.printf("[Gelen Mesaj]: %s\n", payload);
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, payload);
      if (!error) {
        const char* action = doc["action"];
        if (action && strcmp(action, "trigger_power_relay") == 0) {
          triggerPowerButton();
        }
      }
      break;
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  // Wi-Fi Bağlantısı
  Serial.printf("\nWi-Fi Ağına Bağlanılıyor: %s\n", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWi-Fi Bağlandı! IP: %s\n", WiFi.localIP().toString().c_str());

  // WebSocket Bağlantısı
  String path = "/ws/agent/" + String(device_id);
  webSocket.begin(server_host, server_port, path.c_str());
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();
}
