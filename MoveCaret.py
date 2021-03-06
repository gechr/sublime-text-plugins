import sublime, sublime_plugin


class MoveCaretDownCommand(sublime_plugin.TextCommand):
    def run(self, edit, nlines):
        (row, col) = self.view.rowcol(self.view.sel()[0].begin())
        target = self.view.text_point(row + nlines, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)


class MoveCaretUpCommand(sublime_plugin.TextCommand):
    def run(self, edit, nlines):
        (row, col) = self.view.rowcol(self.view.sel()[0].begin())
        target = self.view.text_point(row - nlines, col)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)
