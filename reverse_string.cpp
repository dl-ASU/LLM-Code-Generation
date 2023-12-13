// Include the iostream header file
#include <iostream>
#include <cstring>
using namespace std;

// A function definition for a function that reverses a string
char* reverse_string(char* str) {
    // Get the length of the string
    int len = strlen(str);
    // Allocate memory for the reversed string
    char* rev = (char*)malloc(len + 1);
    // Check if the memory allocation was successful
    if (rev == NULL) {
    return NULL;
    }
    // Copy the characters from the original string to the reversed string in reverse order
    for (int i = 0; i < len; i++) {
    rev[i] = str[len - i - 1];
    }
    // Add the null terminator to the reversed string
    rev[len] = '\0';
    // Return the reversed string
    return rev;
}

int main() {
    const int maxInputLength = 100;  // Adjust the maximum input length as needed
    char input[maxInputLength];

    // Get input from the user
    std::cin.getline(input, maxInputLength);

    // Call the reverse_string function
    char* reversed = reverse_string(input);

    // Display the result
    std::cout << reversed << std::endl;

    // Free the allocated memory
    free(reversed);

    return 0;
}