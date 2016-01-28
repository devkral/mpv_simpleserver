<header>
<h1>Mainpage</h1><br/>
</header>
<table style="border-collapse: collapse;"><tr>
<td>
<form action="/start" method="post">
    Screen: <input name="screenid" id="screenidd" type="number" value="0" max="{{maxscreen}}" min="0" placeholder="<screen>"/>
    Url/File: <input name="fileinp" id="fileinpd" type="text" placeholder="<Url/File>" style="width:60%;"/>
    <br>
    <input value="Play" type="submit" id="mpv_play" formaction="/start"/>
    <input value="Stop" type="submit" id="mpv_stop" formaction="/stop"/>
</form>
</td>

<td style="border: 1px solid black; min-width: 150px;">
<table style="border-collapse: collapse;">
<tr>
<th>Playing:</th></tr>
%if len(playingscreens)>0:
%for screennum,playingfile in playingscreens:
    <tr style="border: 1px solid black; min-width: 150px;"><td style="min-width: 150px;">
        <a href="#" onclick='document.getElementById("screenidd").value={{screennum}}; document.getElementById("screenidd").style="background-color:lightgreen;";document.getElementById("fileinpd").value="{{playingfile}}"'><b>{{screennum}}</b>: {{playingfile}}</a>
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
            <a href="#" onclick='document.getElementById("fileinpd").value="{{realfile}}"' style="color:blue">{{playfile}}</a>
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


