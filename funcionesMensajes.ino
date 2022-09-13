

String traducirOrdenEnv(String mensaje){
  String bitString = "";
  int j  = 0;
  while (mensaje[j] != '\0') {
     for(int i = 7; i >= 0; i--) {
    
       bitString += bitRead(mensaje[j], i);
     }
  j++;
  }
  return bitString;
}

String traducirOrdenRec(String mensajeBit){
  int j  = 0;
  String ordenTrad = "";
       for(int i=0; i<mensajeBit.length(); i++) {
    }
    while (mensajeBit[j] != '\0') {
       int contador = 7;

       int bitEnInt = 0;
       int limite = j +8;
           for (int i = j; i < limite; i++) {


             if (mensajeBit.charAt(i)== '1') {
                bitEnInt += pow( 2, contador);


             }
             contador--;
             j++;
           }


            byte aux = bitEnInt;
           char charTraducido = aux;
            ordenTrad += charTraducido;
    }

  return ordenTrad;
}

bool comprobarCheckSum(String mensaje, String chcksum) {
    Serial.print("mensajeChck: ");

    for(int i=0; i<mensaje.length(); i++) {
      Serial.print(mensaje.charAt(i));
    }
    Serial.print("chksumm: ");
    for(int i=0; i<chcksum.length(); i++) {
      Serial.print(chcksum.charAt(i));
    }
  int value = 0;
  for (int j = 0; j < mensaje.length() / 8; j++) {
      int aux = 0;
    for (int i = 0; i < 8; i++)  // for every character in the string  strlen(s) returns the length of a char array
    {
      aux *= 2; // double the result so far
      if (mensaje[j * 8 + i] == '1') aux++;  //add 1 if needed
    }
    value += aux;
  }
  int chckSum = 0;
  
 for (int i = 0; i < 8; i++) 
  {
    chckSum *= 2; // double the result so far
    if (chcksum[i] == '0') chckSum++;  //add 1 if needed
  }


  if (value == chckSum) {
          Serial.print("bien");

    return true;
  }

  return false;

}

String calcularChecksum(String mensaje, int nBits) {
  
  int value = 0;
  for (int j = 0; j < mensaje.length() / 8; j++) {
      int aux = 0;
    for (int i = 0; i < 8; i++) 
    {
      aux *= 2; // double the result so far
      if (mensaje[j * 8 + i] == '1') aux++;  //add 1 if needed
    }
    value += aux;
  }
  int chckSum = 0;
  value = -value - 1;

  String chcksum = "";
for (int i = nBits; i >= 0; i--) {
  if( (value & (1 << i)) != 0) {
    chcksum = chcksum + "1";
    
  } else {
        chcksum = chcksum + "0";

  }
}
  return chcksum;

}


String WaitForAnswer(String httpUrl) {
 
  http.begin(client, httpUrl);
  http.GET();
  TheHiddenAnswerOfClient = (http.getString());
  http.end();
  return TheHiddenAnswerOfClient;
}

void realizaFuncion(String msj) {

  int szChecksumExt =  msj.length() % 8;

  int finMensaje = msj.length() - 8 - szChecksumExt;
  String mensaje = msj.substring(0, finMensaje);
  String chcksum = msj.substring(finMensaje);
  if (comprobarCheckSum(mensaje, chcksum) == false) {
     enviarMensajeError();   
     return;
     }

   mensaje = traducirOrdenRec(mensaje);

    switch (mensaje[mensaje.length() - 1]) {
    case '/':
      reenviarMensaje();
      break;
    case '0':
      mensajeErrorAccion();
      break;
    case '1':
      break;
  
    case '2':
      break;
    case '3':
      enviarBateria();
      break;

    case '4':
      devolverDistanciaSensor();
      break;
    case '5':
      moverPasos(mensaje);
      break;
  }
}

void reenviarMensaje() {
  mensajeGlobal = ultMensaje;

}

void enviarMensajeError() {
  String mensajeError = "00101111";
  mensajeGlobal = mensajeError + calcularChecksum(mensajeError, 8);

 
}

void mensajeErrorAccion() {
  String mensajeRecibido = "00110000";
  mensajeGlobal = mensajeRecibido + calcularChecksum(mensajeRecibido , 8);


}

void PostCompletado() {
  String mensajeCompletado = "00110010";

  mensajeGlobal = mensajeCompletado + calcularChecksum(mensajeCompletado, 8);

}

void enviarBateria() {

}

void devolverDistanciaSensor() {
  String mensajeDistancia = "00110010";
  httpurl = "http://192.168.1.46:8080/";
  String distancia = String(sensorDistanceRead(1), 2);

  String distanciaTraducida = traducirOrdenEnv(distancia);
   
 String algo = distanciaTraducida + mensajeDistancia;
 String checksums = calcularChecksum(algo, 14);
  mensajeGlobal = distanciaTraducida + mensajeDistancia + checksums; 
  
    

}

void moverPasos(String mensaje) {
  String mensajeMover = "00110010";
  Serial.print("MENSAJEMOVER is: ") ;
  Serial.println(mensaje);
  char direccion = mensaje.charAt(0);
  String aux = mensaje.substring(1, mensaje.length());
  int pasos = aux.toFloat();
  movement(mensaje[0], pasos);

  mensajeGlobal = mensajeMover + calcularChecksum(mensajeMover, 8);

}
