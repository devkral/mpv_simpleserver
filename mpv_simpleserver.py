#! /usr/bin/env python3

from bottle import route, run, template, request, redirect,abort
import os
from subprocess import Popen
import threading

# path is replaced by filecontent
sites = {"index": "data/index.tpl"} #, "success": "data/success.tpl","success": "data/error.tpl"}

maxscreen = 30
basedir = os.path.dirname(__file__)

playdir = os.path.join(basedir, "mpv_files")


simplempvself = None
class mpv_simpleserver(object):
    cur_mpvprocess = {}
    #cur_mpvlock = None
    
    def __init__(self):
        global simplempvself
        simplempvself = self
        for _name, _path in sites.items():
            with open(os.path.join(basedir, _path), "r") as reado:
                sites[_name] = reado.read()
        
        #os.chroot(playdir)
    
    
    def _routehelper(func):
        def wrapper(*args, **kwargs):
            return func(simplempvself, *args, **kwargs)
        return wrapper
        
    @route(path='/index', method="GET")
    @route(path='/', method="GET")
    @_routehelper
    def index(self):
        if os.path.isdir(playdir):
            pllist = os.listdir(playdir)
        else:
            pllist = []
        
        listscreens = []
        for screennu, val in self.cur_mpvprocess.items():
            if val[0].poll() is not None:
                #del self.cur_mpvprocess[screennu]
                continue
            
            listscreens.append((screennu, val[1]))
        return template(sites["index"], playfiles=pllist, maxscreen=maxscreen,playingscreens=listscreens)
    
    
    
    @route(path='/start/<screen:int>', method="POST")
    @_routehelper
    def start_a(self, screen):
        return self.start_mpv(screen)
        
    #--fs-screen
    @route(path='/start', method="POST")
    @_routehelper
    def start_b(self):
        self.start_mpv(int(request.forms.get('screenid')))
        
    def start_mpv(self, screen):
        if screen>maxscreen or screen<0:
            abort(400,"Error: screenid invalid")
            return
        if self.cur_mpvprocess.get(screen) and self.cur_mpvprocess.get(screen)[0].poll() is None:
            self.cur_mpvprocess.get(screen)[0].terminate()
            self.cur_mpvprocess.get(screen)[0].wait()
        turl = request.forms.get('fileinp')
        if turl=="":
            abort(400,"Error: no file specified")
            return
        #if os.path TODO: mpv can PLAY everything on the local filesystem, fix
        self.cur_mpvprocess[screen] = [Popen(["/usr/bin/mpv", "--fs-screen", str(screen), turl], cwd=playdir), turl]
        #threading.Thread(target=self.cease, args=[screen])
        if self.cur_mpvprocess[screen][0].poll() is not None:
            abort(500,"playing file failed")
        else:
            redirect("/")
    
    @route(path='/stop', method="POST")
    @_routehelper
    def stop_b(self):
        self.stop_mpv(int(request.forms.get('screenid')))
    
    @route(path='/stop/<screen:int>', method="GET")
    @_routehelper
    def stop(self, screen):
        self.stop_mpv(screen)
    
    def stop_mpv(self, screen):
        if screen>maxscreen or screen<0:
            abort(400,"Error: screenid invalid")
            return
        if self.cur_mpvprocess.get(screen) and self.cur_mpvprocess.get(screen)[0].poll() is None:
            self.cur_mpvprocess.get(screen)[0].terminate()
            #del self.cur_mpvprocess[screen]
        else:
            abort(400,"Error: screen not exist")
            return
        redirect("/")
    


if __name__ == "__main__":
    mpv_simpleserver()
    run(host='', port=8080)
