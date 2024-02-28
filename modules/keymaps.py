from libqtile.command import lazy
from libqtile.config import EzClick, EzDrag, EzKey, Screen
from qtile_extras import widget as widgetx
from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupWidget
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT

from libqtile import qtile

import os

# Default applications
myTerminal = "alacritty"
# myBrowser = "google-chrome-stable --password-store=gnome"
myBrowser = "firefox"
file_manager = "thunar"
my_editor = "code"
notes = "obsidian"

EzKey.modifier_keys = {
    "M": "mod4",
    "A": "mod1",
    "S": "shift",
    "C": "control",
    "H": "mod3",
}


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


def widgets_pane(qtile):
    qtile.cmd_to_screen(0)
    i = qtile.screens.index(qtile.current_screen)
    qtile.screens[i].cmd_toggle_group("0",True)
    qtile.cmd_spawn(os.path.expanduser("~/.config/qtile/Scripts/wdigets"))
    # lazy.spawn()
    




# Drag floating layouts.
mouse = [
    EzDrag(
        "M-<Button1>",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    EzDrag(
        "M-<Button3>", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    EzClick("M-<Button2>", lazy.window.bring_to_front()),
]

window_navigation = [
    EzKey("M-h", lazy.layout.left()),
    EzKey("M-j", lazy.layout.down()),
    EzKey("M-k", lazy.layout.up()),
    EzKey("M-l", lazy.layout.right()),
]

window_displacement = [
    EzKey("M-<Tab>", lazy.layout.next()),  # Shift focus -> other window(s) in stack
    EzKey("M-S-<Tab>", lazy.layout.previous()),
    EzKey("M-<Return>", lazy.layout.swap_main()),
    EzKey("M-S-j", lazy.layout.swap_left(), lazy.layout.shuffle_left()),
    EzKey("M-S-k", lazy.layout.swap_down(), lazy.layout.shuffle_down()),
    EzKey("M-S-i", lazy.layout.swap_up(), lazy.layout.shuffle_up()),
    EzKey("M-S-l", lazy.layout.swap_right(), lazy.layout.shuffle_right()),
    EzKey("M-S-<comma>", lazy.function(window_to_next_screen)),
    EzKey("M-S-<period>", lazy.function(window_to_previous_screen)),
    EzKey("M-C-<comma>", lazy.function(window_to_next_screen, switch_screen=True)),
    EzKey("M-C-<period>", lazy.function(window_to_previous_screen, switch_screen=True))
]

window_size_control = [
    EzKey("M-C-j", lazy.layout.grow_left()),
    EzKey("M-C-k", lazy.layout.grow_down()),
    EzKey("M-C-i", lazy.layout.grow_up()),
    EzKey("M-C-l", lazy.layout.grow_right()),
    EzKey("M-C-m", lazy.layout.maximize()),
    EzKey("M-C-n", lazy.layout.normalize()), 
    EzKey("M-A-<comma>", lazy.layout.shrink()), 
    EzKey("M-A-<period>", lazy.layout.grow()),  # Restore to original size
]

toggles = [
    EzKey("M-w", lazy.window.kill()),
    EzKey("M-<space>", lazy.next_layout()),
    EzKey("M-f", lazy.window.toggle_floating()),
    EzKey("M-m", lazy.window.toggle_minimize()),
    EzKey("M-C-<space>", lazy.group.setlayout("max")),
    EzKey("M-S-<space>", lazy.window.toggle_fullscreen()),
    # EzKey("M-A-C-h", lazy.function()),
]

qtile_controls = [
    EzKey("M-S-r", lazy.restart()),
    EzKey("M-S-q", lazy.shutdown()),
    EzKey("M-C-r", lazy.reload_config()),
]

# rofi_spawns = [
#     EzKey("M-p", lazy.spawn("rofi -show drun")),
#     EzKey("M-A-<space>", lazy.spawn("rofi -show window")),
#     EzKey("M-S-p", lazy.spawn("rofi -show run")),
#     EzKey("M-C-S-p", lazy.function(widgets_pane)),
#     EzKey("M-C-p", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu")),
# ]

rofi_spawns = [
    EzKey("M-p", lazy.spawn(os.path.expanduser("~/.config/rofi/bin/launcher"))),
    EzKey("M-A-<space>", lazy.spawn("rofi -show window")),
    EzKey("M-S-p", lazy.spawn(os.path.expanduser("~/.config/rofi/bin/runner"))),
    EzKey("M-C-p", lazy.spawn(os.path.expanduser("~/.config/rofi/bin/powermenu"))),
    EzKey("M-C-S-w", lazy.function(widgets_pane))
]

application_spawns = [
    EzKey("M-t", lazy.spawn(myTerminal)),
    EzKey("M-b", lazy.spawn(myBrowser)),
    EzKey("M-e", lazy.spawn(file_manager)),
    EzKey("M-c", lazy.spawn(my_editor)),
    EzKey("M-o", lazy.spawn(notes)),
]

audio_controls = [
    EzKey("<XF86AudioMute>", lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/volctl --mute"))),
    EzKey("<XF86AudioRaiseVolume>", lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/volctl  --up"))),
    EzKey("<XF86AudioLowerVolume>", lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/volctl  --down"))),
    EzKey("<XF86AudioMicMute>", lazy.spawn("micvol --mute")),
    EzKey("M-A-p", lazy.widget["mpris2"].toggle_player()),
]

media_controls = [
    EzKey("M-<Down>", lazy.spawn("playerctl play-pause")),
    EzKey("M-<Right>", lazy.spawn("playerctl next")),
    EzKey("M-<Left>", lazy.spawn("playerctl previous")),
]

xrandr_controls = [
    EzKey("M-A-C-s", lazy.spawn(os.path.expanduser("~/.config/rofi/bin/screens"))),
]

screenshot = [
    EzKey("<Print>", lazy.spawn(os.path.expanduser("~/.config/rofi/bin/screenshot"))),
    # EzKey("C-<Print>", lazy.spawn("scrcap -c -w")),
    # EzKey("A-<Print>", lazy.spawn("scrcap -a")),
    # EzKey("C-A-<Print>", lazy.spawn("scrcap -c -a")),
    # EzKey("S-<Print>", lazy.spawn("scrcap -r")),
    # EzKey("C-S-<Print>", lazy.spawn("scrcap -c -r")),
]

quick_launch = [
    EzKey("<XF86Calculator>", lazy.spawn([myTerminal, "-T Qalc -e qalc"])),
    EzKey("M-A-C-<Up>", lazy.window.up_opacity()),
    EzKey("M-A-C-<Down>", lazy.window.down_opacity()),
]

keys = [
    *window_navigation,
    *window_displacement,
    *window_size_control,
    *toggles,
    *qtile_controls,
    *rofi_spawns,
    *application_spawns,
    *audio_controls,
    *media_controls,
    *screenshot,
    *quick_launch,
    *xrandr_controls,
]