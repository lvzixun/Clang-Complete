CC = clang 
OUT = cc
CFLAGS = -g -Wall

CLANG = $(PWD)/lib
ST3 = ~/Library/Application\ Support/Sublime\ Text\ 3/Packages

FILES = \
src/cc_result.c \
src/cc_resultcache.c \
src/cc_symbol.c \
src/cc_trie.c \
src/py_bind.c


all: cc_lib

cc_lib: $(FILES)
	$(CC) -shared -o lib/libcc.so $(CFLAGS) $^ -L$(CLANG) -rpath $(CLANG) -I$(CLANG)/include  -lclang

install:
	ln -s $(PWD) $(ST3)/Clang-Complete

cc: cc_lib
	clang -o cc test/test_cc.c libcc.so

trie: src/cc_trie.c test/test_trie.c test/token.h
	$(CC) -o trie $(CFLAGS) src/cc_trie.c test/test_trie.c

tcc: clang_complete.c
	$(CC) -o $@ $(CFLAGS) $^ -L$(CLANG) -rpath $(CLANG) -lclang


.PHONY : clean
clean:
	rm $(ST3)/cc
	rm  -f cc
	rm  -f tt
	rm  -rf src/*.o
	rm  -rf *.so
	rm  -rf lib/*.so
	rm  -f tcc