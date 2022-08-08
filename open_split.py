import sublime
import sublime_plugin
from typing import Optional
from OpenSplit.target_file import TargetFile

class OpenSplitCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    window = view.window()

    if window:
      if (text := self.has_selected_word(view.sel())) is not None:
        print(f"found symbol: {text}")
        symbol = window.symbol_locations(text, type=sublime.SYMBOL_TYPE_DEFINITION)

        if len(symbol) > 0:
          target_file = self.get_target_file(symbol[0])
          # if the target file open in group 0?
           # find file in group 0
           # close file in group 0

          # open file in group 1
          if target_file and not self.open_in_views(window, target_file):
            self.create_or_focus_group1(window)
            window.open_file(target_file.encoded_str(), sublime.ENCODED_POSITION, group=1)
          else:
            print("no valid target file")
        else:
          print("symbol is empty")
      else:
        print("Invalid word selected")
    else:
      print("No active window found")

  def open_in_views(self, window: sublime.Window, target_file: TargetFile) -> bool:
    views = window.views()
    found = [v for v in views if v.file_name() == target_file.file_name]
    return len(found) > 0

  def get_target_file(self, first_match: sublime.SymbolLocation) -> TargetFile:
    file_name = first_match.path
    line = first_match.row
    column = first_match.col
    target_file = TargetFile(file_name, line, column)
    print(f"target_file: {target_file}")
    return target_file

  def create_or_focus_group1(self, window: sublime.Window) -> None:
    groups = window.num_groups()
    active_group = window.active_group()
    if groups > 1:
      if active_group == 1:
        print("nothing to do. Split 1 is already selected")
      else:
        window.focus_group(1)
    else:
      window.run_command('set_layout', { "cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]] })
      window.focus_group(1)


  def has_selected_word(self, selection: sublime.Selection) -> Optional[str]:
    if len(selection) > 0:
      view = self.view
      possible_word = view.substr(view.word(selection[0]))
      if possible_word and possible_word.lstrip():
        word = possible_word.lstrip()
      else:
        word = None
    else:
      word = None

    return word
