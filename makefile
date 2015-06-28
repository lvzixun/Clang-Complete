UNAME_S := $(shell uname -s)

CLANG = "$(PWD)/lib"

# mac os x
ifeq ($(UNAME_S), Darwin)
	CC = clang
	CFLAGS = -g -Wall
	LIB_FLAG = -Wl,-rpath,@loader_path/.
	ST3 = ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Clang-Complete
	LIBCC = lib/libcc.so
endif

# linux
ifeq ($(UNAME_S), Linux)
	CC = gcc
	CFLAGS = -g -Wall -fPIC
	ST3 = ~/.config/sublime-text-3/Packages/Clang-Complete
	LIBCC = lib/libcc.so
endif

# windows (mingw)
ifeq ($(OS),Windows_NT)
	CLANG = "$(CURDIR)/lib"
	CC = gcc
	CFLAGS = -g -Wall
	LIBCC = lib/libcc.dll
endif


FILES = \
src/cc_result.c \
src/cc_resultcache.c \
src/cc_symbol.c \
src/cc_trie.c \
src/py_bind.c


all: cc_lib


linux: linux_config cc_lib

linux_config:
	sudo apt-get install clang
	sudo ln -sf /usr/lib/llvm-3.5/lib/libclang-3.5.so.1 ./lib/libclang.so

cc_lib: $(FILES)
	$(CC) -shared -o $(LIBCC)  $(CFLAGS) $^ -L$(CLANG) $(LIB_FLAG) -I$(CLANG)/include  -lclang

link:
	ln -s $(PWD) $(ST3)

##  for test
cc: cc_lib
	$(CC) -o cc test/test_cc.c -I$(CLANG)/include  $(LIBCC)

trie: src/cc_trie.c test/test_trie.c test/token.h
	$(CC) -o trie $(CFLAGS) src/cc_trie.c test/test_trie.c



.PHONY : clean
clean:
	rm  -f $(ST3)
	rm  -f cc
	rm  -f tt
	rm  -rf src/*.o
	rm  -rf $(LIBCC)
	rm  -f tcc
