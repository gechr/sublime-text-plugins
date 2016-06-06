import sublime_plugin

class DuplicateCommand(sublime_plugin.TextCommand):
    def run(self, edit, count=1):
        for _ in range(count):
            for region in self.view.sel():
                if region.empty():
                    line = self.view.line(region)
                    line_contents = self.view.substr(line) + '\n'
                    self.view.insert(edit, line.begin(), line_contents)
                else:
                    self.view.insert(edit, region.begin(), self.view.substr(region) + '\n')

class DuplicateCountCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Duplicate Count:', '', self.on_done, None, None)

    def on_done(self, text):
        try:
            duplicate_count = int(text)
            if self.window.active_view():
                self.window.active_view().run_command('duplicate', {'count': duplicate_count})
        except ValueError:
            pass
