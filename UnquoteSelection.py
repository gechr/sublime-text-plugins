import sublime, sublime_plugin


class UnquoteSelectionCommand(sublime_plugin.TextCommand):

    QUOTE_CHARS = ("'", '"', "`")

    def run(self, edit):
        view = self.view
        for region in view.sel():
            if region.empty():
                region = self.view.word(region.a)
            selection = view.substr(region)
            if self._is_quoted(selection):
                begin, end = region.begin(), region.end()
                view.erase(edit, sublime.Region(end - 1, end))
                view.erase(edit, sublime.Region(begin, begin + 1))

    def _is_quoted(self, text):
        return len(text) > 2 and any(
            [q for q in self.QUOTE_CHARS if text.startswith(q) and text.endswith(q)]
        )
