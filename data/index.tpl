<html>
<header>
<h1>Mainpage</h1><br/>
</header>
<table style="border-collapse: collapse;"><tr>
<td>
<form method="post">
    Screen: <input name="screenid" id="screenidid" type="number" value="0" max="{{maxscreen}}" min="0" placeholder="<screen>"/>
    <input value="Stop" type="submit" id="mpv_stop" formaction="/stop"/>
    <br>
    Background (quieter) <input name="background" id="backgroundid" type="checkbox"/>
    <br>
    Url/File: <input name="stream_path" id="stream_pathid" type="text" placeholder="<Url/File>" style="width:60%;"/>
    <input value="Play" type="submit" id="mpv_play" formaction="/start"/>
</form>
</td>

<td style="border: 1px solid black; min-width: 150px;">
<table style="border-collapse: collapse;">
<tr>
<th>Playing:</th></tr>
%if len(playingscreens)>0:
%for screennum,playingfile in playingscreens:
    <tr style="border: 1px solid black; min-width: 150px;"><td style="min-width: 150px;">
        <a href="#" onclick='document.getElementById("screenidid").value={{screennum}}; document.getElementById("screenidid").style="background-color:lightgreen;";document.getElementById("stream_pathid").value="{{playingfile}}"'><b>{{screennum}}</b>: {{playingfile}}</a>
    </td></tr>
%end
%end
%if len(playingscreens)==0:
    <tr style="border: 1px solid black;"><td style="min-width: 150px;">
    No played files
    </td></tr>
%end
</table>
</td>
</tr>
<tr>
<td></td>
<td style="border: 1px solid black;">
<table style="border-collapse: collapse; min-width: 150px;">
<tr><th>Files:</th></tr>
%if len(playfiles)>0:
%for playfile, playaction, realfile in playfiles:
    <tr style="border: 1px solid black;"><td style="min-width: 150px;">
        %if playaction == "file":
            <a href="#" onclick='document.getElementById("stream_pathid").value="{{realfile}}"' style="color:blue">{{playfile}}</a>
        %end
        %if playaction == "dir":
            <a href="/index/{{realfile}}" style="color:black">{{playfile}}</a>
        %end
    </td></tr>
%end
%end
%if len(playfiles)==0:
<tr style="border: 1px solid black;"><td style="min-width: 150px;">
empty
</td></tr>
%end
</table>
</td>
</tr>
<table>

</html>
