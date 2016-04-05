#! /usr/bin/env python3

from bottle import route, run, template, request, redirect, abort, debug
import os
from subprocess import Popen
import time
import sys

# path is replaced by filecontent
pages = {"index": "data/index.tpl"} #, "success": "data/success.tpl","success": "data/error.tpl"}
allowed_protocols = ["file", "http", "https", "ftp", "smb", "mf"]
background_volume = 70
novideo = False
maxscreens = -1
debugmode = False
# time to wait before redirecting after start/stop.
# elsewise old information are shown
waittime = 1

parameters = []
parameters_fallback = []



if sys.platform in ["linux", "freebsd"]:
    if not novideo and os.getenv("DISPLAY") is None and os.getenv("WAYLAND_DISPLAY") is None:
        print("novideo activated because no display variable was found; use DISPLAY=:0")
        novideo = True

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
                        wasread = readob.read().strip().rstrip()
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

def convert_path(path):
    if "://" in path[:10] and path.split("://", 1)[0] not in allowed_protocols:
        return None, False
    if "file://" in path[:7]:
        path = path[7:]
    if "://" not in path: # if is file
        if os.sep != "/":
            path = path.replace("/", "\\")
        path = path.strip("./")
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
    return index_intern("")

@route(path='/index/<path:path>', method="GET")
def index_b(path):
    if os.sep != "/":
        path = path.replace("/", "\\")
    return index_intern(path)
    
def index_intern(_path):
    _path = _path.strip("./\\")
    path = os.path.join(playdir, _path)
    pllist = []
    if os.path.isdir(path):
        if _path != "":
            pllist.append(("..", "dir", os.path.relpath(os.path.dirname(path), playdir)))
        for _file in os.listdir(path):
            _fullfile = os.path.join(path, _file)
            if os.path.isdir(_fullfile):
                pllist.append((_file, "dir", os.path.relpath(_fullfile, playdir)))
            elif os.path.isfile(_fullfile):
                pllist.append((_file, "file", os.path.relpath(_fullfile, playdir)))
        
    listscreens = []
    for screennu, val in cur_mpvprocess.items():
        if val[0].poll() is not None:
            #del cur_mpvprocess[screennu]
            continue
        listscreens.append((screennu, val[1]))
    screens = count_screens()
    hidescreens = screens<=1
    return template(pages["index"], playfiles=pllist, hidescreens=hidescreens, maxscreens=max(0,screens-1), playingscreens=listscreens)
    
    
    
@route(path='/start/<screen:int>', method="POST")
def start_a(screen):
    start_mpv(screen)

@route(path='/start', method="POST")
def start_b():
    start_mpv(int(request.forms.get('screenid')))
        
def start_mpv(screen, use_fallback=False):
    if screen>max(count_screens()-1, 0) or screen < 0:
        abort(400,"Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:
        cur_mpvprocess.get(screen)[0].terminate()
        cur_mpvprocess.get(screen)[0].wait()
    turl = request.forms.get('stream_path')
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
    calledargs = ["/usr/bin/mpv"]
    if use_fallback:
        calledargs += parameters_fallback
    else:
        calledargs += parameters
    screens = count_screens()
    if not novideo and screens > 0:
        calledargs += ["--fs"]
        if screens > 1:
            calledargs += ["--fs-screen", "{}".format(screen)]
    elif use_fallback:
        calledargs.append("--vo=null")
    else:
        calledargs.append("--no-video")
    if request.forms.get('background', False):
        calledargs += ["--softvol=yes", "--volume={}".format(background_volume)]
    #else:
    #    calledargs += ["--volume=100"]
    
    calledargs.append(newurl)
    cur_mpvprocess[screen] = [Popen(calledargs, cwd=playdir), turl]
    time.sleep(waittime)
    if cur_mpvprocess[screen][0].poll() is not None:
        if use_fallback:
            abort(500, "playing file failed")
        else:
            start_mpv(screen, use_fallback=True)
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
run(host='::', port=8080)
