#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "cc_trie.h"

#include <stdio.h>

#define _CHAR_COUNT 63
static int _char2pos[] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0,
  0, 0, 0, 0, 0, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
  53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 0, 0, 0, 0, 1, 0, 12, 13, 14,
  15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
  35, 36, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static int idx2char[] = {
  '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
  'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
  'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
  'W', 'X', 'Y', 'Z',
};


#define c2idx(c) (assert(((unsigned char)c)>=0 && ((unsigned char)c)<=0xff), _char2pos[(unsigned char)c]-1)
#define pos2node(tp, node_pos) ( (assert(node_pos>0 && tp->pool.pos>=(node_pos)), &(tp->pool.p[(node_pos)-1])) )

struct cc_node {
  struct {
    unsigned int* p;
    unsigned int tmp;
    uint32_t pos;
    uint32_t len;
  }ud_slot;

  uint8_t list[_CHAR_COUNT];
  uint8_t count;

  uint32_t childs[_CHAR_COUNT];
};

struct cc_trie {
  struct {
    struct cc_node* p;
    uint32_t pos;
    uint32_t size;
  }pool;

  uint32_t root;
};

#define DEF_POOL_SIZE 8

static uint32_t pool_get(struct cc_trie* tp);
static uint32_t node_insert(struct cc_trie* tp, uint32_t node_pos, char c);

static struct cc_node* node_next(struct cc_trie* tp, struct cc_node* node, char c);
static inline void node_init();

struct cc_trie* 
cc_trie_new() {
  int i;
  struct cc_trie* tp = (struct cc_trie*)malloc(sizeof(*tp));
  tp->pool.p = (struct cc_node*)malloc(DEF_POOL_SIZE*sizeof(struct cc_node));
  tp->pool.pos = 0;
  tp->pool.size = DEF_POOL_SIZE;
  for(i=0; i<DEF_POOL_SIZE; i++) {
    struct cc_node* node = tp->pool.p + i;
    node_init(node);
  }

  tp->root = pool_get(tp);
  return tp;
}

static inline void
node_init(struct cc_node* node) {
  node->ud_slot.p = NULL;
  node->ud_slot.tmp = 0;
  node->ud_slot.len = 1;
  node->ud_slot.pos = 0;
}

static void
node_addud(struct cc_node* node, unsigned int ud) {
  if(node->ud_slot.pos==0) {
    if(node->ud_slot.p == NULL) {
      node->ud_slot.tmp = ud;
      node->ud_slot.pos++;
      return;
    }
  }else if(node->ud_slot.p == NULL) {
    assert(node->ud_slot.pos == 1 && node->ud_slot.len == 1);
    node->ud_slot.p = (unsigned int*)malloc(sizeof(unsigned int)*2);
    node->ud_slot.p[0] = node->ud_slot.tmp;
    node->ud_slot.len = 2;
  }

  if(node->ud_slot.pos >= node->ud_slot.len) {
    assert((node->ud_slot.len & 0x80000000) == 0); // check overflow
    uint32_t sz = node->ud_slot.len * 2;
    node->ud_slot.p = (unsigned int*)realloc(node->ud_slot.p, sizeof(unsigned int)*sz);
    node->ud_slot.len = sz;
  }

   node->ud_slot.p[node->ud_slot.pos] = ud;
   (node->ud_slot.pos)++;
}


void
cc_trie_free(struct cc_trie* tp) {
  uint32_t i;
  for(i=0; i<tp->pool.size; i++) {
    struct cc_node* node = tp->pool.p + i;
    if(node->ud_slot.p) {
      free(node->ud_slot.p);
    }
  }
  free(tp->pool.p);
  free(tp);
}

void
cc_trie_clear(struct cc_trie* tp) {
  tp->pool.pos = 0;
  tp->root = pool_get(tp);
}


void
cc_trie_insert(struct cc_trie* tp, const char* str, unsigned int ud) {
  if(str == NULL) return;

  char c;
  uint32_t cur_pos = tp->root;
  for(; (c=*str++); ) {
    if(c2idx(c) >= 0){
      cur_pos = node_insert(tp, cur_pos, c);
    }
  }

  struct cc_node* node = pos2node(tp, cur_pos);
  node_addud(node, ud);
}

static void
_dump_node(struct cc_trie* tp, struct cc_node* root, trie_visit func, void* ud) {
  int i;
   for(i=0; i<root->ud_slot.pos; i++) {
    unsigned int *p = root->ud_slot.p;
    unsigned int v  = (p)?(p[i]):(root->ud_slot.tmp);
    func(v, ud);
   }

  for(i=0; i<root->count; i++){
    int idx = root->list[i];
    struct cc_node* next = pos2node(tp, root->childs[idx]);
    _dump_node(tp, next, func, ud);
  }
}

void
cc_trie_match(struct cc_trie* tp, const char* prefix, trie_visit func, void* ud) {
  char c;
  struct cc_node* cur = pos2node(tp, tp->root);
  for(; (prefix && (c=*prefix++)); ) {
    struct cc_node* next = node_next(tp, cur, c);
    if(!next) return;
    cur = next;
  }

  // dump
  _dump_node(tp, cur, func, ud);
}


static uint32_t
pool_get(struct cc_trie* tp) {
  size_t sz = tp->pool.size;
  if(tp->pool.pos >= sz) {
    size_t i;
    assert((tp->pool.size & 0x80000000) == 0);  // is overflow
    tp->pool.size *= 2;
    tp->pool.p = (struct cc_node*)realloc(tp->pool.p, sizeof(struct cc_node)*tp->pool.size);
    for(i=sz; i<tp->pool.size; i++) {
      struct cc_node* node = tp->pool.p + i;
      node_init(node);
    }
  }

  struct cc_node* node = &(tp->pool.p[tp->pool.pos]);
  memset(node->childs, 0, sizeof(node->childs));
  node->count = 0;
  node->ud_slot.pos = 0;
  return ++(tp->pool.pos);
}

static struct cc_node* 
node_next(struct cc_trie* tp, struct cc_node* node, char c) {
  int idx = c2idx(c);
  if(idx<0) return NULL;

  uint32_t pos = node->childs[idx];
  if(pos == 0) return NULL;

  return pos2node(tp, pos);
}

static uint32_t
node_insert(struct cc_trie* tp, uint32_t node_pos, char c) {
  struct cc_node* node = pos2node(tp, node_pos);
  int idx = c2idx(c);

  uint32_t pos = node->childs[idx];
  if(pos == 0){
    pos = pool_get(tp);
    node = pos2node(tp, node_pos);
    node->childs[idx] = pos;
    assert(node->count < _CHAR_COUNT);
    node->list[node->count++] = idx;
  }
  return pos;
}


// for test
static void
_tdump(struct cc_trie* tp, struct cc_node* node, uint32_t pos) {
  printf("pos[%d] count[%d] ud_p[%p] ud_pos[%d] ud_len[%d]\n", pos, node->count, 
    node->ud_slot.p, node->ud_slot.pos, node->ud_slot.len);
  int i=0;
  for(i=0; i<node->count; i++) {
    int idx = node->list[i];
    printf("  %c -> pos[%d]\n", idx2char[idx], node->childs[idx]);
  }

  for(i=0; i<node->count; i++) {
    int idx = node->list[i];
    uint32_t pos = node->childs[idx];
    _tdump(tp, pos2node(tp, pos), pos);
  }
}

void
trie_dump(struct cc_trie* tp) {
  _tdump(tp, pos2node(tp, tp->root), tp->root);
}



