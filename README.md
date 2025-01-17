# About
**i3 Better Float Toggle**

When toggling a window to float mode, sometimes, i3 keeps the full-screen size
for the floated window. That is counter intuitive for me. When toggle to
floating mode, it is becuase I want to exit the current structure of the
windows and see something behind it.

Although it is possible to resize the window after entering the floating state,
it is inconvinient. This script tries to provide an alternative approach by
looking the programs hinted window size and resizing it.

## Install

Configure your i3 to invoke the script. An example is provided bellow.

```
bindsym Mod1+Shift+n exec "python3 <script install dir>/i3betterfloattoggle.py"
```

