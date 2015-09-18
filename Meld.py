import sublime, sublime_plugin

import os

MELD_COMMAND = "meld"

# MeldDiff
class MeldDiff(sublime_plugin.WindowCommand):
    def do_diff(self, index):
        if index == -1:
            return

        os.system('%s "%s" "%s" &' % (MELD_COMMAND, self.current_file, self.open_files[index]))

    def get_open_files(self):
        files = [view.file_name() for view in self.window.views() if type(view.file_name()) is str]
        self.current_file = self.window.active_view().file_name()
        files.remove(self.current_file)
        return files

    def show_select_panel(self):
        self.open_files = self.get_open_files()
        num_files = len(self.open_files)
        if num_files == 0:
            sublime.status_message("No other open files.")
            return
        elif num_files == 1:
            sublime.status_message("Performing comparison between 2 open files.")
            self.do_diff(0)
            return

        files_truncated = ["/".join(f.split("/")[-4:]) for f in self.open_files]
        self.window.show_quick_panel(files_truncated, self.do_diff)

class MeldDiffCommand(MeldDiff):
    def run(self):
        self.show_select_panel()

# MeldCVS
class MeldCvs(sublime_plugin.WindowCommand):
    def do_meld(self, is_dir):
        file_path = self.window.active_view().file_name()
        dir_path  = os.path.dirname(os.path.realpath(file_path))
        if is_dir:
            os.system('%s "%s" &' % (MELD_COMMAND, dir_path))
        else:
            os.system('%s "%s" &' % (MELD_COMMAND, file_path))

class MeldCvsFileCommand(MeldCvs):
    def run(self):
        self.do_meld(False)

class MeldCvsDirCommand(MeldCvs):
    def run(self):
        self.do_meld(True)
