#include <stdio.h>
#include <stdbool.h>


void printChar(const char* character, bool errStream) {
	if(errStream) {
		fprintf(stderr, "%c", *character);
	}
	else {
		printf("%c", *character);
	}
}

