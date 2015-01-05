#ifndef _CC_RESULT_H_
#define _CC_RESULT_H_

#include "cc_trie.h"
#include "cc_resultcache.h"
#include <clang-c/Index.h>

struct match_result {
  CXCompletionResult** table;
  unsigned int size;
};

struct cc_result;

struct cc_result* cc_result_new(CXTranslationUnit tu, struct cc_trie* tp, struct cc_resultcache* cache, const char* filename, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files);
void cc_result_free(struct cc_result* rp);

const char* cc_result_entryname(CXCompletionString cs);
struct match_result cc_result_match(struct cc_result* rp, const char* prefix);

void cc_result_dump(struct cc_result* rp,  struct match_result result);
#endif