#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {  // Need at least weight and one value
        printf("Usage: %s weight value1 [value2 ...]\n", argv[0]);
        return 1;
    }

    // Get weight from first argument
    const double w = atof(argv[1]);
    double sum = 0.0;

    // Calculate sum of x[i] * w for all remaining arguments
    for (int i = 2; i < argc; i++) {
        double x = atof(argv[i]);
        sum += x * w;
    }

    printf("%f", sum);
    return 0;
}