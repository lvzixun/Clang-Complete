#include <clang-c/Index.h>
#include <stdio.h>

#include "cc_symbol.h"
#include "cc_result.h"


#if _WIN32
    #if _MSC_VER
       #define snprintf _snprintf_s
    #endif
    #define EXPORT __declspec(dllexport)
#else
   #define EXPORT
#endif
#if __MINGW32__
    #define MINGWSUPPORT __attribute__ ((callee_pop_aggregate_return(0)))
#else
    #define MINGWSUPPORT
#endif



EXPORT struct cc_symbol* 
py_symbol_new(const char* filename, const char* opt[], unsigned int opt_len, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files) {
  void* p = cc_symbol_new(filename, opt, opt_len, unsaved_files, num_unsaved_files);
  return p;
}

EXPORT void
py_symbol_free(struct cc_symbol* sp) {
  cc_symbol_free(sp);
}

EXPORT void
py_symbol_reparse(struct cc_symbol* sp, struct CXUnsavedFile*  unsaved_files, unsigned num_unsaved_files) {
  cc_symbol_reparse(sp, unsaved_files, num_unsaved_files);
}

EXPORT struct cc_result* 
py_symbol_complete_at(struct cc_symbol* sp, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files) {
  struct cc_result* ret = cc_symbol_complete_at(sp, line, col, unsaved_files, num_unsaved_files);
  return ret;
}

EXPORT void
py_result_free(struct cc_result* rp) {
  cc_result_free(rp);
}

EXPORT struct match_result
py_result_match(struct cc_result* rp, const char* prefix) {
  // printf("py_result_match: %p prefix: %s\n", rp, prefix);
  struct match_result ret = cc_result_match(rp, prefix);
  // cc_result_dump(rp, ret);  // for test
  return ret;
}

EXPORT const char*
py_cs_entryname(CXCompletionString cs) {
  return cc_result_entryname(cs);
}

EXPORT unsigned int
py_cs_count(CXCompletionString cs) {
  return clang_getNumCompletionChunks(cs);
}

struct cc_trunk {
  enum CXCompletionChunkKind kind;
  const char* value;
};

EXPORT struct cc_trunk
py_cs_trunk(CXCompletionString cs, unsigned int idx) {
  struct cc_trunk trunk = {
    .kind = clang_getCompletionChunkKind(cs, idx),
    .value = NULL,
  };

  CXString str = clang_getCompletionChunkText(cs, idx);
  trunk.value = clang_getCString(str);
  return trunk;
}


EXPORT CXDiagnosticSet
py_diagnostic_new(struct cc_symbol* sp) {
  CXDiagnosticSet set = clang_getDiagnosticSetFromTU(cc_symbol_tu(sp));
  return set;
}

EXPORT void
py_diagnostic_free(CXDiagnosticSet set) {
  clang_disposeDiagnosticSet(set);
}


EXPORT unsigned int
py_diagnostic_num(CXDiagnosticSet set) {
  return clang_getNumDiagnosticsInSet(set);
}


EXPORT const char*
py_diagnostic(CXDiagnosticSet set, unsigned int idx) {
  CXDiagnostic c = clang_getDiagnosticInSet(set, idx);
  CXString cs = clang_formatDiagnostic(c, CXDiagnostic_DisplaySourceLocation | CXDiagnostic_DisplayColumn);
  return clang_getCString(cs);
}

EXPORT struct cc_def
py_symbol_def(struct cc_symbol* sp, const char* filename, unsigned line, unsigned col) {
	struct cc_def ret = {
		.filename = "",
		.line = 0,
		.col = 0,
	};

	cc_symbol_def(sp, filename, line, col, &ret);
	return  ret;
}


