#include <UIPEthernet.h>
#include <PubSubClient.h>
#include <IRremote.h>

IRsend irsend;
int khz = 38; // 38kHz carrier frequency for the NEC protocol
int rec;
int led = 13;

// Update these with values suitable for your network. MAC UNIQUE IN THE NETWORK
byte mac[]    = {  0xXX, 0xXX, 0xXX, 0xXX, 0xXX, 0xXX };
byte server[] = { 'X', 'X', 'X', 'X' };
byte ip[]     = { 'X', 'X', 'X', 'X' };

// Ir codes to send
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
  
  // Topic filtering
  if(strcmp(topic,"/estado")==0)rec=1; 
  if(strcmp(topic,"/volumen")==0)rec=2; 
  if(strcmp(topic,"/canal")==0)rec=3; 
  if(strcmp(topic,"/reset")==0)rec=4; 
  
  switch(rec){
    //Case change state on/off
    case 1:
      Serial.println("case recibo publicacion estado");
      onoff();
      break;
    //Change volume with recived value (up or down)  
    case 2:
      Serial.println("case recibo publicacion volumen");
      volumen((char)payload[0]);
      break;
    //Change channel with recived value (up or down)   
    case 3:
      Serial.println("case recibo publicacion canal");
      canal((char)payload[0]);
      break;
    //Go system to kwonw state  
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
//Ir code to send on/off order
void onoff(){
  //for (int i = 0; i < 2; i++) {
    irsend.sendRaw(rawEstado, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
    delay(40);
  //}
}
//Ir code to change volume
void volumen(char vol){
  //if 'u' value, send up value code
  if(vol=='u'){
    Serial.println("if volumen up");
    irsend.sendRaw(rawVolMas, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  }
  //if 'd' value, send down value code   
  if(vol=='d'){
    Serial.println("if volumen down");
    irsend.sendRaw(rawVolMenos, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  }

}
//Ir code to change channel
void canal(char can){
  //if 'u' value, send up value code
  if(can=='u'){
    Serial.println("if canal up");
    irsend.sendRaw(rawCanalMas, sizeof(rawCanalMas)/sizeof(rawCanalMas[0]), khz);
  }
  //if 'd' value, send down value code
  if(can=='d'){
    Serial.println("if canal down");
    irsend.sendRaw(rawCanalMenos, sizeof(rawCanalMenos)/sizeof(rawCanalMenos[0]), khz);
  }
}
//Ir codes to go system to a known state
void reset(){
  
  // Set volume to 0
  for (int i = 0; i < 30; i++) {
    irsend.sendRaw(rawVolMenos, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
    delay(80);
  }
  delay(1000);
  
  // Set channel to 0
  irsend.sendRaw(rawCanalUno, sizeof(rawEstado)/sizeof(rawEstado[0]), khz);
  delay(2000);

}
