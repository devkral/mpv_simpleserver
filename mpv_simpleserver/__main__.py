import sys
import os
from bottle import debug
import mpv_simpleserver
from mpv_simpleserver import mpvserver, debugmode, port


def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            mpv_simpleserver.playdir = sys.argv[1]
        else:
            print("Usage: {} [existing directory]".format(sys.argv[0]))
            sys.exit(1)
    else:
        # for relative path security ensure playdir
        os.makedirs(mpv_simpleserver.playdir, exist_ok=True)

    debug(debugmode)
    if debugmode:
        mpvserver.run(host='::', port=port, reloader=True)
    else:
        mpvserver.run(host='::', port=port, quiet=True)


if __name__ == "__main__":
    main()
