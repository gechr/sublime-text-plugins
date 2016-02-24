import sublime_plugin

class IncrementDecrement(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            old_value, new_value = self.view.substr(region), ''
            try:
                old_value = int(old_value)
                new_value = str(self.op(old_value))
            except ValueError:
                new_chars = []
                for char in old_value:
                    new_chars.append(chr(self.op(ord(char))))
                new_value = ''.join(new_chars)
            if new_value:
                self.view.replace(edit, region, new_value)

    def is_enabled(self):
        return len(self.view.sel()) > 0

class IncrementCommand(IncrementDecrement):
    def op(self, value):
        return value + 1

class DecrementCommand(IncrementDecrement):
    def op(self, value):
        return value - 1
