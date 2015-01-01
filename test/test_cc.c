#include <clang-c/Index.h>
#include <stdio.h>

#include "../src/cc_symbol.h"
#include "../src/cc_result.h"


int main(int argc, char const *argv[]){
  const char* opt[] = {
    "-Wall",
  };

  struct cc_symbol* sp = cc_symbol_new("t.c", opt, 1, NULL, 0);

  struct cc_result* rp = cc_symbol_complete_at(sp, 18, 3, NULL, 0);

  struct match_result match_ret = cc_result_match(rp, "clang");
  cc_result_dump(rp, match_ret);  // for test

  cc_result_free(rp);
  cc_symbol_free(sp);
  return 0;
}