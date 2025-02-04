# About
**i3 Better Float Toggle**

Using [i3 window manager](https://i3wm.org/), when I toggle a window to float
mode (a window that is not structured automatically), sometimes, the
full-screen size is kept. That is counterintuitive for me. When I toggle to
floating mode, it is because I want to remove the window from the current
structure and see something behind it.

Although it is possible to resize the window after entering the floating state,
it is inconvenient. This script tries to provide an alternative approach by
looking the programs hinted window size and resizing it.

## Install

Configure your i3 to invoke the script. An example is provided bellow.

```
bindsym Mod1+Shift+n exec "python3 <script install dir>/i3betterfloattoggle.py"
```

## TODO

- [x] Remember the users last configuration for floating window size (inspired from [this post](https://www.reddit.com/r/i3wm/comments/l8tlxt/how_to_set_default_size_for_floating_windows/))

> Feel free to open issue and submit suggestions; discussig how your workflow may need a better float-toggle function
