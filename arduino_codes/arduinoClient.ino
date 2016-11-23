#include <UIPEthernet.h>
#include <PubSubClient.h>
#include <IRremote.h>

IRsend irsend;
int khz = 38; // 38kHz carrier frequency for the NEC protocol
int rec;
int led = 13;

// Update these with values suitable for your network.
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
byte server[] = { 192, 168, 1, 141 };
byte ip[]     = { 192, 168, 1, 120 };

// Codigos raw ir minicadena

unsigned int  rawEstado[67] = {4300,4600, 450,700, 450,650, 450,650, 450,650, 450,1800, 450,650, 450,700, 400,700, 450,650, 450,650, 450,700, 450,650, 450,1800, 400,700, 450,650, 450,650, 450,700, 450,1750, 450,1800, 450,1750, 450,1800, 450,650, 450,650, 450,700, 450,1750, 450,700, 450,650, 450,650, 450,650, 450,1800, 450,1800, 400,1800, 450};
unsigned int  rawVolMas[67] = {4300,4650, 450,650, 450,650, 500,650, 450,650, 450,1750, 500,650, 450,650, 450,650, 500,650, 450,650, 450,650, 450,650, 500,1750, 450,650, 500,650, 400,700, 450,1750, 450,1800, 450,1800, 450,650, 450,1750, 500,650, 450,650, 450,650, 450,650, 450,700, 450,650, 450,1800, 400,700, 450,1750, 500,1750, 450,1800, 450};
unsigned int  rawVolMenos[67] = {4300,4600, 450,700, 450,650, 450,650, 450,700, 400,1800, 450,650, 450,700, 450,650, 450,650, 450,650, 500,650, 450,650, 450,1800, 450,650, 450,650, 500,600, 450,700, 450,1750, 500,1750, 450,650, 500,1750, 450,650, 450,650, 450,700, 450,1750, 450,650, 450,700, 450,1750, 500,650, 400,1800, 450,1800, 450,1750, 450};
unsigned int  rawCanalMas[67] = {4350,4600, 450,650, 450,700, 450,650, 450,650, 450,1800, 450,650, 450,650, 450,700, 450,650, 450,650, 450,650, 450,700, 450,1750, 450,700, 450,650, 450,650, 450,1800, 450,1750, 500,1750, 450,650, 500,600, 500,1750, 450,650, 500,1750, 450,650, 500,600, 450,700, 450,1750, 500,1750, 450,650, 450,1800, 450,650, 450}; 
unsigned int  rawCanalMenos[67] = {4350,4600, 450,650, 450,650, 450,700, 450,650, 450,1800, 450,650, 450,650, 500,600, 450,700, 450,650, 450,650, 450,700, 400,1800, 450,650, 450,700, 450,650, 450,650, 450,1800, 450,1750, 450,700, 450,650, 450,1800, 400,700, 450,1750, 450,1800, 450,650, 450,700, 400,1800, 450,1800, 450,650, 450,1800, 400,700, 450}; 
unsigned int  rawCanalUno[67] = {4300,4600, 450,700, 450,650, 450,650, 450,700, 450,1750, 450,650, 450,700, 450,650, 450,650, 450,700, 450,650, 450,650, 450,1800, 450,650, 450,650, 450,700, 450,1750, 450,650, 450,700, 450,650, 450,650, 450,700, 400,1800, 450,650, 450,700, 450,1750, 450,1800, 450,1750, 450,1800, 450,1800, 400,700, 450,1750, 450};

EthernetClient ethClient;
PubSubClient client(server, 11883, callback, ethClient);

long lastReconnectAttempt = 0;

// Callback function
void callback(char* topic, byte* payload, unsigned int length) {
  
  Serial.print(topic);
  Serial.print(" => ");
  Serial.write(payload, length);
  Serial.println();
  
  // Filtramos por topics
  if(strcmp(topic,"/estado")==0)rec=1; 
  if(strcmp(topic,"/volumen")==0)rec=2; 
  if(strcmp(topic,"/canal")==0)rec=3; 
  if(strcmp(topic,"/reset")==0)rec=4; 
  
  switch(rec){
    
    case 1:
      Serial.println("case recibo publicacion estado");
      onoff();
      break;
      
    case 2:
      Serial.println("case recibo publicacion volumen");
      volumen((char)payload[0]);
      break;
      
    case 3:
      Serial.println("case recibo publicacion canal");
      canal((char)payload[0]);
      break;
      
    case 4:
      Serial.println("case reset");
      reset();
      break;    
  }
  delay(1000);
  
}

void setup(){
  
  Serial.begin(38400);
  Serial.println("MQTT Subscribe test");
  pinMode(led, OUTPUT);
 
  // Activamos red
  Ethernet.begin(mac, ip);
  delay(1500);
  lastReconnectAttempt = 0;
  Serial.println("conectado por ethernet");
  
}

void loop(){
  // Funcion de reconexion no bloqueante, si el cliente mqtt pierde su conexion,
  //intenta reconectar cada 5 segundos sin bloquear la funcion main loop.
  if (!client.connected()) {
    long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      // Intento de reconectar
      if (reconnect()) {
        lastReconnectAttempt = 0;
      }
    }
  } else{
    // Client connected
    client.loop();
  }
}

boolean reconnect() {
  if (client.connect("arduinoMinicadenaClient")) {
    Serial.println("conectado a server mqtt");
    // ... and resubscribe
    client.subscribe("/estado");
    client.subscribe("/volumen");
    client.subscribe("/canal");
    client.subscribe("/reset");
  }
  return client.connected();
}

void onoff(){
  //for (int i = 0; i < 2; i++) {
    irsend.sendRaw(rawEstado, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
    delay(40);
  //}
}

void volumen(char vol){
  if(vol=='u'){
    Serial.println("if volumen up");
    irsend.sendRaw(rawVolMas, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  }
      
  if(vol=='d'){
    Serial.println("if volumen down");
    irsend.sendRaw(rawVolMenos, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  }

}

void canal(char can){
  if(can=='u'){
    Serial.println("if canal up");
    irsend.sendRaw(rawCanalMas, sizeof(rawCanalMas)/sizeof(rawCanalMas[0]), khz);
  }
  if(can=='d'){
    Serial.println("if canal down");
    irsend.sendRaw(rawCanalMenos, sizeof(rawCanalMenos)/sizeof(rawCanalMenos[0]), khz);
  }
}

void reset(){
  
  // Inicializamos volumen a 0
  for (int i = 0; i < 30; i++) {
    irsend.sendRaw(rawVolMenos, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
    delay(80);
  }
  delay(1000);
  
  // Inicializamos a canal 1
  irsend.sendRaw(rawCanalUno, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  delay(2000);

}
