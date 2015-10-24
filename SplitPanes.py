import sublime_plugin

LAYOUT_NORMAL = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1]]
}

LAYOUT_VERTICAL = {
    "cols": [0.0, 0.5, 1.0],
    "rows": [0.0, 1.0],
    "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
}

LAYOUT_HORIZONTAL = {
    "cols": [0.0, 1.0],
    "rows": [0.0, 0.5, 1.0],
    "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]
}

class SplitPaneCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        orientation = kwargs['orientation']
        w = self.window
        if w.num_groups() == 1:
            if orientation == 'vertical':
                w.run_command('set_layout', LAYOUT_VERTICAL)
            elif orientation == 'horizontal':
                w.run_command('set_layout', LAYOUT_HORIZONTAL)
            else:
                raise Exception('SplitPanes: Unknown orientation "%s"' % (orientation,))
            if len(w.views()) > 1:
                w.focus_group(0)
                w.run_command('move_to_group', {'group': 1})
        else:
            w.run_command('set_layout', LAYOUT_NORMAL)
