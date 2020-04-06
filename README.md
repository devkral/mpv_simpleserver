
# Requirements:
python3
python3-bottle
mpv

# Installation

pip install mpv_simpleserver


start skript
mpv_simpleserver

it is possible to specify an other directory by calling:
mpv_simpleserver /home/wanteddirectory

# Env Options
* BACKGROUND_VOLUME: how load if played in background (default 70)
* AUDIO: preferred audio quality (default 192)
* VIDEO: preferred view quality (default 480)
* PORT: preferred Port (default 8080)
* NOVIDEO: audio only mode (auto detected elsewise)
* DEBUG: debug mode
* DISPLAY, WAYLAND_DISPLAY: which display will be used


# warning

be aware that an potential attacker can play any local file in playdir and any remote file
