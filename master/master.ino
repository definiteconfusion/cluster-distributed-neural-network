void setup()
{
    Serial.begin(19200);
    Serial1.begin(4800);
    Serial2.begin(4800);

}

void loop()
{
    if (Serial.available() > 0) {
        Serial1.println(Serial.readStringUntil('\n'));
        float worker_id;
        String inputString = Serial.readStringUntil('\n');
        int commaIndex = inputString.indexOf(',');
        int startIndex = 0;
        worker_id = inputString.substring(startIndex, commaIndex).toFloat();
        startIndex = commaIndex + 1;
        if (worker_id == 1) {
            Serial1.println(inputString.substring(commaIndex + 1));
        }
        else if (worker_id == 2) {
            Serial2.println(inputString.substring(commaIndex + 1));
            
        }
      }
      else if (Serial1.available() > 0) {
        String inputString = Serial1.readStringUntil('\n');
        if (inputString.length() > 0) {
            Serial.println(inputString);
        }
    }
    else if (Serial2.available() > 0) {
        String inputString = Serial2.readStringUntil('\n');
        if (inputString.length() > 0) {
            Serial.println(inputString);
        }
    }
}

