void setup()
{
    Serial1.begin(4800);

}

void loop()
{
    Serial1.println("8.2, 0.5, 0.5, 0.5, 0.5"); // Send data to the worker
    delay(1000); // Wait for a second before sending the next message
}

