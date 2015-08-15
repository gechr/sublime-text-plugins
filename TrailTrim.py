import sublime_plugin

class TrailTrimCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        trailing = self.view.find_all("[\t ]+$")
        trailing.reverse()

        for r in trailing:
            for r2 in self.view.sel():
                if r2.empty() and r.contains(r2):
                    self.view.erase(edit, r)
                else:
                    self.view.erase(edit, r2.intersection(r))
