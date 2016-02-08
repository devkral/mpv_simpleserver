#! /usr/bin/env python3

from bottle import route, run, template, request, redirect, abort, debug
import os
from subprocess import Popen
import sys

# path is replaced by filecontent
sites = {"index": "data/index.tpl"} #, "success": "data/success.tpl","success": "data/error.tpl"}
allowed_protocols = ["file", "http", "https", "ftp", "smb", "mf"]
background_volume = 70
novideo = False
maxscreen = None

parameters = []
parameters_fallback = []



if sys.platform in ["linux", "freebsd"]:
    if not novideo and os.getenv("DISPLAY") is None and os.getenv("WAYLAND_DISPLAY") is None:
        print("novideo activated because no display variable was found; use DISPLAY=:0")
        novideo = True

if maxscreen is None and not novideo:
    maxscreen = 0
    if os.uname().sysname == "Linux":
        if os.path.isdir("/sys/class/drm/"):
            for elem in os.listdir("/sys/class/drm/"):
                _statusdrm = os.path.join("/sys/class/drm/", elem, "status")
                if not os.path.exists(_statusdrm):
                    continue
                #wasread = ""
                #with open(_statusdrm, "r") as readob:
                #    wasread = readob.read().strip().rstrip()
                #if wasread != "connected":
                #    continue
                maxscreen += 1
    if maxscreen > 0:
        maxscreen -= 1 # begins with 0
    print("Screens detected:", maxscreen+1)



basedir = os.path.dirname(__file__)
playdir = os.path.join(basedir, "mpv_files")
playdir = os.path.realpath(playdir)


if novideo:
    parameters.append("--no-video")
    parameters_fallback.append("--vo=null")
    maxscreen = 0

if len(sys.argv)>1:
    if os.path.isdir(sys.argv[1]):
        playdir = sys.argv[1]
    else:
        print("Usage: {} [existing directory]".format(sys.argv[0]))
        sys.exit(1)


cur_mpvprocess = {}
for _name, _path in sites.items():
    with open(os.path.join(basedir, _path), "r") as reado:
        sites[_name] = reado.read()

def convert_path(path):
    if "://" in path[:10] and path.split("://", 1)[0] not in allowed_protocols:
        return None
    if "file://" in path[:7]:
        path = path[7:]
    if "://" not in path: # if is file
        if os.sep != "/":
            path = path.replace("/", "\\")
        path = path.strip("./")
        path = os.path.join(playdir, path)
        return path
    return path

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
    
def index_intern(path):
    path = path.strip("./\\")
    path = os.path.join(playdir, path)
    pllist = []
    if os.path.isdir(path):
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
    return template(sites["index"], playfiles=pllist, maxscreen=maxscreen,playingscreens=listscreens)
    
    
    
@route(path='/start/<screen:int>', method="POST")
def start_a(screen):
    start_mpv(screen)

@route(path='/start', method="POST")
def start_b():
    start_mpv(int(request.forms.get('screenid')))
        
def start_mpv(screen, use_fallback=False):
    if screen>maxscreen or screen<0:
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
    newurl = convert_path(turl)
    if newurl is None:
        abort(400,"forbidden pathtype")
        return
    calledargs = ["/usr/bin/mpv"]
    if use_fallback:
        calledargs += parameters_fallback
    else:
        calledargs += parameters
    if not novideo:
        calledargs += ["--fs"]
        if maxscreen>0:
            calledargs += ["--fs-screen", "{}".format(screen)]
    if request.forms.get('background', False):
        calledargs += ["--softvol=yes", "--volume={}".format(background_volume)]
    #else:
    #    calledargs += ["--volume=100"]
    
    calledargs.append(newurl)
    cur_mpvprocess[screen] = [Popen(calledargs, cwd=playdir), turl]
    if cur_mpvprocess[screen][0].poll() is not None:
        if use_fallback:
            abort(500,"playing file failed")
        else:
            start_mpv(screen, use_fallback=True)
    else:
        redirect("/")

@route(path='/stop', method="POST")
def stop_b():
    stop_mpv(int(request.forms.get('screenid')))
    
@route(path='/stop/<screen:int>', method="GET")
def stop(screen):
    stop_mpv(screen)
    
def stop_mpv(screen):
    if screen>maxscreen or screen<0:
        abort(400,"Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:
        cur_mpvprocess.get(screen)[0].terminate()
    #else:
        #redirect("/") #Error: screen not exist")
        #abort(400,"Error: screen not exist")
        #return
    redirect("/")

debug(True)
run(host='', port=8080)
