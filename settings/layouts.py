from libqtile import layout
from libqtile.config import Match
from .theme import colors

# Layouts and layout rules

layout_conf = {
    'border_focus': colors['focus'][0],
    'border_width': 1,
    # 'margin': 4
}

layouts = [
    layout.Columns(**layout_conf),
    layout.Max(),
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
