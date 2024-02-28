from typing import List  # noqa: F401

from libqtile import utils, hook, qtile

from modules.groups import floating_layout, groups, layouts
from modules.keymaps import keys, mouse
from modules.statusbar import extension_defaults, screens, widget_defaults
from Xlib import display as xdisplay

import os
import subprocess
import psutil
import sys

# @hook.subscribe.startup_once
# def start_dex():
#     s_layout = os.path.expanduser('~/.screenlayout/my-config.sh')

    # subprocess.run(["/usr/bin/dex", "-a"])
    # Start udiskie for automounting.
    # subprocess.Popen(["/usr/bin/udiskie", "--tray"])
    # subprocess.Popen(["/usr/bin/playerctld", "daemon"])

    #subprocess.run([s_layout])

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

auto_fullscreen = False
auto_minimize = False
bring_front_click = True
cursor_warp = True
floats_kept_above = True

dgroups_app_rules = []  # type: List
dgroups_key_binder = None
dpi_scale = 1

focus_on_window_activation = "smart"
follow_mouse_focus = True
reconfigure_screens = True

wmname = "LG3D"
