<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Play Music</title>
</head>
<header>
<h1>Play Music</h1><br/>
</header>
<table style="width:100%;"><tr>
<td style="width:60%;">
<form method="post">
%if hidescreens == True:
<div hidden>
%end
    Screen: <input name="screenid" id="screenidid" type="number" value="0" max="{{maxscreens}}" min="0" placeholder="<screen>"/>
%if hidescreens:
</div>
%end
%if len(playingscreens) > 0:
    <input value="Stop" type="submit" id="mpv_stop" formaction="/stop"/>
%else:
    <span title="shot in the dark"><input value="Stop" type="submit" id="mpv_stop" style="color: #FFFFFF; background-color: #555555; border-radius: 4px;" formaction="/stop"/></span>
%end
    <br>
    Background (quieter) <input name="background" type="checkbox"/>
    Play Playlist <input name="playplaylist" checked="" type="checkbox"/>
    Loop <input name="loop" type="checkbox"/>
    <br>
    Url/File: 
%if currentfile!="":
    <input name="stream_path" id="stream_pathid" type="text" placeholder="<Url/File>" autofocus=true value="{{currentfile}}" style="width:90%;min-width: 150px;"/>
%else:
    <input name="stream_path" id="stream_pathid" type="text" placeholder="<Url/File>" autofocus=true style="width:90%;min-width: 150px;"/>
%end
    <input value="Play" type="submit" id="mpv_play" formaction="/start"/>
</form>
</td>

<td>
<table style="border-collapse: collapse; width:100%; border: 1px solid #000000;">
<tr><th style="border-bottom: 1px solid;">Playing:</th></tr>
%if len(playingscreens)>0:
%for screennum, playingfile, hasaudio, isbackground, isloop in playingscreens:
    <tr><td>
        <a href="#" onclick='document.getElementById("screenidid").value={{screennum}}; document.getElementById("screenidid").style="background-color: #00FF00;";document.getElementById("stream_pathid").value="{{playingfile}}"'><b>{{screennum}}</b>: {{playingfile}}</a>
%if not hasaudio:
 mute
%elif isbackground:
 background
%end
%if isloop:
 looped
%end
    </td></tr>
%end
%else:
    <tr><td>No played files</td></tr>
%end
%if currentdir=="":
<tr><th style="border-bottom: 1px solid; border-top: 1px solid;">Files:</th></tr>
%else:
<tr><th style="border-bottom: 1px solid; border-top: 1px solid;">Files in <a href='/index/{{currentdir}}'>{{currentdir}}</a>:</th></tr>
%end
%if len(playfiles)>0:
%for playfile, playaction, realfile in playfiles:
    <tr><td>
        %if playaction == "file":
            <a href="#" onclick='document.getElementById("stream_pathid").value="{{realfile}}"' style="color: #0000FF;">{{playfile}}</a>
        %end
        %if playaction == "dir":
            <a href="/index/{{realfile}}" style="color: #000000;">{{playfile}}</a>
        %end
    </td></tr>
%end
%end
%if len(playfiles)==0 or (len(playfiles)==1 and currentdir!=""):
    <tr><td><b>empty</b></td></tr>
%end

</table>
</td>
</tr>
<table>

</html>
