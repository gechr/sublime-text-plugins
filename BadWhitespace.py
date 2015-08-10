import sublime, sublime_plugin

# 0.5 mebibytes = 512^2 bytes = 524288 bytes
DEFAULT_MAX_FILE_SIZE = 524288

"""
  super regex to detect:

    (1) >1 trailing <tab/space>
    (2) <tab> followed by >1 <space>
    (3) >1 <space>, followed by >1 <tab>, followed by >0 <space>
    (4) <tab> occurring anywhere other than the start of the line
"""
BAD_WHITESPACE_RE = r'\\?(?:[\t ]+$|\t +| +\t+ *|(?!^)(?<!\t)\t+)'

def _file_too_large(view):
    if view.size() > DEFAULT_MAX_FILE_SIZE:
        sublime.status_message("File too large - BadWhitespace plugin disabled.")
        return True

def highlight_whitespace(view, ignore_current_line=True):
    # stop if the file is too large or it's a scratch view
    if _file_too_large(view) or view.is_scratch():
        return

    # clear any previous regions
    view.erase_regions('BadWhitespaceListener')

    # get the current line
    selection = view.sel()[0]
    line = view.line(selection.b)

    if ignore_current_line:
        bad_regions = [r for r in view.find_all(BAD_WHITESPACE_RE)
                       if not r.intersects(line)]
    else:
        bad_regions = view.find_all(BAD_WHITESPACE_RE)

    # actually highlight the regions
    if bad_regions:
        view.add_regions('BadWhitespaceListener',
                         bad_regions,
                         'meta.whitespace.mixed',
                         '',
                         sublime.DRAW_EMPTY)

class BadWhitespaceListener(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        highlight_whitespace(view)

    def on_activated_async(self, view):
        highlight_whitespace(view)

    def on_load_async(self, view):
        highlight_whitespace(view)

    def on_pre_save(self, view):
        highlight_whitespace(view, ignore_current_line=False)
