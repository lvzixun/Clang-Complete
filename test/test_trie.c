#include "../src/cc_trie.h"
#include "token.h"

#include <stdio.h>
#include <assert.h>

#define _len      (sizeof(tokens) / sizeof(tokens[0]))
#define _idx2s(idx) (tokens[idx])

void func(unsigned int idx, void* ud) {
  printf("[%d] %s\n", idx, _idx2s(idx));
}


int main(int argc, char const *argv[]) {
  struct cc_trie* tp = cc_trie_new();

  int i;
  for(i=0; i<_len; i++) {
    const char* s = _idx2s(i);
    printf("insert [%d] %s\n", i, s);
    cc_trie_insert(tp, s, i);
  }

  printf("trie size: %ld M\n", cc_trie_size(tp) / 1024 / 1024);
  // trie_dump(tp);

  while(true) {
    char buf[64] = {0};
    printf("\n input prefix:");
    gets(buf);
    printf("\n\n*********  match: %s\n", buf);
    cc_trie_match(tp, buf, func, NULL);  
  }
  // assert(argc >= 1 && argv[1]);
  // printf("\n\n*********  match: %s\n", argv[1]);
  // cc_trie_match(tp, argv[1], func, NULL);

  cc_trie_free(tp);
  return 0;
}