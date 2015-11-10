import sublime_plugin

class ToggleRulersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.settings().get("rulers") == []:
            self.view.settings().set("rulers", range(4, 200, 4))
        else:
            self.view.settings().set("rulers", [])
