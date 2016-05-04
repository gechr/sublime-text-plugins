import subprocess

import sublime, sublime_plugin

class PrettifyTerraformCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        p = subprocess.Popen("terraform fmt -no-color -",
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        region = sublime.Region(0, self.view.size())
        stdout, stderr = p.communicate(self.view.substr(region).encode('utf-8'))

        if p.returncode == 0:
            self.view.replace(edit, region, stdout.decode('utf-8'))
            return

        sublime.error_message(stderr.decode('utf-8'))
