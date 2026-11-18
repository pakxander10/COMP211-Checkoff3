#include <stdio.h>

double dot_product(double* vec1, double* vec2, int length) {
    double result = 0.0;
    for (int i = 0; i < length; i++) {
        result += vec1[i] * vec2[i];
    }
    return result;
}