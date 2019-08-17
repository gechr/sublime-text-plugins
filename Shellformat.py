import subprocess

import sublime, sublime_plugin

PLUGIN_NAME = "Shellformat"

SHELLSCRIPT_SYNTAX_FILE = "Packages/ShellScript/Bash.sublime-syntax"
PLAIN_TEXT_SYNTAX_FILE = "Packages/Text/Plain text.tmLanguage"

SHELLFMT_COMMAND = "shfmt -i 2 -ci"


def _is_shellscript(view, plaintext_to_shellscript=False):
    current_syntax_file = view.settings().get("syntax")
    if plaintext_to_shellscript and current_syntax_file == PLAIN_TEXT_SYNTAX_FILE:
        view.set_syntax_file(SHELLSCRIPT_SYNTAX_FILE)
        return True
    if current_syntax_file == SHELLSCRIPT_SYNTAX_FILE:
        return True
    return False


class Shellformat(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if _is_shellscript(view):
            view.run_command("shellformat")


class ShellformatCommand(sublime_plugin.TextCommand):
    def _shellfmt(self, edit, start, end):
        p = subprocess.Popen(
            SHELLFMT_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        region = sublime.Region(start, end)
        inp = self.view.substr(region)
        stdout, stderr = p.communicate(inp.encode("utf-8"))

        if p.returncode == 0:
            out = stdout.decode("utf-8")
            # Do not "dirty" the view unnecessarily
            if inp != out:
                self.view.replace(edit, region, out)
            return

        self.view.set_status("shellformat_errors", stderr.decode("utf-8"))

    def run(self, edit):
        if not _is_shellscript(self.view, plaintext_to_shellscript=True):
            return
        # Format the entire file
        self._shellfmt(edit, 0, self.view.size())


class ShellformatOnSaveListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        current_syntax_file = view.settings().get("syntax")
        if current_syntax_file == SHELLSCRIPT_SYNTAX_FILE:
            sublime.active_window().run_command("shellformat")
