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
  // Example input: 1, 30, 0.5, 1.27, 3.55, 0.7, 0.5, 0.2
  // Reset number of weights
  numWeights = 0;
  
  // Find the first comma to skip the initial value
  int startIndex = 0;
  int commaIndex = input.indexOf(',');
  if (commaIndex == -1) return; // Error case, no commas found
  
  // Parse x - it's the second value in the string
  startIndex = commaIndex + 1;
  commaIndex = input.indexOf(',', startIndex);
  if (commaIndex == -1) {
    // If there's no more commas, take the rest of the string
    x = input.substring(startIndex).toFloat();
    return; // No more values to parse
  } else {
    x = input.substring(startIndex, commaIndex).toFloat();
  }
  
  // Parse y
  startIndex = commaIndex + 1;
  commaIndex = input.indexOf(',', startIndex);
  if (commaIndex == -1) {
    y = input.substring(startIndex).toFloat();
    return;
  } else {
    y = input.substring(startIndex, commaIndex).toFloat();
  }
  
  // Parse z
  startIndex = commaIndex + 1;
  commaIndex = input.indexOf(',', startIndex);
  if (commaIndex == -1) {
    z = input.substring(startIndex).toFloat();
    return;
  } else {
    z = input.substring(startIndex, commaIndex).toFloat();
  }
  
  // Parse sI
  startIndex = commaIndex + 1;
  commaIndex = input.indexOf(',', startIndex);
  if (commaIndex == -1) {
    sI = input.substring(startIndex).toFloat();
    return;
  } else {
    sI = input.substring(startIndex, commaIndex).toFloat();
  }
  
  // Parse weights
  startIndex = commaIndex + 1;
  while (startIndex < input.length() && numWeights < MAX_WEIGHTS) {
    commaIndex = input.indexOf(',', startIndex);
    if (commaIndex != -1) {
      weights[numWeights] = input.substring(startIndex, commaIndex).toFloat();
      startIndex = commaIndex + 1;
    } else {
      // Last value (no comma after it)
      weights[numWeights] = input.substring(startIndex).toFloat();
      startIndex = input.length();
    }
    numWeights++;
  }
}

void processWeights() {
  // Apply formula to each weight
  // Example formula: weight = weight * x + y * sin(z) + sI

  float layer_weight = 0.0;
    for (int i = 0; i < numWeights; i++) {
        layer_weight += weights[i];
    }

  float lr = 0.1; // Learning rate
  // Calculate the update factor once to avoid potential division by zero
  float update_factor = 0;
  if (x != 0 && layer_weight != 0) {
    // update_factor = lr * ((((float)(z - y) / y) * ((float)layer_weight / sI)) * (1.0f / x));
    update_factor = (1.0 / (((z - y) / y) * ((z - y) / y))) * (layer_weight / sI);
    Serial.println(update_factor);
  }
  
  for (int i = 0; i < numWeights; i++) {
    weights[i] = weights[i] + update_factor;
  }
}

void printResults() {
  // Print the modified weights
  for (int i = 0; i < numWeights; i++) {
    Serial1.print(weights[i]);
    if (i < numWeights - 1) {
      Serial1.print(", ");
    }
  }
}