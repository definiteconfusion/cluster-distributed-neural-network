const int MAX_WEIGHTS = 50;  // Maximum number of weights to handle

float x, y, z, sI;  // Variables for x, y, z, and sI
float weights[MAX_WEIGHTS];  // Array to store the weights
int numWeights = 0;  // Number of weights received

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  Serial1.begin(4800);  // Initialize serial communication
}

void loop() {
  if (Serial1.available() > 0) {
    String inputString = Serial1.readStringUntil('\n');
    parseInput(inputString);
    processWeights();
    printResults();
  }
}

void parseInput(String input) {
  // Reset number of weights
  numWeights = 0;
  
  // Parse the input string
  int commaIndex = input.indexOf(',');
  int startIndex = 0;
  
  // Parse x
  x = input.substring(startIndex, commaIndex).toFloat();
  startIndex = commaIndex + 1;
  
  // Parse y
  commaIndex = input.indexOf(',', startIndex);
  y = input.substring(startIndex, commaIndex).toFloat();
  startIndex = commaIndex + 1;
  
  // Parse z
  commaIndex = input.indexOf(',', startIndex);
  z = input.substring(startIndex, commaIndex).toFloat();
  startIndex = commaIndex + 1;
  
  // Parse sI
  commaIndex = input.indexOf(',', startIndex);
  sI = input.substring(startIndex, commaIndex).toFloat();
  startIndex = commaIndex + 1;
  
  // Parse weights
  while (commaIndex != -1 && numWeights < MAX_WEIGHTS) {
    commaIndex = input.indexOf(',', startIndex);
    if (commaIndex != -1) {
      weights[numWeights] = input.substring(startIndex, commaIndex).toFloat();
      startIndex = commaIndex + 1;
    } else {
      // Last value (no comma after it)
      weights[numWeights] = input.substring(startIndex).toFloat();
    }
    numWeights++;
  }
  
}

void processWeights() {
  // Apply formula to each weight
  // Example formula: weight = weight * x + y * sin(z) + sI

  float layer_weight = 0.0;
    for (int i = 0; i < numWeights; i++) {
      Serial.println(weights[i]);
        layer_weight += weights[i];
    }

  float lr = 0.1; // Learning rate
  // Calculate the update factor once to avoid potential division by zero
  float update_factor = 0;
  if (x != 0 && layer_weight != 0) {
    update_factor = lr * (((y-z) / x) / (layer_weight / sI));
  }
  
  for (int i = 0; i < numWeights; i++) {
    Serial.print(weights[i]);
    weights[i] = weights[i] + update_factor;
    Serial.println(weights[i]);
  }
}

void printResults() {
  // Print the modified weights
  Serial.println("");
  for (int i = 0; i < numWeights; i++) {
    Serial.print(weights[i]);
    if (i < numWeights - 1) {
      Serial.print(", ");
    }
  }
}