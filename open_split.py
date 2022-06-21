import sublime
import sublime_plugin
from typing import Optional


class OpenSplitCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    window = view.window()

    if (text := self.has_selected_word(view.sel())) is not None:
      print(f"found symbol: {text}")
      symbol = window.symbol_locations(text, type=sublime.SYMBOL_TYPE_DEFINITION)

      if len(symbol) > 0:
        first_match = symbol[0]
        file_name = first_match.path
        line = first_match.row
        column = first_match.col
        print(f"first_match {first_match}")
        self.create_or_focus_group1(window)
        target_file = f"{file_name}:{line}:{column}"
        print(f"target_file: {target_file}")
        window.open_file(target_file, sublime.ENCODED_POSITION, group=1)
      else:
        print("symbol is empty")
    else:
      print("Invalid word selected")

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
