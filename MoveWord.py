import sublime, sublime_plugin

class WordMover(sublime_plugin.TextCommand):
    def move_word(self, edit, right):

        view = self.view
        sel  = view.sel()

        classes = sublime.CLASS_WORD_START | sublime.CLASS_PUNCTUATION_START | sublime.CLASS_LINE_START | \
                  sublime.CLASS_WORD_END   | sublime.CLASS_PUNCTUATION_END   | sublime.CLASS_LINE_END

        separators = "./\\\"'-:,.;~!@#$%^&*|+=`~?)]}>([{<"

        for region in sel:
            if right:
                dest_start = view.find_by_class(region.end(), right, classes, separators)
                dest_end   = dest_start - region.size()
                target     = dest_end
            else:
                dest_start = view.find_by_class(region.begin(), right, classes, separators)
                dest_end   = dest_start + region.size()
                target     = dest_start

            word = view.substr(region)

            sel.subtract(region)
            view.erase(edit, region)
            view.insert(edit, target, word)

            if right:
                sel.add(sublime.Region(dest_end, dest_start))
            else:
                sel.add(sublime.Region(dest_start, dest_end))

            view.show(target, False)

class MoveWordLeftCommand(WordMover):
    def run(self, edit):
        self.move_word(edit, False)

class MoveWordRightCommand(WordMover):
    def run(self, edit):
        self.move_word(edit, True)
