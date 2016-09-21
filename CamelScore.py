import re

import sublime_plugin

class CamelScoreCommand(sublime_plugin.TextCommand):

    def _is_snake_case(self, word):
        return '_' in word

    def _is_camel_case(self, word):
        return re.match(r'([A-Z][a-z0-9]+)+', word)

    def _snake_to_camel(self, word):
        return ''.join(x.title() for x in word.split('_'))

    def _camel_to_snake(self, word):
        word = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', word).lower()

    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                region = self.view.word(region.a)
            word = self.view.substr(region)
            if self._is_snake_case(word):
                word = self._snake_to_camel(word)
            elif self._is_camel_case(word):
                word = self._camel_to_snake(word)
            else:
                continue
            self.view.replace(edit, region, word)
