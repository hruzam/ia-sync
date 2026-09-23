# keys

In-TUI keybind legend (runbook.py, v0.3 dispatch loop). Transcribed from the
live key-dispatch loop — if this ever disagrees with the running TUI, the
code is truth.

## Global (any focus)

```
? h       open the named-scope help navigator
H         hide / show the bottom hint belt (remembered)
Tab       switch pane: tree ↔ content
q Q Esc   quit (buffer prints to scroll-back)
r         reload all beds + board + vault
R         card's resume: → clipboard (select a card first)
b         toggle buffer pane
P         buffer maintainer (x remove line · X clear · y copy line · q back)
v         flip tree column left ↔ right (remembered)
<  >      move the pane divider (5% steps, remembered)
A A       drain a consumed card → archive/ (two presses; routines never archive)
B         presence board modal (Enter lands on a local-host record's bed)
J K       jump to next / previous bed
1-5       jump to bed part: STATUS / _bus / RUNBOOK / files / raw
m         attach selected bed to the presence board
u         detach own record(s) for the selected bed
p         collect current path into the print buffer
y         copy current path to clipboard (fallback: buffer)
Y         copy current FILE/card CONTENT to clipboard
e  E      open selection in $EDITOR (GUI editors detach; TUI stays)
```

## Help navigator (`?`)

Help scopes are discovered from `session/help/*/HELP.md`; a new named folder
appears automatically. Wide terminals show scope names beside the content.
Narrow terminals show one pane at a time.

```
↑ ↓         select a scope / result, or scroll scope content
Enter →    open the selected scope; Enter on a result lands on its line
←           return to the scope list
Tab         switch scope list ↔ content
[ ]         previous / next scope and open it
Ctrl+F      search the current scope
F           search across all scopes (portable replacement for Ctrl+Shift+F)
q Q Esc     close help
```

Search is case-insensitive. Every typed token must occur on the matching line;
results show the scope, nearest Markdown heading, source line, and matching text.

## Tree focus

```
↑ ↓         move cursor
PgUp PgDn   move cursor a page
→           expand node, or step into first child if already open;
            on a file/card: focus the content pane
←           collapse node, else jump to parent
Enter Space toggle branch · on a file: focus content · on a card: land on
            its bed (or focus content if the card's target isn't here)
F  f        fold/unfold the selected bed
```

## Content focus

```
↑ ↓         scroll one line
PgUp PgDn   scroll one page
g           jump to top
G           jump to end
←           back to tree focus
```
