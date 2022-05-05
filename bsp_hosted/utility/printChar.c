#include <stdbool.h>
#include <stdio.h>

void printChar(const char* character, bool errStream) {
  if (errStream) {
    fprintf(stderr, "%c", *character);
  } else {
    printf("%c", *character);
  }
}
