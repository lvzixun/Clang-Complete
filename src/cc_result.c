#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

#include "cc_resultcache.h"
#include "cc_trie.h"
#include "cc_result.h"


struct cc_result {
  CXCodeCompleteResults* result;

  struct cc_trie* ref_tp;             // the struct cc_trie reference, not need free
  struct cc_resultcache* ref_cache;   // the struct ccresultcache reference, not need free
};

#define _COMPLETE_OPTIONS CXCodeComplete_IncludeMacros | \
                          CXCodeComplete_IncludeCodePatterns | \
                          CXCodeComplete_IncludeBriefComments


static void _insert(struct cc_result* rp, unsigned int entry_idx);


struct cc_result* 
cc_result_new(CXTranslationUnit tu, struct cc_trie* tp, struct cc_resultcache* cache, const char* filename, unsigned int line, unsigned int col, struct CXUnsavedFile* unsaved_files, unsigned int num_unsaved_files) {
  unsigned int i;
  CXCodeCompleteResults* result = clang_codeCompleteAt(tu, filename, line, col, unsaved_files, num_unsaved_files, _COMPLETE_OPTIONS);
  struct cc_result* rp = (struct cc_result*)malloc(sizeof(*rp));

  cc_trie_clear(tp);
  rp->result = result;
  rp->ref_cache = cache;
  rp->ref_tp = tp;

  for(i=0; i<result->NumResults; i++) {
    _insert(rp, i);
  }
  return rp;
}


void 
cc_result_free(struct cc_result* rp) {
  clang_disposeCodeCompleteResults(rp->result);
  free(rp);
}


const char*
cc_result_entryname(CXCompletionString cs) {
  int num = clang_getNumCompletionChunks(cs);
  if(clang_getCompletionAvailability(cs) == CXAvailability_Available && num >= 1) {
    int i;
    for(i=0; i<num; i++) {
      int type = clang_getCompletionChunkKind(cs, i);
      if(type == CXCompletionChunk_TypedText){
        CXString str = clang_getCompletionChunkText(cs, i);
        return clang_getCString(str);
      }
    }
    return NULL;
  }else {
    return NULL;
  }
}


static void
_insert(struct cc_result* rp, unsigned int entry_idx) {
  assert(entry_idx < rp->result->NumResults);
  CXCompletionResult* entry = &rp->result->Results[entry_idx];
  CXCompletionString cs = entry->CompletionString;
  const char* str = cc_result_entryname(cs);
  if (str) {
    // printf("%s\n", str);
    cc_trie_insert(rp->ref_tp, str, entry_idx);
  }
}


static void
_visit_func(unsigned int v, void* ud) {
  struct cc_result* rp = (struct cc_result*)ud;
  CXCompletionResult** p = cc_resultcache_get(rp->ref_cache);
  assert(v < rp->result->NumResults);
  *p = &(rp->result->Results[v]);
}


struct match_result
cc_result_match(struct cc_result* rp, const char* prefix) {
  struct match_result ret = {0};

  cc_resultcache_clear(rp->ref_cache);
  cc_trie_match(rp->ref_tp, prefix, _visit_func, rp);
  ret.table = cc_resultcache_head(rp->ref_cache);
  ret.size = cc_resultcache_pos(rp->ref_cache);
  return ret;
}



// for test
void
cc_result_dump(struct cc_result* rp,  struct match_result result) {
  unsigned int i;

  printf("*************  match *************\n");
  for(i=0; i<result.size; i++) {
    CXCompletionResult* item = result.table[i];
    CXCompletionString cs = item->CompletionString;
    printf("[%u] %s\n", i, cc_result_entryname(cs));
  }
}

