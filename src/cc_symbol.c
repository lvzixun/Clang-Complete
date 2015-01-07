#include <stdio.h>
#include <clang-c/Index.h>
#include <stdlib.h>
#include <string.h>

#include "cc_symbol.h"
#include "cc_result.h"
#include "cc_trie.h"
#include "cc_resultcache.h"

struct cc_symbol {
  CXTranslationUnit tu;
  char* filename;

  struct cc_trie* tp;
  struct cc_resultcache* cache;
};



#define _PARSE_OPTIONS  CXTranslationUnit_DetailedPreprocessingRecord |  \
                        CXTranslationUnit_IncludeBriefCommentsInCodeCompletion | \
                        CXTranslationUnit_Incomplete |  \
                        CXTranslationUnit_PrecompiledPreamble |  \
                        CXTranslationUnit_CacheCompletionResults


struct cc_symbol* 
cc_symbol_new(const char* filename, const char* opt[], int opt_len, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files) {
  struct cc_symbol* ret = (struct cc_symbol*)malloc(sizeof(*ret));
  CXIndex index = clang_createIndex(1, 0);
  ret->tu =  clang_parseTranslationUnit(index, filename, opt, opt_len, unsaved_files, num_unsaved_files, _PARSE_OPTIONS);
  ret->filename = strdup(filename);

  ret->tp = cc_trie_new();
  ret->cache = cc_resultcache_new();
  return ret;
}

CXTranslationUnit
cc_symbol_tu(struct cc_symbol* sp) {
  return sp->tu;
}

void 
cc_symbol_free(struct cc_symbol* sp) {
  clang_disposeTranslationUnit(sp->tu);
  cc_trie_free(sp->tp);
  cc_resultcache_free(sp->cache);

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
  return cc_result_new(sp->tu, sp->tp, sp->cache, sp->filename, line, col, unsaved_files, num_unsaved_files);
}


bool
cc_symbol_def(struct cc_symbol* sp, const char* file_name, unsigned int line, unsigned int col, struct cc_def* out_def) {
  CXSourceLocation location = clang_getLocation(sp->tu, clang_getFile(sp->tu, file_name), line, col);
  CXCursor cursor = clang_getCursor(sp->tu, location);
  CXCursor def_cursor = clang_getCursorDefinition(cursor);
  if(clang_Cursor_isNull(def_cursor)) {
    def_cursor = clang_getCursorReferenced(cursor);
    if(clang_Cursor_isNull(def_cursor)) return false;
  }

  CXSourceLocation def_location = clang_getCursorLocation(def_cursor);
  CXFile def_f = NULL;
  unsigned def_line, def_col, offset;

  clang_getSpellingLocation(def_location, &def_f, &def_line, &def_col, &offset);
  out_def->filename = clang_getCString(clang_getFileName(def_f));
  out_def->line = def_line;
  out_def->col = def_col;

  return  true;
}
