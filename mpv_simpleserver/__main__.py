from bottle import debug
from mpv_simpleserver import mpvserver, debugmode, port


debug(debugmode)
if debugmode:
    mpvserver.run(host='::', port=port, reloader=True)
else:
    mpvserver.run(host='::', port=port, quiet=True)
