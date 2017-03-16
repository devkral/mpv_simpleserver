#! /usr/bin/env python3

from bottle import route, run, template, request, redirect, abort, debug
import os
from subprocess import Popen
import time
import sys
if os.sep != "/":
    import functools

pathtompv = "/usr/bin/mpv"
# path is replaced by filecontent
pages = {"index": "data/index.tpl"} #, "success": "data/success.tpl","success": "data/error.tpl"}
allowed_protocols = ["file", "http", "https", "ftp", "smb", "mf"]
background_volume = int(os.environ.get("BACKGROUND_VOLUME", "70"))
prefaudioquality = os.environ.get("AUDIO", "192")
prefvideoquality = os.environ.get("VIDEO", "480")
novideo = "NOVIDEO" in os.environ
debugmode = "DEBUG" in os.environ
maxscreens = -1
# time to wait before redirecting after start/stop.
# elsewise old information are shown
waittime = 1

parameters = []


if not debugmode:
    parameters += ["--no-terminal", "--really-quiet"]

if sys.platform in ["linux", "freebsd"]:
    if not novideo and os.getenv("DISPLAY") is None and os.getenv("WAYLAND_DISPLAY") is None:
        print("novideo activated because no display variable was found; use DISPLAY=:0")
        novideo = True

if os.sep != "/":
    @functools.lru_cache(maxsize=512)
    def converttopath(path):
        return path.replace(os.sep, "/")
else:
    def converttopath(path):
        return path

if os.sep != "/":
    @functools.lru_cache(maxsize=512)
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
                    _statusdrm = os.path.join("/sys/class/drm/", elem, "status")
                    if not os.path.exists(_statusdrm):
                        continue
                    #wasread = ""
                    with open(_statusdrm, "r") as readob:
                        wasread = readob.read().strip()
                    if wasread != "connected":
                        continue
                    screens += 1
        else: # set to maxscreens if screencounting not supported
            screens = max(0, maxscreens)
        #if maxscreen > 0:
        #    maxscreen -= 1 # begins with 0
        #print("Screens detected:", maxscreen+1)
        if maxscreens > 0:
            return min(maxscreens, screens)
        else:
            return screens
    else:
        return 0

#print("Screens detected:", count_screens())


basedir = os.path.dirname(__file__)
playdir = os.path.join(basedir, "mpv_files")
playdir = os.path.realpath(playdir)


if len(sys.argv)>1:
    if os.path.isdir(sys.argv[1]):
        playdir = sys.argv[1]
    else:
        print("Usage: {} [existing directory]".format(sys.argv[0]))
        sys.exit(1)
else:
    # for relative path security ensure playdir
    os.makedirs(playdir, exist_ok=True)

cur_mpvprocess = {}

for _name, _path in pages.items():
    with open(os.path.join(basedir, _path), "r") as reado:
        pages[_name] = reado.read()

icon = b""
iconpath = os.path.join(basedir, "data/favicon.ico")
if os.path.exists(iconpath):
    with open(iconpath, "rb") as icoob:
        icon = icoob.read()

def check_isplaying_audio():
    for elem in cur_mpvprocess.values():
        if elem[0].poll() is not None and elem[2]:
            return True
    return False
def get_ytdlquality(onlyvideo=False):
    if novideo and not onlyvideo:
        return "--ytdl-format=worstaudio[abr>={aquality}]/bestaudio/worst[abr>={aquality}]/best".format(aquality=prefaudioquality)
    elif not novideo and onlyvideo:
        return "--ytdl-format=worstvideo[height>={vquality}]/bestvideo/worst[height>={vquality}]/best".format(vquality=prefvideoquality)
    elif not novideo and not onlyvideo:
        return "--ytdl-format=worst[height>={vquality}][abr>=?{aquality}]/best".format(aquality=prefaudioquality, vquality=prefvideoquality)
    else:
        return None

def convert_path(path):
    if "://" in path[:10] and path.split("://", 1)[0] not in allowed_protocols:
        return None, False
    if "file://" in path[:7]:
        path = path[7:]
    if "://" not in path: # if is file
        path = converttopath(path)
        path = path.lstrip("./")
        path = os.path.join(playdir, path)
        return path, True
    return path, False

@route(path='/favicon.ico', method="GET")
def return_icon():
    return icon

@route(path='/index/', method="GET")
def redwrong_index():
    redirect("/index")

@route(path='/index', method="GET")
@route(path='/', method="GET")
def index_a():
    ret = index_intern("")
    if ret:
        return ret
    abort(500, "Magic smoke?")


@route(path='/index/<path:path>', method="GET")
def index_b(path):
    path = converttopath(path)
    ret = index_intern(path)
    if ret:
        return ret
    abort(404, "directory not found")

def index_intern(relpath):
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
                pllist.append(("..", "dir", backconvert(relpath)))
            else:
                pllist.append(("..", "dir", backconvert(os.path.dirname(relpath))))
        for _file in os.listdir(path):
            _fullfile = os.path.join(path, _file)
            if os.path.isdir(_fullfile):
                pllist.append((_file, "dir", backconvert(os.path.relpath(_fullfile, playdir))))
            elif os.path.isfile(_fullfile):
                pllist.append((_file, "file", backconvert(os.path.relpath(_fullfile, playdir))))
    else:
        return None
    listscreens = []
    for screennu, val in cur_mpvprocess.items():
        if val[0].poll() is not None:
            #del cur_mpvprocess[screennu]
            continue
        listscreens.append((screennu, val[1]))
    screens = count_screens()
    hidescreens = screens<=1
    print(backconvert(relpath))
    return template(pages["index"], currentdir=backconvert(relpath), \
                    currentfile=backconvert(currentfile), \
                    playfiles=pllist, hidescreens=hidescreens, \
                    maxscreens=max(0,screens-1), playingscreens=listscreens)

@route(path='/start/<screen:int>', method="POST")
def start_a(screen):
    start_mpv(screen)

@route(path='/start', method="POST")
def start_b():
    start_mpv(int(request.forms.get('screenid')))
        
def start_mpv(screen):
    if screen>max(count_screens()-1, 0) or screen < 0:
        abort(400,"Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:
        cur_mpvprocess.get(screen)[0].terminate()
        cur_mpvprocess.get(screen)[0].wait()
    turl = request.forms.getunicode('stream_path', "")
    if turl=="":
        abort(400,"Error: no stream/file specified")
        return
    # should fix arbitary reads
    newurl, isfile = convert_path(turl)
    if newurl is None:
        abort(400,"forbidden pathtype")
        return
    if isfile and not os.path.isfile(newurl):
        abort(400,"no such file")
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
    if check_isplaying_audio() and not novideo:
        calledargs += ["--audio=no"]
        hasaudio = False
    elif not novideo:
        hasaudio = True
        if request.forms.get('background', False):
            calledargs += ["--volume={}".format(background_volume)]
        #else:
        #    calledargs += ["--volume=100"]
    else:
        abort(400,"cannot play video (novideo and audio plays)")
        return
    calledargs += [get_ytdlquality(onlyvideo=not hasaudio)]
    if calledargs[-1] is None:
        abort(400,"should not happen, case catched")
        return
    calledargs.append(newurl)
    cur_mpvprocess[screen] = [Popen(calledargs, cwd=playdir), turl, hasaudio]
    time.sleep(waittime)
    if cur_mpvprocess[screen][0].poll() is not None:
        abort(500, "playing file failed")
    else:
        redirect("/index")

@route(path='/stop', method="POST")
def stop_b():
    stop_mpv(int(request.forms.get('screenid')))
    
@route(path='/stop/<screen:int>', method="GET")
def stop(screen):
    stop_mpv(screen)
    
def stop_mpv(screen):
    if screen > max(0, maxscreens) or screen < 0:
        abort(400,"Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:
        cur_mpvprocess.get(screen)[0].terminate()
    #else:
        #redirect("/") #Error: screen not exist")
        #abort(400,"Error: screen not exist")
        #return
    time.sleep(waittime)
    redirect("/index")

debug(debugmode)
if debugmode:
    run(host='::', port=8080)
else:
    run(host='::', port=8080, quiet=True)
