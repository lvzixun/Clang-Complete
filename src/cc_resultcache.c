#include <stdlib.h>
#include <assert.h>
#include <clang-c/Index.h>


struct cc_resultcache {
  CXCompletionResult** p;
  size_t pos;
  size_t size;
};

#define DEF_CACHE_SIZE 8

struct cc_resultcache*
cc_resultcache_new() {
  struct cc_resultcache* ret = (struct cc_resultcache*)malloc(sizeof(*ret));
  ret->p = (CXCompletionResult**)malloc(DEF_CACHE_SIZE * sizeof(CXCompletionResult*));
  ret->pos = 0;
  ret->size = DEF_CACHE_SIZE;

  return ret;
}


void
cc_resultcache_clear(struct cc_resultcache* cache) {
  cache->pos = 0;
}

void
cc_resultcache_free(struct cc_resultcache* cache) {
  free(cache->p);
  free(cache);
}

CXCompletionResult**
cc_resultcache_head(struct cc_resultcache* cache) {
  return cache->p;
}

size_t
cc_resultcache_pos(struct cc_resultcache* cache) {
  return cache->pos;
}

CXCompletionResult**
cc_resultcache_get(struct cc_resultcache* cache) {
  if(cache->pos >= cache->size) {
    cache->size *= 2;
    cache->p = (CXCompletionResult**)realloc(cache->p, sizeof(CXCompletionResult*)*cache->size);
  }

  return &(cache->p[cache->pos++]);
}
