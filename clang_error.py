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
    markers = {'warning': 'comment', 'error': 'invalid', 'fatal error': 'invalid'}

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
            self.view = window.get_output_panel("cc")
            self.view.settings().set("result_file_regex", "^(..[^:\n]*):([0-9]+):?([0-9]+)?:? (.*)$")
            self.view.set_syntax_file('Packages/Clang-Complete/ErrorPanel.tmLanguage')
        self.flush()

        window.run_command("show_panel", {"panel": "output.cc"})

    def close(self):
        sublime.active_window().run_command("hide_panel", {"panel": "output.cc"})


    def error_marks(self, view, digst, display):
        self.erase_error_marks(view)

        cur_filename = view.file_name()
        outlines = {'warning': [], 'error': [], 'fatal error': []}
        for i, (filename, line, col, error_type, info) in digst:
            print(error_type, line)
            if error_type in outlines and cur_filename == filename:
                outlines[error_type].append(view.full_line(view.text_point(line-1, 0)))

        if display:
            for line_type in outlines:
                if not outlines[line_type] is None:
                    args = [
                        'sublimeclang-outlines-{0}'.format(line_type),
                        outlines[line_type],
                        self.markers[line_type],
                        'dot',
                        sublime.DRAW_OUTLINED
                    ]
                    view.add_regions(*args)


    def erase_error_marks(self, view):
        view.erase_regions('sublimeclang-outlines-error')
        view.erase_regions('sublimeclang-outlines-warning')
        view.erase_regions('sublimeclang-outlines-fatal error')


clang_error_panel = ClangErrorPanel()
