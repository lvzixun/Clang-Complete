#ifndef _CC_TRIE_H_
#define _CC_TRIE_H_

#include <string.h>
#include <stdbool.h>
struct cc_trie;

typedef void (*trie_visit)(unsigned int v, void* ud);

struct cc_trie* cc_trie_new();
void cc_trie_free(struct cc_trie* tp);
void cc_trie_clear(struct cc_trie* tp);
void cc_trie_insert(struct cc_trie* tp, const char* str, unsigned int ud);
void cc_trie_match(struct cc_trie* tp, const char* prefix, trie_visit func, void* ud);

size_t cc_trie_size(struct cc_trie* tp);
void trie_dump(struct cc_trie* tp);
#endif