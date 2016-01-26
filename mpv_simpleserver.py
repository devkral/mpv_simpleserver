#! /usr/bin/env python3

from bottle import route, run, template, request, redirect,abort
import os
from subprocess import Popen
import sys

# path is replaced by filecontent
sites = {"index": "data/index.tpl"} #, "success": "data/success.tpl","success": "data/error.tpl"}

maxscreen = None

if maxscreen is None:
    maxscreen = 0
    if os.uname().sysname == "Linux":
        if os.path.isdir("/sys/class/drm/"):
            for elem in os.listdir("/sys/class/drm/"):
                if os.path.exists(os.path.join("/sys/class/drm/", elem, "status")):
                    maxscreen += 1
        
        
        if maxscreen>0:
            maxscreen-=1 # begins with 0
        
    print("Screens detected:", maxscreen+1)


basedir = os.path.dirname(__file__)

playdir = os.path.join(basedir, "mpv_files")

playdir = os.path.realpath(playdir)

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
    if "file://" in path[:7]:
        path = path[7:]
    if "://" not in path:
        if os.sep != "/":
            path = path.replace("/", "\\")
        path = path.strip("./")
        path = os.path.join(playdir, path)
        
    return path

@route(path='/index/', method="GET")
def redwrong_index():
    redirect("/index")

@route(path='/index', method="GET")
@route(path='/', method="GET")
def index_a():
    return index_intern("")

@route(path='/index/<path>', method="GET")
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
        
def start_mpv(screen):
    if screen>maxscreen or screen<0:
        abort(400,"Error: screenid invalid")
        return
    if cur_mpvprocess.get(screen) and cur_mpvprocess.get(screen)[0].poll() is None:
        cur_mpvprocess.get(screen)[0].terminate()
        cur_mpvprocess.get(screen)[0].wait()
    turl = request.forms.get('fileinp')
    if turl=="":
        abort(400,"Error: no file specified")
        return
    # should fix arbitary reads
    turl = convert_path(turl)
    if maxscreen==0:
        calledargs = ["/usr/bin/mpv", "--fs", turl]
    else:
        calledargs = ["/usr/bin/mpv", "--fs-screen", str(screen), turl]
    cur_mpvprocess[screen] = [Popen(calledargs, cwd=playdir), turl]
    if cur_mpvprocess[screen][0].poll() is not None:
        abort(500,"playing file failed")
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


run(host='', port=8080)
