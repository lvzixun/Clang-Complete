CC = clang 
OUT = cc
CFLAGS = -g -Wall

CLANG = /usr/local/opt/llvm/lib

FILES = \
src/cc_result.c \
src/cc_resultcache.c \
src/cc_symbol.c \
src/cc_trie.c \
src/py_bind.c


all: cc_lib

cc_lib: $(FILES)
	$(CC) -shared -o libcc.so $(CFLAGS) -Wl,-undefined,dynamic_lookup $^ -L$(CLANG) -rpath $(CLANG)  -lclang

cc: cc_lib
	clang -o cc test/test_cc.c libcc.so

trie: src/cc_trie.c test/test_trie.c test/token.h
	$(CC) -o trie $(CFLAGS) src/cc_trie.c test/test_trie.c

tcc: clang_complete.c
	$(CC) -o $@ $(CFLAGS) $^ -L$(CLANG) -rpath $(CLANG) -lclang


.PHONY : clean
clean:
	rm tcc
	rm cc
	rm tt
	rm -rf src/*.o
	rm *.so