import sublime
import sublime_plugin
from typing import Optional, List
from OpenSplit.target_file import TargetFile
import re

class OpenDefinitionCommand(sublime_plugin.TextCommand):

  phantom_id = "open_split"

  sealed_trait_r = re.compile(r"sealed trait ([A-Z][0-9A-Za-z_]*)")
  trait_r = re.compile(r"trait")


  def run(self, edit):
    view = self.view
    window = view.window()

    if window:
      if (text := self.has_selected_word(view.sel())) is not None:
        print(f"found symbol: {text}")
        symbol = window.symbol_locations(text, type=sublime.SYMBOL_TYPE_DEFINITION)

        if len(symbol) > 0:
          print(symbol)
          result = self.read_symbol_from_file(symbol[0])
          if result:
            print(f"received: {result}")
            self.show_popup(result)
          else:
            print(f"not result")
        else:
          print("symbol is empty")
      else:
        print("Invalid word selected")
    else:
      print("No active window found")

  def read_symbol_from_file(self, symbol_location: sublime.SymbolLocation) -> Optional[str]:
    line = symbol_location.row
    path = symbol_location.path

    with open(path, 'r') as f:
      lines: list[str] = f.readlines()

    if len(lines) >= line and line > 0:
      target_line = lines[line-1].lstrip().rstrip()
      return self.enhance_scala(lines, target_line)
    else:
      return None

  Lines = List[str]

  def enhance_scala(self, lines: Lines, line: str) -> str:
    print(f"---------> [{line}]")
    if OpenDefinitionCommand.sealed_trait_r.match(line):
      groups = OpenDefinitionCommand.sealed_trait_r.match(line).groups()
      if len(groups) > 0:
        trait_name = groups[0]
        # search for lines that are extending trait

        extends_sealed_trait = f"extends {trait_name}"

        matched_extensions: list[str] = [l for l in lines if extends_sealed_trait in l]
        print(f"matched_extensions: {matched_extensions}")
        matched_extensions.insert(0, line)
        return "\n".join(matched_extensions)
      else:
        print("Didn't find groups for sealed traits")
        return line
    elif OpenDefinitionCommand.trait_r.match(line):
      print("not trait matching not implemented")
      return line
    else:
      print("------------> no matches")
      return line


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

  def show_popup(self, content: str) -> None:
    lines = content.split("\n")

    formatted_lines = "".join(list(map(lambda l: f"<div>{l}</div>", lines)))

    markup = f'''
        <body id="open-split">
            <style>
                    body#open-split {{
                      background-color:  white;
                      color: color(var(--bluish));
                    }}
            </style>
            <div>{formatted_lines}</div>
        </body>
    '''
    self.view.show_popup(content = markup, max_width = 800, max_height = 800, flags = sublime.HIDE_ON_MOUSE_MOVE_AWAY)
