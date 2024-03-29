# OpenSplit

[Sublime Text](https://www.sublimetext.com/) plugin to Open the symbol definition under the cursor in a separate group.

![](OpenSplit.gif)


By default only 2 groups are supported where the group opened will be below the current one (similar to `CMD + ALT + SHIFT + 2`).


## Installation

- Open the command palette with `CMD + SHIFT + P`
- Select `Package Control: Add Repository`
- Enter https://github.com/ssanj/OpenSplit for the repository
- Select `Package Control: Install Package`
- Choose OpenSplit


## Functionality

### Open a symbol in a Split window

To open a symbol in a split window press `F7`.

![](OpenSplit-open-symbol.png)

### Close the Split Window

To close all the views in a split window press `SHIFT + F7`

### Close all views except the current view

To close all the views except the current view, and move to a single-grouped layout use `SHIFT + CMD + F7`

### Move all views except the current view

To move all views out of the current group into the alternate group except the current view use `SHIFT + CTRL + DOWN`

### Move the current view and swap the other views

To move the current view into the alternate group and move all views from the alternate group into the current group use `SHIFT + CTRL + UP`

