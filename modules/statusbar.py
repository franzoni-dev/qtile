from libqtile import bar, qtile, hook, utils
from libqtile.config import Screen
from libqtile.lazy import lazy
from modules.groups import borderline
from Xlib import display as xdisplay

from qtile_extras import widget as widgetx
from qtile_extras.widget.decorations import PowerLineDecoration
# from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT


import os
# import qtile_extras.hook

from modules.themes import palette

fontinfo = dict(
    # font="NotoSansM Nerd Font",
    font="JetBrainsMono NFP",
    fontsize=16,
    padding=7,
)

rofi = "rofi -no-lazy-grab -show drun -modi drun"

# @qtile_extras.hook.subscribe.mpris_new_track
# def new_track(metadata):
#     if metadata["xesam:title"] == "Never Gonna Give You Up":
#         qtile.spawn("max_volume.sh")

def colorstr(color,symbol,params):
    return f"<span size='large' foreground='{color}'>{symbol}</span> <span rise='1pt'>{params}</span>"

def wincon(name):
  switch={
    'Telegram': f"<span size='large' foreground='{palette[3]}'>󰍡</span> <span rise='1pt'>{name}</span>",
    'code': f"<span size='large' foreground='{palette[3]}'>󰨞</span> <span rise='1pt'>{name}</span>",
  }
  return switch.get(name," {name}")

def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception as e:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors

num_monitors = get_num_monitors()

sl = [
    widgetx.Spacer,
    {
        "left":True,
        "background": palette[25],
        "foreground": palette[11],
    }
]

sr = [
    widgetx.Spacer,
    {
        "right":True,
        "background": palette[25],
        "foreground": palette[11],
    }
]

groupbox = [
    widgetx.GroupBox,
    {
        "foreground": palette[14],
        "background": palette[21],
        "highlight_method": "line",
        "inactive": palette[3],
        "active": palette[4],
        "this_current_screen_border": palette[4],
        "this_screen_border":palette[7],
        "other_screen_border": palette[12],
        "other_current_screen_border": palette[4],
        "highlight_color":palette[21],
        "center_aligned": False,
        "borderwidth":3,
        "disable_drag": True,
        "font": fontinfo["font"],
        "fontsize": fontinfo["fontsize"],
        "use_mouse_wheel": True,
        "hide_unused": True,
        "spacing": 15,
        "margin_x": 10,
        "right": True,
    },
]

windowname = [
    widgetx.WindowName,
    {
        "background": palette[24],
        "foreground": palette[14],
        # "center_aligned": True,
        "font": fontinfo["font"],
        "fontsize": fontinfo["fontsize"],
        "width": 300,
        "markup":True,
        "fmt": "{}",
        "format": wincon("{name}"),
        "empty_group_string": "",
        "max_chars": 0,
        "padding": 5,
        # "max_chars": 200,
        "scroll": True,
        "mouse_callbacks": {"Button1": lazy.spawn("rofi -show windowcd")},
        "right": True
    },
]

systray = [
    widgetx.Systray,
    {
        "background": palette[20],
        "foreground": palette[3],
        "padding": 10,
        "icon_size":20,
        "left": True
    },
]


logo = [
    widgetx.TextBox,
    {
        "font": fontinfo["font"],
        "background": palette[20],
        "fontsize": fontinfo["fontsize"] * 2,
        "foreground": palette[3],
        "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/rofi/bin/launcher"))},
        "padding": 20,
        "text": "",
        "fontshadow": palette[23],
        "right": True,
    },
]

dash = [
    widgetx.TextBox,
    {
        "font": fontinfo["font"],
        "background": palette[20],
        "fontsize": fontinfo["fontsize"] * 1.5,
        "foreground": palette[3],
        "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/player"))},
        "padding": 20,
        "text": "",
        "fontshadow": palette[23],
        "right": True,
    },
]

power = [
    widgetx.TextBox,
    {
        "font": fontinfo["font"],
        "background": palette[19],
        "fontsize": fontinfo["fontsize"]*1.5,
        "foreground": palette[8],
        "fontshadow": palette[23],
        "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/rofi/bin/powermenu"))},
        "padding": 10,
        "text": " ",
        # "right": True
    },
]

layout = [
    widgetx.CurrentLayout,
    {
        **fontinfo,
        "background": palette[22],
        "foreground": palette[14],
        # "scale": 0.60,
        # "use_mask": True,
        "right": True
    },
]

windowcount = [
    widgetx.WindowCount,{
        "text_format":'󱂬 {num}',
        "background":palette[23],
        "foreground":palette[14],
        "show_zero":True,
        "right": True
    },
]

openwin = [
    widgetx.TaskList,{
        "background": palette[23],
        "foreground": palette[14],
        "highlight_method":"border",
        "border": palette[8],
        "borderwidth": 1,
        "fontsize": fontinfo["fontsize"],
        "margin_x": 10,
        "spacing": 10,
        "padding_x": 10,
        "max_title_width": 100,
        "title_width_method": "uniform",
        #"markup": True,
        # "theme_path":"/usr/share/icons/ePapirus-Dark",
        #"icon_size":fontinfo["fontsize"],
        "theme_mode": "preferred",
        # "markup_floating":"<span>{}</span>",
        # "markup_focused":"<b>{}</b>",
        # "markup_maximized":"<span>{}</span>",
        # "markup_minimized":"<s>{}</s>",
        # "markup_normal":"<span>{}</span>",
        "right": True
    }
]

# volume = [
#     widgetx.ALSAWidget,{
#         "mode": "both",
#         "background":palette[21],
#         "bar_colour_high":palette[7],
#         "bar_colour_loud":palette[4],
#         "bar_colour_normal":palette[8],
#         "bar_colour_mute":palette[21],
#         "bar_width": 100,
#         "update_interval": 0.1 ,
#         "margin_y": 5,
#         "foreground":palette[14],
#         # "scroll":True,
#         "text_format": '{volume}%',
#         "font":fontinfo["font"],
#         "fontsize":fontinfo["fontsize"],
#         "emoji":True,
#         "theme_path":"/usr/share/icons/Papirus-Dark",
#         "volume_app": "pavucontrol",
#         "right": True
#     },
# ]

checkupdatesY = [
    widgetx.CheckUpdates,{
        "background":palette[24],
        "foreground":palette[14],
        "colour_no_updates":palette[14],
        "colour_have_updates":palette[14],
        "markup":True,
        "display_format": colorstr(palette[5],"󰏗","{updates}"),
        "no_update_string": colorstr(palette[9],"󰏗","0"),
        "distro": "Arch_yay",
        "update_interval": 720,
        "left": True
    },
]

checkupdatesA = [
    widgetx.CheckUpdates,{
        "background":palette[24],
        "foreground":palette[14],
        "colour_no_updates":palette[14],
        "colour_have_updates":palette[14],
        "markup":True,
        "display_format": colorstr(palette[5],"󰮯","{updates}"),
        "no_update_string": colorstr(palette[9],"󰮯","0"),
        "distro": "Arch",
        "update_interval": 720,
        "left": True
    },
]

cpu = [
    widgetx.CPU,
    {
        **fontinfo,
        "background": palette[21],
        "foreground": palette[14],
        "format": colorstr(palette[6]," ","{freq_current}GHz {load_percent}%"),
        "markup": True,
        "left": True
    },
]

net = [
    widgetx.Net,
    {
        **fontinfo,
        "background": palette[23],
        "foreground": palette[14],
        "format": colorstr(palette[7],"󰈀","{up:.2f} 󰓢 {down:.2f}"),
        "interface": "enp6s0",
        "update_interval": 3,
        "left": True
    },
]

mem = [
    widgetx.Memory,
    {
        **fontinfo,
        "background": palette[22],
        "foreground": palette[14],
        "format": colorstr(palette[8], "", '{MemUsed:.2f}|{MemTotal:.2f}{mm}'),
        "measure_mem": "G",
        "update_interval": 1.0,
        "left": True
    },
]

mpris = [
    widgetx.Mpris2,
    {
        **fontinfo,
        "foreground": palette[14],
        "background": palette[22],
        "markup": True,
        "fmt": colorstr(palette[6], "󰐎","  {}"),
        "width": 250,
        "format": '{xesam:title} - {xesam:artist}',
        "scroll": True,
        "left": True,
        # "scroll_fixed_width": True,
        # "max_chars": 50,
        # "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/player"))},
        # "popup_layout":DEFAULT_LAYOUT,
        # "popup_show_args":{'relative_to': 3, 'relative_to_bar': True},
        # "mouse_callbacks": {"Button1":lazy.widget["mpris2"].toggle_player()},
    },
]


datetime = [
    widgetx.Clock,
    {
        "font": fontinfo["font"],
        "fontsize": fontinfo["fontsize"],
        "background": palette[20],
        "foreground": palette[14],
        "markup": True,
        "format": colorstr(palette[11], "", '<span rise="1pt"> %a %d/%m/%Y</span>  '),
        "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/calendar"))},
        # "right": True
    },
]

clock = [
    widgetx.Clock,
    {
        "font": fontinfo["font"],
        "fontsize": fontinfo["fontsize"],
        "background": palette[25],
        "foreground": palette[14],
        "format": '%I:%M %p',
        # "right": True
    },
]

vpn = [
    widgetx.Image,
    {
        "background": palette[20],
        "filename": "/home/stavox/.config/qtile/icons/nord.svg",
        "mouse_callbacks": {"Button1": lazy.spawn(os.path.expanduser("~/.config/qtile/Scripts/nord"))},
        "margin":8,
        "margin_x": 15,
        "scale": True,
        "right": True,
    },
]


def widgetlist(primary=False, top=True):
    widgets =  [
        logo,
        groupbox,
        layout,
        windowcount,
        # openwin,
        windowname,
        sl,
        clock,
        sl,
        mpris,
        systray,
        power
    ]

    b_widgets =  [
        vpn,
        sr,
        sl,
        checkupdatesY,
        checkupdatesA,
        net,
        mem,
        cpu,
        datetime
    ]
    if not(primary):
        widgets.remove(systray)
    if (top):
        return widgets
    else:
        return b_widgets


def style(widgetlist, primary=False):
    styled = widgetlist[:]

    for index, wid in enumerate(widgetlist):

        plr = dict(
            decorations=[
                PowerLineDecoration(path="arrow_right")
            ]
        )

        pll = dict(
            decorations=[
                PowerLineDecoration(path="arrow_left")
            ]
        )
        # if not(primary):
            # styled[index][1].update([("fontsize",fontinfo["fontsize"] + 10)])
        
        if widgetlist[index][1].get("right"):
            styled[index][1].update(pll)
        elif widgetlist[index][1].get("left"):
            styled[index][1].update(plr)

    return [w[0](**w[1]) for w in styled]




def my_bar(primary=False, h=40, pos=True):
    if(pos):
        margin = [30,30,0,30]
    else:
        margin = [0,30,30,30]

    return bar.Bar(
        [*style(widgetlist(primary, pos),primary)],
        h,
        foreground=palette[14],
        # background=palette[23],
        # background='#11111b80',
        margin=margin,
        opacity=1,
    )


widget_defaults = dict(
    **fontinfo,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=my_bar(primary=True,pos=True),
        bottom=my_bar(primary=True, pos=False),
    ),

]

if num_monitors > 1:
  for m in range(num_monitors - 1):
    screens.append(
      Screen(top=my_bar(primary=False)),  
    )
