/*
 * Instituto Tecnologico de Costa Rica
 * Ingenieria en Computadores
 * Compiladores
 * 
 * Código Servidor
 * Implementación del servidor NodeMCU
 * 2023

 * Restricciónes: Biblioteca ESP8266WiFi instalada
 */
#include <ESP8266WiFi.h>

//Cantidad maxima de clientes es 1
#define MAX_SRV_CLIENTS 1
//Puerto por el que escucha el servidor
#define PORT 7070

/*
 * ssid: Nombre de la Red a la que se va a conectar el Arduino
 * password: Contraseña de la red
 * 
 * Este servidor no funciona correctamente en las redes del TEC,
 * se recomienda crear un hotspot con el celular
 *TP-Link_331A, 76669385
 */
const char* ssid = "vale";
const char* password = "12345678";


// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

/*
 * Intervalo de tiempo que se espera para comprobar que haya un nuevo mensaje
 */
unsigned long previousMillis = 0, temp = 0;
const long interval = 100;

/*
 * Variables para controlar los motores.
 * EnA y EnB son los que habilitan las salidas del driver.
 * EnA = 0 o EnB = 0 -> free run (No importa que haya en las entradas el motor no recibe potencia)
 * EnA = 0 -> Controla la potencia (Para regular la velocidad utilizar analogWrite(EnA,valor), 
 * con valor [0-1023])
 * EnB = 0 -> Controla la dirección, poner en 0 para avanzar directo.
 * In1 e In2 son inputs de driver, controlan el giro del motor de potencia
 * In1 = 0 ∧ In2 = 1 -> Moverse hacia adelante motor A
 * In1 = 1 ∧ In2 = 0 -> Moverse en reversa motor A
 * In3 e In4 son inputs de driver, controlan la dirección del carro
 * In3 = 0 ∧ In4 = 1 -> Moverse hacia adelante motor B
 * In3 = 1 ∧ In4 = 0 -> Moverse en reversa motor B
 */
#define EnA 2 //D4 
#define In1 0 //D3 
#define In2 4 //D2
#define In3 5 //D1
#define EnB 14 //D5 
#define In4 16 //D0
// 0 para ir hacia adelante


/**
 * Función de configuración.
 * Se ejecuta la primera vez que el módulo se enciende.
 * Si no puede conectarse a la red especificada entra en un ciclo infinito 
 * hasta ser reestablecido y volver a llamar a la función de setup.
 * La velocidad de comunicación serial es de 115200 baudios, tenga presente
 * el valor para el monitor serial.
 */
void setup() {
  Serial.begin(115200);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  pinMode(EnA,OUTPUT);
  pinMode(EnB,OUTPUT);
  
  // ip estática para el servidor
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  // Modo para conectarse a la red
  WiFi.mode(WIFI_STA);
  // Intenta conectar a la red
  WiFi.begin(ssid, password);
  
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("\nCould not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.print("\nConnection Succeeded to: "); Serial.println(ssid);
    Serial.println(".....\nWaiting for a client at");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Port: ");
    Serial.print(PORT);
  }
  server.begin();
  server.setNoDelay(true);

}

/*
 * Función principal que llama a las otras funciones y recibe los mensajes del cliente
 * Esta función comprueba que haya un nuevo mensaje y llama a la función de procesar
 * para interpretar el mensaje recibido.
 */

byte data= 0b11111111;
void loop() {
  
  unsigned long currentMillis = millis();
  uint8_t i;
  //check if there are any new clients
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      //find free/disconnected spot
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //no free/disconnected spot so reject
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      // El cliente existe y está conectado
      if (serverClients[i] && serverClients[i].connected()) {
        // El cliente tiene un nuevo mensaje
        if(serverClients[i].available()){
          // Leemos el cliente hasta el caracter '\r'
          String mensaje = serverClients[i].readStringUntil('\r');
          // Eliminamos el mensaje leído.
          serverClients[i].flush();
          
          // Preparamos la respuesta para el cliente
          String respuesta; 
          procesar(mensaje, &respuesta);
          Serial.println(mensaje);
          // Escribimos la respuesta al cliente.
          serverClients[i].println(respuesta);
        }  
        serverClients[i].stop();
      }
    }
  }
}

/** Movimiento de los motores */
String implementar(String llave, String valor){
   int y=0;
  /**
   * La variable result puede cambiar para beneficio del desarrollador
   * Si desea obtener más información al ejecutar un comando.
   */
  String result="ok;";
  Serial.print("Comparing llave: ");
  Serial.println(llave);
  
  //LLave pwm = movimientos hacia adelante, atras o detener el movimiento
  if(llave == "pwm"){

      if(valor.toInt()==0){
      digitalWrite (In1,LOW);
      digitalWrite (In2,LOW);
      digitalWrite (In3,LOW);
      digitalWrite (In4,LOW);
      analogWrite (EnA,0);
      analogWrite (EnB,0);
      result = "detenido";
    }
      else if(valor.toInt()>0){
      digitalWrite (In1,HIGH);
      digitalWrite (In2,LOW);
      digitalWrite (In3,HIGH);
      digitalWrite (In4,LOW);
      analogWrite (EnA,valor.toInt());
      analogWrite (EnB,valor.toInt());
      result = "adelante";
    }
    else if(valor.toInt()<0){
      digitalWrite (In2,HIGH);  
      digitalWrite (In1,LOW);
      digitalWrite (In3,HIGH);  
      digitalWrite (In4,LOW);
      y= -(valor.toInt());
      analogWrite (EnA,y);
      analogWrite (EnB,y);
      
      result = "reversa";
      
    } 
    
      Serial.print("Move....: ");
      Serial.println(valor);
  }
      
  //Direcciones
  /**
  else if(llave == "dir"){
    if(valor.toInt() == -1){
      digitalWrite (In3,HIGH);
      digitalWrite (In4,LOW);
      analogWrite(EnB,1000);
      result = "izquierda";
      Serial.println("Girando izquierda");
      }

      else if(valor.toInt() == 0){
      digitalWrite (In3,LOW);
      digitalWrite (In4,LOW);
      analogWrite(EnB,0);
      result = "directo";
      Serial.println("directo");
      }

      else if(valor.toInt() == 1){
      digitalWrite (In3,LOW);
      digitalWrite (In4,HIGH);
      analogWrite(EnB,1000);
      result = "derecha";
      Serial.println("Girando derecha");
      }
  }*/

   /* El comando tiene el formato correcto pero no tiene sentido para el servidor
   */
  else{
    result = "Undefined key value: " + llave+";";
    Serial.println(result);
  }
  return result;
}

/*
 * Función para dividir los comandos en pares llave, valor
 * para ser interpretados y ejecutados por el Carro
 * Un mensaje puede tener una lista de comandos separados por ;
 * Se analiza cada comando por separado.
 * Esta función es semejante a string.split(char) de python
 * 
 */
void procesar(String input, String * output){
  //Buscamos el delimitador ;
  Serial.println("Checking input....... ");
  int comienzo = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',comienzo);
  
  while(delComa>0){
    String comando = input.substring(comienzo, delComa);
    Serial.print("Processing comando: ");
    Serial.println(comando);
    del2puntos = comando.indexOf(':');
    /*
    * Si el comando tiene ':', es decir tiene un valor
    * se llama a la función exe 
    */
    if(del2puntos>0){
        String llave = comando.substring(0,del2puntos);
        String valor = comando.substring(del2puntos+1);

        Serial.print("(llave, valor) = ");
        Serial.print(llave);
        Serial.println(valor);
        //Una vez separado en llave valor 
        *output = implementar(llave,valor); 
    }
    //Aqui se llamaba getSense en caso de que comando == "sense"
    //No se necesita porque se usaba para obtener valores de la bateria y fotoresistencia

      //Aqui iban movimientos como zig zag, circulo, etc
    
    else if(comando=="det"){
      digitalWrite (In1,LOW);
      digitalWrite (In2,LOW);
      digitalWrite (In3,LOW);
      digitalWrite (In4,LOW);
      result="detenido";
      
      }
    comienzo = delComa+1;
    delComa = input.indexOf(';',comienzo);
  }
}





