#include <clang-c/Index.h>
#include <stdlib.h>
#include <string.h>

#include "cc_symbol.h"
#include "cc_result.h"

struct cc_symbol {
  CXTranslationUnit tu;
  char* filename;
};



#define _PARSE_OPTIONS  CXTranslationUnit_DetailedPreprocessingRecord |  \
                        CXTranslationUnit_IncludeBriefCommentsInCodeCompletion | \
                        CXTranslationUnit_Incomplete |  \
                        CXTranslationUnit_PrecompiledPreamble |  \
                        CXTranslationUnit_CacheCompletionResults


struct cc_symbol* 
cc_symbol_create(const char* filename, const char* opt[], int opt_len, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files) {
  struct cc_symbol* ret = (struct cc_symbol*)malloc(sizeof(*ret));
  CXIndex index = clang_createIndex(1, 0);
  ret->tu =  clang_parseTranslationUnit(index, filename, opt, opt_len, unsaved_files, num_unsaved_files, _PARSE_OPTIONS);
  ret->filename = strdup(filename);
  return ret;
}


void 
cc_symbol_free(struct cc_symbol* sp) {
  clang_disposeTranslationUnit(sp->tu);
  free(sp->filename);
  free(sp);
}


int 
cc_symbol_reparse(struct cc_symbol* sp, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files) {
  return clang_reparseTranslationUnit(sp->tu, num_unsaved_files, unsaved_files, _PARSE_OPTIONS);
}


void
cc_symbol_diagnostic(struct cc_symbol* sp, diagnostic_visit func, void* ud) {
  CXDiagnosticSet set = clang_getDiagnosticSetFromTU(sp->tu);
  unsigned num = clang_getNumDiagnosticsInSet(set);
  unsigned i;
  for(i=0; i<num; i++) {
    CXDiagnostic c = clang_getDiagnosticInSet(set, i);
    CXString cs = clang_formatDiagnostic(c, CXDiagnostic_DisplaySourceLocation | CXDiagnostic_DisplayColumn);
    func(clang_getCString(cs), ud);
  }
  clang_disposeDiagnosticSet(set);
}


struct cc_result*
cc_symbol_complete_at(struct cc_symbol* sp, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files) {
  return cc_reslut_create(sp->tu, sp->filename, line, col, unsaved_files, num_unsaved_files);
}



