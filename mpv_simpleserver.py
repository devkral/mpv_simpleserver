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
        for elem in os.listdir("/sys/class/drm/"):
            if os.path.exists(os.path.join("/sys/class/drm/", elem, "status")):
                maxscreen += 1
        if maxscreen>0:
            maxscreen-=1 # begins with 0
    print("Screens detected:", maxscreen+1)


basedir = os.path.dirname(__file__)

playdir = os.path.join(basedir, "mpv_files")
if len(sys.argv)>1:
    if os.path.isdir(sys.argv[1]):
        playdir = sys.argv[1]
    else:
        print("Usage: {} [existing director]".format(sys.argv[0]))
        sys.exit(1)
    

cur_mpvprocess = {}
for _name, _path in sites.items():
    with open(os.path.join(basedir, _path), "r") as reado:
        sites[_name] = reado.read()

@route(path='/index', method="GET")
@route(path='/', method="GET")
def index():
    if os.path.isdir(playdir):
        pllist = os.listdir(playdir)
    else:
        pllist = []
        
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
    #if os.path TODO: mpv can PLAY everything on the local filesystem, fix
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
    else:
        abort(400,"Error: screen not exist")
        return
    redirect("/")


run(host='', port=8080)
