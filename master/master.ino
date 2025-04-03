void setup()
{
    Serial.begin(9600);
    Serial1.begin(4800);
    Serial2.begin(4800);

}

void loop()
{
    if (Serial.available() > 0) {
        float worker_id;
        String inputString = Serial.readStringUntil('\n');
        int commaIndex = inputString.indexOf(',');
        int startIndex = 0;
        worker_id = inputString.substring(startIndex, commaIndex).toFloat();
        startIndex = commaIndex + 1;
        if (worker_id == 1) {
            Serial.println(inputString.substring(commaIndex + 1));
            Serial1.println(inputString.substring(commaIndex + 1));
        }
        else if (worker_id == 2) {
            Serial.println(inputString.substring(commaIndex + 1));
            Serial2.println(inputString.substring(commaIndex + 1));
            
        }
      }
}

