import sublime
import sublime_plugin

from typing import Optional, List

class OpenSplitCloseAllButCommand(sublime_plugin.WindowCommand):
  def run(self) -> None:
    window = self.window
    current_view: Optional[sublime.View] = window.active_view()

    if current_view:
      views: List[sublime.View] = [v for v in window.views() if not v.is_dirty() and v != current_view]

      for v in views:
        v.close()

      window.run_command('set_layout', {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})

    else:
      sublime.message_dialog("OpenSplit: No active view found")
