import re
import subprocess

import sublime, sublime_plugin

PLUGIN_NAME = "Terraform"

TERRAFORM_SYNTAX_FILE = "Packages/Terraform/Terraform.sublime-syntax"
PLAIN_TEXT_SYNTAX_FILE = "Packages/Text/Plain text.tmLanguage"

TERRAFORM_FMT_COMMAND = "terrafmt -"
TERRAFORM_FMT_ERROR_REGEX = re.compile(
    r"^<stdin>:(?P<linestart>\d+),(?P<colstart>\d+)-(?P<colend>\d+)(,(?P<lineend>\d+))?: (?P<message>.+?)$"
)

ERR_NO_MATCH = """
{}: Could not match error message!

[Message]
{}
[Pattern]
{}"""


def _is_terraform(view, plaintext_to_terraform=False):
    current_syntax_file = view.settings().get("syntax")
    if plaintext_to_terraform and current_syntax_file == PLAIN_TEXT_SYNTAX_FILE:
        view.set_syntax_file(TERRAFORM_SYNTAX_FILE)
        return True
    if current_syntax_file == TERRAFORM_SYNTAX_FILE:
        return True
    return False


class Terraformat(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if _is_terraform(view):
            view.run_command("terraformat")


class TerraformatCommand(sublime_plugin.TextCommand):
    def _highlight_error(self, message):
        m = TERRAFORM_FMT_ERROR_REGEX.search(message)
        if m:
            view = self.view
            sel = view.sel()
            msg = m.group("message")
            line = int(m.group("linestart")) - 1
            colstart = int(m.group("colstart")) - 1
            # Convert line & column to a text point (for seeking)
            error_point = view.text_point(line, colstart)
            # Clear any current selections
            sel.clear()
            # Convert the text point to a region
            err_region = sublime.Region(error_point)
            # Add the selection (i.e. seek the cursor to the error region)
            sel.add(err_region)
            # Highlight the entire line
            highlight_region = [self.view.full_line(error_point)]
            # Draw an error outline around the entire line
            view.add_regions(
                "terraformat_errors",
                highlight_region,
                "invalid",
                "dot",
                sublime.DRAW_OUTLINED,
            )
            # Set the error text in the status bar
            view.set_status("terraformat_errors", msg)
            # Scroll to the error
            view.show(error_point)
            return
        err = ERR_NO_MATCH.format(
            PLUGIN_NAME, message, TERRAFORM_FMT_ERROR_REGEX.pattern
        )
        sublime.error_message(err)

    def _terraform_fmt(self, edit, start, end):
        p = subprocess.Popen(
            TERRAFORM_FMT_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        region = sublime.Region(start, end)
        tf_input = self.view.substr(region)
        stdout, stderr = p.communicate(tf_input.encode("utf-8"))

        if p.returncode == 0:
            tf_output = stdout.decode("utf-8")
            # Do not "dirty" the view unnecessarily
            if tf_input != tf_output:
                self.view.replace(edit, region, tf_output)
            return

        err = stderr.decode("utf-8")
        self._highlight_error(err)

    def run(self, edit):
        self.view.erase_regions("terraformat_errors")
        if not _is_terraform(self.view, plaintext_to_terraform=True):
            return
        # Format the entire file
        self._terraform_fmt(edit, 0, self.view.size())


class TerraformatOnSaveListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        current_syntax_file = view.settings().get("syntax")
        if current_syntax_file == TERRAFORM_SYNTAX_FILE:
            sublime.active_window().run_command("terraformat")
