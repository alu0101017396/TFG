void radar() {
  for(int i=0;i<=360;i+=15){  
   sensorDistanceRead(i);
  }
}

// FUNCTION 4: DISTANCE READING: ------------------------------------------------------------------------------------------//
float sensorDistanceRead(float servoAngle_) { 

  // First you read the angle you are given and move the servo motor:
  float chosenServoAngle=servoAngle_;
  sensorServo.write(chosenServoAngle);

  // Then choose the delay for the required angle, for 0º, 90º and 180º, the required time is longer:
  if ((chosenServoAngle == 90) || (chosenServoAngle == 0) || (chosenServoAngle == 45) || (chosenServoAngle == 135)) {
    delay(500); // servo movement large pause
  }
  else {
    delay(50);  // servo movement small pause
  }

  float referenceMv = 1000; // 1V for the WeMos D1

  // The distance in cm are calculated through the analog pin and the getsensorDistance function:
  float val = analogRead(sensorPin);
  
  // Then choose the delay for the required angle, for 0º, 90º and 180º, the required time is longer:
  if ((chosenServoAngle == 90) || (chosenServoAngle == 0) || (chosenServoAngle == 45) || (chosenServoAngle == 135)) {
    delay(500); // sensor reading large pause
  }
  else {
    delay(50);  // sensor reading small pause
  }
  delay(50); //  pause
  float mV = (val * referenceMv) / 1023;   // using the voltage reference and the resolution of A0
  float cm = getSensorDistance(mV); // the distance calculated with the sensor
  Serial.print("cm is: ");
  Serial.println(cm);
  float xValue = mV;
  float cmInter = Interpolation::ConstrainedSpline(xValues, yValues, numValues, xValue);
  Serial.print("cmInter is: ") ;
  Serial.println(cmInter);

  return cm;
}
//-------------------------------------------------------------------------------------------------------------------------//

// FUNCTION 5: GET sensorDistance: ----------------------------------------------------------------------------------------//
float getSensorDistance(int mV) {
   if (mV > mVinterval * tableEntries - 1) {

      // To check the correct distance calculations, uncomment the following two code lines:
      Serial.print("distancia predefinida:");
      Serial.println(sensorDistance[tableEntries - 1]);

      return sensorDistance[tableEntries - 1];
   }
   else {
      int index = mV / mVinterval;
      float frac = (mV % 100) / (float)mVinterval; // 100 mV for the interval, but in integer
      
      // To check the correct distance calculations, uncomment the following 15 code lines:
      Serial.print(index);
      Serial.print("=");
      Serial.print(mV);
      Serial.print("/");
      Serial.println(mVinterval);
      Serial.print("distancia calculada:");
      Serial.print(sensorDistance[index]);
      Serial.print("-((");
      Serial.print(sensorDistance[index]);
      Serial.print("-");
      Serial.print(sensorDistance[index+1]);
      Serial.print(")*");
      Serial.print(frac);
      Serial.print(")=");
      Serial.println(sensorDistance[index] - ((sensorDistance[index] - sensorDistance[index + 1]) * frac));

      return sensorDistance[index] - ((sensorDistance[index] - sensorDistance[index + 1]) * frac);
   }
}
//-------------------------------------------------------------------------------------------------------------------------//
