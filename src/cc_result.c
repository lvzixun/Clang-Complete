#include "cc_result.h"
#include <stdlib.h>


struct cc_result {
  CXCodeCompleteResults* result;

  CXCompletionResult** cahce;
  unsigned int pos;
  unsigned int size;

  // construct metch tree
};

#define _COMPLETE_OPTIONS CXCodeComplete_IncludeMacros | \
                          CXCodeComplete_IncludeCodePatterns | \
                          CXCodeComplete_IncludeBriefComments

struct cc_result* 
cc_reslut_create(CXTranslationUnit tu, const char* filename, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files) {
  CXCodeCompleteResults* result = clang_codeCompleteAt(tu, filename, line, col, unsaved_files, num_unsaved_files, _COMPLETE_OPTIONS);
  struct cc_result* rt = (struct cc_result*)malloc(sizeof(*rt));

  rt->result = result;
  rt->size = result->NumResults;
  rt->cahce = (CXCompletionResult**)calloc(1, sizeof(*rt->cahce) * rt->size);
  rt->pos = 0;

  return rt;
}


void 
cc_reslut_free(struct cc_result* rt) {
  clang_disposeCodeCompleteResults(rt->result);
  free(rt->cahce);
  free(rt);
}



// todo it
struct match_reslut
cc_reslut_match(struct cc_result* rt, const char* prefix) {
  struct match_reslut ret = {
    .table = rt->cahce,
    .size = rt->pos,
  };

  return ret;
}

