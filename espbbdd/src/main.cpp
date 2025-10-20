#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <U8g2lib.h>
#include "ArduinoJson.h"
#include <ArduinoHttpClient.h> 

const char* ssid = "nashe";
const char* password = "weonklxd";
const char* api_host = "10.180.155.38";
const int   api_port = 8000;
const char* api_path = "/reception";

#define API_KEY "kbsCrgB43DVtQmyJwzX09Cuia2eL7rNASsEZ1YTKOgc=" 

U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

#define POT_HUMEDAD_PIN    34 // Potenciómetro 1
#define POT_TEMP_PIN       35 // Potenciómetro 2
#define SWITCH_BOTON_PIN   25 // Switch

unsigned long tiempoAnterior = 0;
const long intervalo = 10000;

float humedad_val;
float temp_val;
int   boton_val; 

void setup() {
  Serial.begin(115200);
  u8g2.begin();
  

  pinMode(POT_HUMEDAD_PIN, INPUT);
  pinMode(POT_TEMP_PIN, INPUT);
  pinMode(SWITCH_BOTON_PIN, INPUT_PULLUP); // (HIGH = 1, LOW = 0)
  
  WiFi.begin(ssid, password);
}

void checkWiFiConnection() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  Serial.println("Conexión WiFi perdida. Reconectando...");
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.drawStr(0, 32, "Reconectando..."); 
  u8g2.sendBuffer();
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nReconectado!");
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_ncenB08_tr);
    u8g2.drawStr(0, 24, "Conectado!");
    u8g2.setFont(u8g2_font_6x10_tf);
    u8g2.drawStr(0, 40, WiFi.localIP().toString().c_str());
    u8g2.sendBuffer();
    delay(2000);  
  }
}

void loop() {

  checkWiFiConnection();

  if (WiFi.status() == WL_CONNECTED) {
    unsigned long tiempoActual = millis();
    if (tiempoActual - tiempoAnterior >= intervalo) {
      tiempoAnterior = tiempoActual;

      int pot1_raw = analogRead(POT_HUMEDAD_PIN);
      int pot2_raw = analogRead(POT_TEMP_PIN);

      boton_val = digitalRead(SWITCH_BOTON_PIN); 

      humedad_val = map(pot1_raw, 0, 4095, 0, 100);

      temp_val = map(pot2_raw, 0, 4095, 0, 50);

      u8g2.clearBuffer();
      u8g2.setFont(u8g2_font_ncenB08_tr);
      u8g2.drawStr(0, 24, "Enviando Datos...");
      u8g2.setFont(u8g2_font_6x10_tf);
      u8g2.setCursor(0, 40); u8g2.print("Hum: "); u8g2.print(humedad_val, 0); u8g2.print("%");
      u8g2.setCursor(64, 40); u8g2.print("Temp: "); u8g2.print(temp_val, 1); u8g2.print("C");
      u8g2.setCursor(0, 55); u8g2.print("Boton: "); u8g2.print(boton_val);
      u8g2.sendBuffer();

      WiFiClient client;
      HttpClient http(client, api_host, api_port); 

      JsonDocument doc_enviar;

      doc_enviar["Humedad"] = humedad_val;
      doc_enviar["Temperatura"] = temp_val;
      doc_enviar["EstadoBoton"] = boton_val;
      
      String json_payload;
      serializeJson(doc_enviar, json_payload);

      http.beginRequest(); 
      http.post(api_path); 
      http.sendHeader("Content-Type", "application/json");

      http.sendHeader("API-Key", API_KEY); 
      http.sendHeader("Content-Length", json_payload.length());
      http.beginBody();
      http.print(json_payload);
      http.endRequest();

      int httpCode = http.responseStatusCode();
      if (httpCode > 0) {
        String response_payload = http.responseBody();
        JsonDocument doc_recibir;
        deserializeJson(doc_recibir, response_payload);
        
        const char* respuesta_api = doc_recibir["respuesta"];
        const char* fechahora_api = doc_recibir["fechahora"];

        u8g2.clearBuffer();
        u8g2.setFont(u8g2_font_ncenB08_tr);
        u8g2.drawStr(0, 24, "Datos Recibidos!");
        u8g2.setFont(u8g2_font_6x10_tf);
        u8g2.setCursor(0, 40); u8g2.print("R: "); u8g2.print(respuesta_api);
        u8g2.setCursor(0, 55); u8g2.print(fechahora_api);
        u8g2.sendBuffer();
        
      } else {
        u8g2.clearBuffer();
        u8g2.setFont(u8g2_font_ncenB08_tr);
        u8g2.drawStr(0, 24, "Error API");
        u8g2.setFont(u8g2_font_6x10_tf);
        u8g2.setCursor(0, 40); u8g2.print("Codigo: "); u8g2.print(httpCode);
        u8g2.sendBuffer();
      }
    }
  }
}