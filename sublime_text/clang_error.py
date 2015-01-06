import sublime, sublime_plugin


class ClangTogglePanel(sublime_plugin.WindowCommand):
    def run(self, **args):
        show = args["show"] if "show" in args else None

        if show or (show == None and not clang_error_panel.is_visible(self.window)):
            clang_error_panel.open(self.window)
        else:
            clang_error_panel.close()


class ClangErrorPanelFlush(sublime_plugin.TextCommand):
    def run(self, edit, data):
	    self.view.erase(edit, sublime.Region(0, self.view.size()))
	    self.view.insert(edit, 0, data)


def is_view_visible(view, window=None):
    ret = view != None and view.window() != None
    if ret and window:
        ret = view.window().id() == window.id()
    return ret

class ClangErrorPanel(object):
    def __init__(self):
        self.view = None
        self.data = ""

    def set_data(self, data):
        self.data = data
        if self.is_visible(): self.flush()

    def get_view(self):
        return self.view

    def is_visible(self, window=None):
        return is_view_visible(self.view, window)

    def set_view(self, view):
        self.view = view

    def flush(self):
        self.view.set_read_only(False)
        self.view.set_scratch(True)
        self.view.run_command("clang_error_panel_flush", {"data": self.data})
        self.view.set_read_only(True)

    def open(self, window=None):
        if window == None:
            window = sublime.active_window()
        if not self.is_visible(window):
            self.view = window.get_output_panel("clangcomplete")
            self.view.settings().set("result_file_regex", "^(..[^:\n]*):([0-9]+):?([0-9]+)?:? (.*)$")
            self.view.set_syntax_file('Packages/cc/ErrorPanel.tmLanguage')
        self.flush()

        window.run_command("show_panel", {"panel": "output.clangcomplete"})

    def close(self):
        sublime.active_window().run_command("hide_panel", {"panel": "output.clangcomplete"})


clang_error_panel = ClangErrorPanel()
