<html>
<header>
<h1>Mainpage</h1><br/>
</header>
<table><tr>
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
    Background (quieter) <input name="background" id="backgroundid" type="checkbox"/>
    <br>
    Url/File: <input name="stream_path" id="stream_pathid" type="text" placeholder="<Url/File>" style="width:100%;min-width: 150px;"/>
    <input value="Play" type="submit" id="mpv_play" formaction="/start"/>
</form>
</td>

<td>
<table style="border-collapse: collapse; width:100%; border: 1px solid #000000;">
<tr><th style="border-bottom: 1px solid;">Playing:</th></tr>
%if len(playingscreens)>0:
%for screennum,playingfile in playingscreens:
    <tr><td>
        <a href="#" onclick='document.getElementById("screenidid").value={{screennum}}; document.getElementById("screenidid").style="background-color: #00FF00;";document.getElementById("stream_pathid").value="{{playingfile}}"'><b>{{screennum}}</b>: {{playingfile}}</a>
    </td></tr>
%end
%else:
    <tr><td>No played files</td></tr>
%end
<tr><th style="border-bottom: 1px solid; border-top: 1px solid;">Files:</th></tr>
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
%else:
    <tr><td>empty</td></tr>
%end

</table>
</td>
</tr>
<table>

</html>
