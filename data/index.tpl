<header>
<h1>Mainpage</h1><br/>
</header>
<table style="border-collapse: collapse;"><tr>
<td>
<form action="/start" method="post">
    Screen: <input name="screenid" id="screenidd" type="number" value="0" max="{{maxscreen}}" min="0" placeholder="<screen>"/>
    Url/File: <input name="fileinp" id="fileinpd" type="text" placeholder="<Url/File>" />
    <input value="Play" type="submit" id="mpv_play" formaction="/start"/>
    <input value="Stop" type="submit" id="mpv_stop" formaction="/stop"/>
</form>
</td>

<td style="border: 1px solid black;">
%if len(playingscreens)>0:
<table style="border-collapse: collapse;">
<tr>
<th>Playing:</th></tr>
%for screennum,playingfile in playingscreens:
    <tr style="border: 1px solid black;"><td>
        <a href="#" onclick='document.getElementById("screenidd").value={{screennum}}; document.getElementById("screenidd").style="background-color:lightgreen;";document.getElementById("fileinpd").value="{{playingfile}}"'><b>{{screennum}}</b>: {{playingfile}}</a>
    </td></tr>
%end
</table>
%end
</td>
</tr>
<tr>
<td></td>
<td style="border: 1px solid black;">
%if len(playfiles)>0:
<table style="border-collapse: collapse;">
<tr><th>Files:</th></tr>
%for playfile in playfiles:
    <tr style="border: 1px solid black;"><td>
        <a href="#" onclick='document.getElementById("fileinpd").value="{{playfile}}"'>{{playfile}}</a>
    </td></tr>
%end
</table>
%end
</td>
</tr>
<table>


