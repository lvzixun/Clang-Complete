CC = clang 
OUT = cc
CFLAGS = -g -Wall

FILES = \
src/cc_result.c \
src/cc_resultcache.c \
src/cc_symbol.c \
src/cc_trie.c \
src/py_bind.c


all: cc_lib

cc_lib: $(FILES)
	$(CC) -shared -o libcc.so $(CFLAGS) -Wl,-undefined,dynamic_lookup $^ -L/usr/local/opt/llvm/lib -lclang

cc: cc_lib
	clang -o cc test/test_cc.c libcc.so

trie: src/cc_trie.c test/test_trie.c test/token.h
	gcc -o trie $(CFLAGS) src/cc_trie.c test/test_trie.c

test: clang_complete.c
	clang -o test -g -Wall clang_complete.c -L/usr/local/opt/llvm/lib -lclang


.PHONY : clean
clean:
	rm cc
	rm test
	rm -rf src/*.o
	rm *.so