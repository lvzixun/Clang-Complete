#ifndef _CC_RESULTCACHE_H_
#define _CC_RESULTCACHE_H_

#include <clang-c/Index.h>

struct cc_resultcache;

struct cc_resultcache* cc_resultcache_new();
void cc_resultcache_clear(struct cc_resultcache* cache);
void cc_resultcache_free(struct cc_resultcache* cache);
CXCompletionResult** cc_resultcache_head(struct cc_resultcache* cache);
size_t cc_resultcache_pos(struct cc_resultcache* cache);
CXCompletionResult** cc_resultcache_get(struct cc_resultcache* cache);

#endif