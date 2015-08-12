import threading
import re
import os
import sublime, sublime_plugin

from .clang_error import *
from .cc import *


language_regex = re.compile("(?<=source\.)[\w+#]+")
drivers = {
  "c++": "-xc++",
  "c": "-xc",
  "objc": "-ObjC",
  "objc++": "-ObjC++",
}

def get_unsaved_files(view):
  buffer = None
  if view.is_dirty():
      buffer = [(view.file_name(), view.substr(sublime.Region(0, view.size())))]
  return buffer

def get_language(view):
  caret = view.sel()[0].a
  language = language_regex.search(view.scope_name(caret))
  if language != None:
    language = language.group(0)
  return language


def can_complete(view):
  language = get_language(view)
  return language in drivers


class WraperComplete(object):

  def __init__(self):
    self._dispatch_map = {
      CXCursorKind.FIELD_DECL: self._field,

      CXCursorKind.FUNCTION_TEMPLATE: self._function,
      CXCursorKind.CXX_METHOD: self._function,
      CXCursorKind.FUNCTION_DECL: self._function,
      CXCursorKind.DESTRUCTOR: self._function,

      CXCursorKind.NAMESPACE: self._namespace,
      CXCursorKind.MACRO_DEFINITION: self._macro,
      CXCursorKind.NOT_IMPLEMENTED: self._not_implemented,
      CXCursorKind.VAR_DECL: self._var,
      CXCursorKind.ENUM_CONSTANT_DECL: self._var,


      CXCursorKind.PARM_DECL: self._var,
      CXCursorKind.TYPEDEF_DECL: self._typdef,

      CXCursorKind.CONSTRUCTOR: lambda v:self._struct(v, "constructor"),
      CXCursorKind.UNION_DECL: lambda v:self._struct(v, "union"),
      CXCursorKind.CLASS_TEMPLATE: lambda v:self._struct(v, "classTemplate"),
      CXCursorKind.CLASS_DECL: lambda v:self._struct(v, "class"),
      CXCursorKind.STRUCT_DECL: self._struct,
    }


  def get_entry(self, v):
    if v.kind in self._dispatch_map:
      func = self._dispatch_map[v.kind]
      return func(v)
    return self._unknow(v)


  def _unknow(self, v):
    print("unknow kind: ", v.kind, v.name)
    trigger, contents = self._attach(v)
    return (trigger, contents)



  def _attach(self, v, begin_idx=0):
    decl = ""
    contents = ""
    holder_idx = 1
    for i in range(begin_idx, v.length):
      trunk = v[i]
      value = trunk.value
      kind = trunk.kind
      if kind == CXCompletionChunkKind.Placeholder:
        value = "${%d:%s}" % (holder_idx, value)
        holder_idx += 1
      elif kind == CXCompletionChunkKind.Informative:
        value = ""
      contents += value
      decl += trunk.value
    return decl, contents


  def _typdef(self, v):
    _v, contents = self._attach(v)
    trigger = "%s\t%s" % (_v, "Typedef")
    return (trigger, contents)


  def _function(self, v):
    return_type = v[0].value
    func_decl, contents = self._attach(v, 1)
    trigger = "%s\t%s" % (func_decl, return_type)
    return (trigger, contents)


  def _not_implemented(self, v):
    _v, contents = self._attach(v)
    trigger = "%s\t%s" % (_v, "KeyWord")
    return (trigger, contents)

  def _namespace(self, v):
    macro, contents = self._attach(v)
    trigger = "%s\t%s" % (macro, "namespace")
    return (trigger, contents)

  def _macro(self, v):
    macro, contents = self._attach(v)
    trigger = "%s\t%s" % (macro, "Macro")
    return (trigger, contents)


  def _var(self, v):
    var = v.name
    var_type = v[0].value
    trigger = "%s\t%s" % (var, var_type)
    return (trigger, var)

  def _field(self, v):
    return self._var(v)


  def _struct(self, v, t="struct"):
    trigger = "%s\t%s" % (v.name, t)
    return (trigger, v.name)


class Complete(object):
  symbol_map = {}
  wraper = WraperComplete()
  member_regex = re.compile(r"(([a-zA-Z_]+[0-9_]*)|([\)\]])+)((\.)|(->)|(::))$")

  @staticmethod
  def clean():
    Complete.symbol_map = {}

  @staticmethod
  def get_settings():
    return sublime.load_settings("cc.sublime-settings")

  @staticmethod
  def get_opt(view):
    settings = Complete.get_settings()
    additional_lang_opts = settings.get("additional_language_options", {})
    language = get_language(view)
    project_settings = view.settings()
    include_opts = settings.get("include_options", []) + project_settings.get("cc_include_options", [])

    window = sublime.active_window()
    variables = window.extract_variables()
    include_opts = sublime.expand_variables(include_opts, variables)

    opt = [drivers[language]]
    if language in additional_lang_opts:
      for v in additional_lang_opts[language]:
        opt.append(v)

    for v in include_opts:
      opt.append(v)
    print("clang options: ", opt)
    return opt

  @staticmethod
  def is_inhibit():
    settings = Complete.get_settings()
    return settings.has("inhibit") and settings.get("inhibit") or False

  @staticmethod
  def get_symbol(file_name, view, unsaved_files=[]):
    self = Complete
    if file_name in self.symbol_map:
      return self.symbol_map[file_name]

    else:
      opt = self.get_opt(view)
      sym = CCSymbol(file_name, opt, unsaved_files)
      self.symbol_map[file_name] = sym
      return sym

  @staticmethod
  def del_symbol(file_name):
    self = Complete
    if file_name in self.symbol_map:
      del self.symbol_map[file_name]

  @staticmethod
  def is_member_completion(view):
    # fast check
    point = view.sel()[0].begin() - 1
    if point < 0:
      return False

    cur_char = view.substr(point)
    # print "cur_char:", cur_char
    if cur_char and cur_char != "." and cur_char != ">" and cur_char != ":" and cur_char != "[":
      return False

    caret= view.sel()[0].begin()
    line = view.substr(sublime.Region(view.line(caret).a, caret))
    return Complete.member_regex.search(line) != None


class ClangClean(sublime_plugin.TextCommand):
  def run(self, edit):
    if not can_complete(self.view):
      return

    Complete.clean()


class ClangGotoDef(sublime_plugin.TextCommand):
  def run(self, edit):
    if not can_complete(self.view):
      return

    filename = self.view.file_name()
    pos = self.view.sel()[0].begin()
    row, col = self.view.rowcol(pos)

    sym = Complete.get_symbol(filename, self.view)
    location = sym.get_def(filename, row+1, col+1)
    if location.has :
      # print(location.target)
      self.view.window().open_file(location.target, sublime.ENCODED_POSITION)
    else:
      sublime.status_message("Cant find definition")


class CCAutoComplete(sublime_plugin.EventListener):
  complete_result = None
  t = False
  dirty = False

  def on_modified(self, view):
    self.dirty = True
    if can_complete(view) and Complete.is_member_completion(view):
      self.per_complete()


  def per_complete(self):
    sublime.active_window().run_command("hide_auto_complete")
    def hack2():
      sublime.active_window().run_command("auto_complete",{
        'disable_auto_insert': True,
        'api_completions_only': Complete.is_inhibit(),
        'next_competion_if_showing': False
      })
    sublime.set_timeout(hack2, 1)


  def on_post_save_async(self, view):
    if not can_complete(view):
      return 

    settings = Complete.get_settings()
    hide_error_panel = settings.get('hide_error_panel') or False
    hide_error_mark = settings.get('hide_error_mark') or False
    file_name = view.file_name()
    sym = Complete.get_symbol(file_name, view)
    if self.dirty:
      sym.reparse()
    self.dirty = False
    digst = sym.diagnostic()
    
    output = "\n".join([err for _, (_, _, _, _, err) in digst])
    clang_error_panel.set_data(output)
    clang_error_panel.error_marks(view, digst, not hide_error_mark)

    if output:
      print(output)
    window = view.window()
    if not window is None and len(digst) >= 1:
      window.run_command("clang_toggle_panel", {"show": not hide_error_panel})

  
  def on_query_completions(self, view, prefix, locations):
    line, col = view.rowcol(locations[0])
    line += 1
    if len(prefix) == 0:
      col += 1

    file_name = view.file_name()

    if not can_complete(view) or file_name==None:
      return

    # flag = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
    flag = 0
    if self.complete_result != None:
      ret = None
      ret = (self.complete_result, flag)
      self.complete_result = None
      return ret

    elif not self.t or not self.t.is_alive():
      unsaved_files = get_unsaved_files(view)
      def do_complete():
        sym = Complete.get_symbol(file_name, view, unsaved_files)
        results = sym.complete_at(line, col, unsaved_files)
        complete = results.match(prefix)
        ret = []
        print("prefix: %s len:%d" % (prefix, len(complete)))
        for i, name, v in complete:
          entry = Complete.wraper.get_entry(v)
          # print("[%d] %s  %s" % (i, entry[1], v.kind))
          ret.append(entry)
        if len(ret) > 0:
          self.complete_result = ret
          self.per_complete()

      self.t = threading.Thread(target=do_complete)
      self.t.start()
      if prefix == "":
        return ([], flag)
      else:  
        return None

    else:
      print("complete busy!")
      return None
