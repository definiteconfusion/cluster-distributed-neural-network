void setup()
{
    Serial.begin(9600);
    Serial1.begin(4800);
    Serial2.begin(4800);

}

void loop()
{
    if (Serial.available())
    {
        Serial1.write(Serial.read());
    }
}

