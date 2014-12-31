#ifndef _CC_RESULT_H_
#define _CC_RESULT_H_

#include <clang-c/Index.h>

struct match_reslut {
  CXCompletionResult** table;
  unsigned int size;
};

struct cc_result;

struct cc_result* cc_reslut_create(CXTranslationUnit tu, const char* filename, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files);
void cc_reslut_free(struct cc_result* rt);

struct match_reslut cc_reslut_match(struct cc_result* rt, const char* prefix);

#endif