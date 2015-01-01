from ctypes import cdll, Structure, POINTER, c_char_p, c_void_p, c_uint, c_bool, c_ulong
from ctypes import c_char_p
from ctypes import py_object
import os

current_path = os.path.dirname(os.path.abspath(__file__))
libcc = cdll.LoadLibrary('%s/../libcc.so' % current_path)


class _CXUnsavedFile(Structure):
    _fields_ = [("name", c_char_p), ("contents", c_char_p), ('length', c_ulong)]

class _cc_symbol(Structure):
  pass

class _cc_result(Structure):
  pass

class _CXCompletionResult(Structure):
  pass


class match_result(Structure):
  _fields_ = [("table", POINTER(POINTER(_CXCompletionResult))), ("size", c_uint)]

  @property
  def length(self):
    return self.__len__()

  def __len__(self):
    return self.size

  def __getitem__(self, key):
    if key >= self.length:
      raise IndexError
      return 'todo getitem'


libcc_symbol_new = libcc.py_symbol_new
libcc_symbol_new.restype = POINTER(_cc_symbol)
libcc_symbol_new.argtypes = [c_char_p, POINTER(c_char_p), c_uint, POINTER(_CXUnsavedFile), c_uint]

libcc_symbol_free = libcc.py_symbol_free
libcc_symbol_free.argtypes = [POINTER(_cc_symbol)]

libcc_symbol_reparse = libcc.py_symbol_reparse
libcc_symbol_reparse.argtypes = [POINTER(_cc_symbol), POINTER(_CXUnsavedFile), c_uint]

libcc_symbol_complete_at = libcc.py_symbol_complete_at
libcc_symbol_complete_at.restype = POINTER(_cc_result)
libcc_symbol_complete_at.argtypes = [POINTER(_cc_symbol), c_uint, c_uint, POINTER(_CXUnsavedFile), c_uint]

libcc_result_free = libcc.py_result_free
libcc_result_free.argtypes = [POINTER(_cc_result)]

libcc_result_match = libcc.py_result_match
libcc_result_match.restype = match_result
libcc_result_match.argtypes = [POINTER(_cc_result), c_char_p]


class bind_helper(object):
  def to_string_list(self, str_list):
    result = (c_char_p * len(str_list))()
    result[:] = [x.encode("utf-8") for x in str_list]
    return result, len(str_list)

  def to_file_list(self, file_list):
    result = (_CXUnsavedFile * len(file_list))()
    for i, (name, value) in enumerate(file_list):
      result[i].name = name
      result[i].contents = value
      result[i].length = len(value)
    return result, len(file_list)


class cc_result(object):
  def __init__(self, c_obj):
    self.c_obj = c_obj

  def __del__(self):
    libcc_result_free(self.c_obj)

  def match(self, prefix):
    return libcc_result_match(self.c_obj, prefix)


class cc_symbol(object):
  def __init__(self, filename, opt, unsaved_files):
    self.helper = bind_helper()
    opt, opt_len = self.helper.to_string_list(opt)
    unsaved_files, num = self.helper.to_file_list(unsaved_files)
    self.c_obj = libcc_symbol_new(filename, opt, opt_len, unsaved_files, num)

  def __del__(self):
    libcc_symbol_free(self.c_obj)

  def complete_at(self, line, col, unsaved_files):
    unsaved_files, num = self.helper.to_file_list(unsaved_files)
    c_result_obj = libcc_symbol_complete_at(self.c_obj, line, col, unsaved_files, num)
    return cc_result(c_result_obj)

  def reparse(self, unsaved_files):
    unsaved_files, num = self.helper.to_file_list(unsaved_files)
    libcc_symbol_reparse(self.c_obj, unsaved_files, num)



def main():
  opt = [
    "-Wall",
  ]
  unsaved_files = []
  symbol = cc_symbol("t.c", opt, unsaved_files)
  result = symbol.complete_at(18, 3, unsaved_files)
  ret = result.match("__")


if __name__ == '__main__':
  main()


