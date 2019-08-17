import sublime_plugin

"""
  Key Bindings:

    { "keys": ["super+alt+v"], "command": "split_pane", "args": {"orientation": "vertical"} },
    { "keys": ["super+alt+h"], "command": "split_pane", "args": {"orientation": "horizontal"} }

"""

LAYOUTS = {
    "vertical": {
        "cols": [0.0, 0.5, 1.0],
        "rows": [0.0, 1.0],
        "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
    },
    "horizontal": {
        "cols": [0.0, 1.0],
        "rows": [0.0, 0.5, 1.0],
        "cells": [[0, 0, 1, 1], [0, 1, 1, 2]],
    },
    "default": {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]},
}


class SplitPaneCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        self.orientation = "default"

    def run(self, *args, **kwargs):
        w = self.window
        orientation = kwargs.get("orientation", "default")
        if self.orientation == "default":
            w.run_command("set_layout", LAYOUTS.get(orientation, LAYOUTS["default"]))
            if len(w.views()) > 1:
                w.focus_group(0)
                w.run_command("move_to_group", {"group": 1})
            self.orientation = orientation
        elif self.orientation != orientation:
            w.run_command("set_layout", LAYOUTS[orientation])
            self.orientation = orientation
        else:
            w.run_command("set_layout", LAYOUTS["default"])
            w.focus_group(1)
            self.orientation = "default"
