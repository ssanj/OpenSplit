import sublime
import sublime_plugin

from typing import Optional, List

class OpenSplitMoveViewAndMoveAllButCommand(sublime_plugin.WindowCommand):
  def run(self) -> None:
    window = self.window
    current_view: Optional[sublime.View] = window.active_view()
    if current_view:

      groups = window.num_groups()
      if groups == 2:
        current_view_group = window.active_group()
        group_to_move_to = 1 if current_view_group == 0 else 0
        views_to_move: List[sublime.View] = [v for v in window.views_in_group(group_to_move_to) if not v.is_dirty() and v != current_view]
        # move the current view to the opposite group
        window.set_view_index(current_view, group_to_move_to, 0)

        # move all the views in the opposite group to the active group
        group_view_count_at_source = len(window.views_in_group(current_view_group))

        for index, v in enumerate(views_to_move):
          window.set_view_index(v, current_view_group, group_view_count_at_source + index)
      else:
        sublime.message_dialog("OpenSplit: Need exactly two groups present. Aborting")
    else:
      sublime.message_dialog("OpenSplit: No active view found")

