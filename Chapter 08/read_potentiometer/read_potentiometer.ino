/*
  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
*/

void setup() {
    // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  // read the input on analog pin 0:
  int i;
  int cnt = 20;
  int  sum = 0;
  for (i = 0; i<cnt; i++)
  {
    int sensorValue = analogRead(A0);
    sum = sum + sensorValue;
    delay(1);        // delay in between reads for stability 
  }
  int avg_value = sum/20;
  int outputValue = map(avg_value, 0, 1023, 0, 255);
  // print out the value you read:
  //float norm_value = (float)avg_value/1023;
  Serial.println(outputValue);
  analogWrite(LED_BUILTIN, outputValue); 
  //delay(1);        // delay in between reads for stability  

}
