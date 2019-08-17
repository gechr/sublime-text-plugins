import sublime, sublime_plugin

# 0.5 mebibytes = 512^2 bytes = 524288 bytes
DEFAULT_MAX_FILE_SIZE = 524288

# Zero-width characters
SPACELESS_RE = (
    "\u007F-\u009F"
    "\u00AD"
    "\u200B-\u200F"
    "\u2028-\u202E"
    "\u2060-\u206F"
    "\u3164"
    "\uFE00-\uFE0F"
    "\uFEFF"
)

# Dodgy ~single-ish spaces
SPACEY_RE = "\u00A0" "\u2000-\u200A" "\u202F" "\u205F" "\u2800" "\u3000"

# Whitelisted characters
WHITELIST = "£€%©®™%"

INVALID_RE = r"[^\x00-\x7F" + WHITELIST + SPACELESS_RE + SPACEY_RE + "]"
ZEROWIDTH_RE = r"[" + SPACELESS_RE + SPACEY_RE + "]"


def _file_too_large(view):
    if view.size() > DEFAULT_MAX_FILE_SIZE:
        sublime.status_message("File too large - BadCharacters plugin disabled.")
        return True


class BadCharactersListener(sublime_plugin.EventListener):
    def highlight_bad_characters(self, view):
        # stop if it's a scratch view or the file is too large
        if not view.window() or _file_too_large(view):
            return

        # clear any previous regions
        view.erase_regions("BadCharactersListener")

        zerowidth_regions = view.find_all(ZEROWIDTH_RE)
        for region in zerowidth_regions:
            region.a -= 1
            region.b += 1
        invalid_regions = view.find_all(INVALID_RE)

        # highlight the regions
        if zerowidth_regions:
            view.add_regions(
                "BadCharactersListener",
                zerowidth_regions,
                "invalid.illegal",
                "",
                sublime.DRAW_EMPTY,
            )
        if invalid_regions:
            view.add_regions(
                "BadCharactersListener",
                invalid_regions,
                "invalid.illegal",
                "",
                sublime.DRAW_EMPTY,
            )

    def on_modified(self, view):
        self.highlight_bad_characters(view)

    def on_load(self, view):
        self.highlight_bad_characters(view)

    def on_pre_save(self, view):
        self.highlight_bad_characters(view)
