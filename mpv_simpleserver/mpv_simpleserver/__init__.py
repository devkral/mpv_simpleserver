#! /usr/bin/env python3


from subprocess import Popen, TimeoutExpired
import os
import re
import sys
import json
from urllib.parse import quote

import bottle
from bottle import request, redirect, abort, view, static_file
from bottle import Bottle

pathtompv = "/usr/bin/mpv"
allowed_protocols = ["file", "http", "https", "ftp", "smb", "mf"]
background_volume = int(os.environ.get("BACKGROUND_VOLUME", "70"))
prefaudioquality = os.environ.get("AUDIO", "192")
prefvideoquality = os.environ.get("VIDEO", "480")
port = int(os.environ.get("PORT", "8080"))
novideo = "NOVIDEO" in os.environ
debugmode = "DEBUG" in os.environ
maxscreens = -1
# time to wait before redirecting after start/stop.
# elsewise old information are shown
waittime = 6

parameters = []


if not debugmode:
    parameters += ["--no-terminal", "--really-quiet"]

if sys.platform in ["linux", "freebsd"]:
    if not novideo and os.getenv("DISPLAY") is None and os.getenv("WAYLAND_DISPLAY") is None:  # noqa
        print("novideo activated because no display variable was found; use DISPLAY=:0")  # noqa
        novideo = True

if os.sep != "/":
    def converttopath(path):
        return path.replace(os.sep, "/")
else:
    def converttopath(path):
        return path

if os.sep != "/":
    def backconvert(path):
        return path.replace(os.sep, "/")
else:
    def backconvert(path):
        return path


def count_screens():
    if not novideo:
        screens = 0
        if os.uname().sysname == "Linux":
            if os.path.isdir("/sys/class/drm/"):
                for elem in os.listdir("/sys/class/drm/"):
                    _statusdrm = os.path.join(
                        "/sys/class/drm/", elem, "status"
                    )
                    if not os.path.exists(_statusdrm):
                        continue
                    # wasread = ""
                    with open(_statusdrm, "r") as readob:
                        wasread = readob.read().strip()
                    if wasread != "connected":
                        continue
                    screens += 1
        else:  # set to maxscreens if screencounting not supported
            screens = max(0, maxscreens)
        # if maxscreen > 0:
        #    maxscreen -= 1 # begins with 0
        # print("Screens detected:", maxscreen+1)
        if maxscreens > 0:
            return min(maxscreens, screens)
        else:
            return screens
    else:
        return 0

# print("Screens detected:", count_screens())


basedir = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(basedir, "views"))
playdir = os.path.join(os.path.expanduser("~"), "mpv_files")
playdir = os.path.realpath(playdir)

cur_mpvprocess = {}

datapath = os.path.join(basedir, "static")


def check_isplaying_audio():
    for elem in cur_mpvprocess.values():
        if elem[0].poll() is None and elem[2]:
            return True
    return False


def get_ytdlquality(onlyvideo=False):
    if novideo and not onlyvideo:
        return "--ytdl-format=worstaudio[abr>={aquality}]/bestaudio/worst[abr>={aquality}]/best".format(aquality=prefaudioquality)  # noqa
    elif not novideo and onlyvideo:
        return "--ytdl-format=worstvideo[height>={vquality}]/bestvideo/worst[height>={vquality}]/best".format(vquality=prefvideoquality)  # noqa
    elif not novideo and not onlyvideo:
        return "--ytdl-format=worst[height>={vquality}][abr>=?{aquality}]/best".format(aquality=prefaudioquality, vquality=prefvideoquality)  # noqa
    else:
        return None


remove_v = re.compile("&?v=[^&]*&?")


def convert_path(path):
    if "://" in path[:10] and path.split("://", 1)[0] not in allowed_protocols:
        return None, False
    if "file://" in path[:7]:
        path = path[7:]
    if "://" not in path:  # is a file
        path = converttopath(path)
        path = path.lstrip("./")
        path = os.path.join(playdir, path)
        return path, True
    return path, False


def get_state(relpath=""):
    relpath = relpath.lstrip("./\\")
    path = os.path.join(playdir, relpath)
    pllist = []
    currentfile = ""
    if not os.path.isdir(path) and os.path.isfile(path):
        currentfile = relpath
        relpath = os.path.dirname(relpath)
        path = os.path.dirname(path)
    if os.path.isdir(path):
        if relpath != "":
            if currentfile != "":
                pllist.append((
                    "..",
                    "dir",
                    quote(backconvert(relpath))
                ))
            else:
                pllist.append((
                    "..",
                    "dir",
                    quote(backconvert(os.path.dirname(relpath)))
                ))
        for _file in os.listdir(path):
            _fullfile = os.path.join(path, _file)
            if os.path.isdir(_fullfile):
                pllist.append((
                    _file,
                    "dir",
                    quote(
                        backconvert(os.path.relpath(_fullfile, playdir))
                    )
                ))
            elif os.path.isfile(_fullfile):
                pllist.append((
                    _file,
                    "file",
                    quote(
                        backconvert(os.path.relpath(_fullfile, playdir))
                    )
                ))
    else:
        return None
    listscreens = []
    for screennu, val in cur_mpvprocess.items():
        if val[0].poll() is not None:
            # del cur_mpvprocess[screennu]
            continue
        listscreens.append((screennu, *val[1:]))
    screens = count_screens()
    hidescreens = screens <= 1
    return dict(
        currentdir=backconvert(relpath),
        currentfile=backconvert(currentfile),
        playfiles=pllist,
        hidescreens=hidescreens,
        maxscreens=max(0, screens-1),
        playingscreens=listscreens
    )


def start_mpv(screen):
    if screen > max(count_screens()-1, 0) or screen < 0:
        abort(400, "Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:  # noqa
        cur_mpvprocess.get(screen)[0].terminate()
        cur_mpvprocess.get(screen)[0].wait()
    turl = request.forms.getunicode('stream_path', "")
    if turl == "":
        abort(400, "Error: no stream/file specified")
        return
    playplaylist = bool(request.forms.get('playplaylist', True))
    # should fix arbitary reads
    newurl, isfile = convert_path(turl)
    if newurl is None:
        abort(400, "forbidden pathtype")
        return
    if playplaylist:
        if not isfile and "youtube" in newurl and "list=" in newurl:
            newurl = remove_v.sub("", newurl.replace("watch", "playlist"))
    else:
        pass
    if isfile and not os.path.isfile(newurl):
        abort(400, "no such file")
        return
    calledargs = [pathtompv]
    calledargs += parameters
    screens = count_screens()
    if not novideo and screens > 0:
        calledargs += ["--fs"]
        if screens > 1:
            calledargs += ["--fs-screen", "{}".format(screen)]
    else:
        calledargs.append("--vo=null")
        calledargs.append("--no-video")
    isbackground = False
    isloop = False
    if check_isplaying_audio():
        calledargs += ["--audio=no"]
        hasaudio = False
    else:
        hasaudio = True
        if request.forms.get('background', False):
            calledargs += ["--volume={}".format(background_volume)]
            isbackground = True
        # else:
        #    calledargs += ["--volume=100"]
    if request.forms.get('loop', False):
        calledargs += ["--loop=inf"]
        isloop = True
    calledargs.append(get_ytdlquality(onlyvideo=not hasaudio))
    if calledargs[-1] is None:
        abort(400, "cannot play video (novideo and audio plays)")
        return
    calledargs.append(newurl)
    cur_mpvprocess[screen] = [
        Popen(calledargs, cwd=playdir),
        turl,
        hasaudio,
        isbackground,
        isloop
    ]
    try:
        # raise timeout if source still runs (=success)
        if isfile:
            cur_mpvprocess[screen][0].wait(1)
        else:
            cur_mpvprocess[screen][0].wait(waittime)
        abort(500, "playing file failed")
    except TimeoutExpired:
        redirect("/index/")


def stop_mpv(screen):
    if screen > max(0, maxscreens) or screen < 0:
        abort(400, "Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:  # noqa
        cur_mpvprocess.get(screen)[0].terminate()
        cur_mpvprocess.get(screen)[0].wait(waittime)
    # else:
        # redirect("/") #Error: screen not exist")
        # abort(400,"Error: screen not exist")
        # return
    redirect("/index/")


mpvserver = Bottle()


@mpvserver.route(path='/favicon.ico', method="GET")
def return_icon():
    return static_file("favicon.ico", root=datapath)


@mpvserver.route(path='/static/<sfile>', method="GET")
def return_static(sfile):
    return static_file(sfile, root=datapath)


@mpvserver.route(path='/', method="GET")
@mpvserver.route(path='/index/', method="GET")
@mpvserver.route(path='/index/<path:path>', method="GET")
@view('mpv_simpleserver/index')
def index_path(path=""):
    if path:
        path = converttopath(path)
    ret = get_state(path)
    if ret:
        return ret
    abort(404, "directory not found")


@mpvserver.route(path='/json/', method="GET")
@mpvserver.route(path='/json/<path:path>', method="GET")
def json_path(path=""):
    if path != "":
        path = converttopath(path)
    ret = get_state(path)
    if ret:
        return json.dumps(ret)
    abort(404, "directory not found")


@mpvserver.route(path='/start/', method="POST")
def start_path(screen=None):
    if screen is None:
        screen = int(request.forms.get('screenid'))
    start_mpv(screen)


@mpvserver.route(path='/stop/', method="POST")
@mpvserver.route(path='/stop/<screen:int>', method="GET")
def stop_path(screen=None):
    if screen is None:
        screen = int(request.forms.get('screenid'))
    stop_mpv(screen)
