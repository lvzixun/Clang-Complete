#ifndef _CC_SYMBOL_H_
#define _CC_SYMBOL_H_

#include <clang-c/Index.h>
#include "cc_result.h"

typedef void(*diagnostic_visit)(const char* info, void* ud);

struct cc_symbol* cc_symbol_new(const char* filename, const char* opt[], int opt_len, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files);
void cc_symbol_free(struct cc_symbol* sp);
int cc_symbol_reparse(struct cc_symbol* sp, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files);
void cc_symbol_diagnostic(struct cc_symbol* sp, diagnostic_visit func, void* ud);
struct cc_result* cc_symbol_complete_at(struct cc_symbol* sp, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files);

#endif
