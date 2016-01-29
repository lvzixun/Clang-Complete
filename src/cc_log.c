#include <stdio.h>
#include <stdarg.h>

#define LOG_FILE "t.log"

void
cc_printf(const char* s, ...) {
	FILE* fp = fopen(LOG_FILE, "w+");
	va_list args;
	va_start(args, s);
	vfprintf(fp, s, args);
	fprintf(fp, "\n");
	va_end(args);
	fclose(fp);
}