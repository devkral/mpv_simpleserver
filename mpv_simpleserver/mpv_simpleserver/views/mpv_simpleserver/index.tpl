<!DOCTYPE html>
<html>
<head>
  <title>Play Music</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link rel="stylesheet" type="text/css" href="static/w3.css"/>
</head>
<body>
  <header class="w3-top w3-bar">
    <h1 class="w3-center">Play Music</h1>
    <span style="position:absolute;top:10px;left:20px">
      <form class="" method="post">
          %if hidescreens == True:
          <span hidden>
          %end
            Screen: <input name="screenid" id="top-screenselect" class="w3-input" onblur="document.getElementById('content-screenselect').value = this.value;" id="screenidid" type="number" value="0" max="{{maxscreens}}" min="0" placeholder="<screen>"/>
          %if hidescreens:
          </span>
          %end
          <input value="Stop" type="submit" class="w3-gray w3-button" formaction="/stop"/>
      </form>
    </span>
  </header>
  <main style="margin-top:100px">
    <table style="width:100%;">
      <tr>
        <td style="width:60%;">
          <form method="post">
            %if hidescreens == True:
            <div hidden>
            %end
              Screen: <input name="screenid" id="content-screenselect" class="w3-button onblur="document.getElementById('top-screenselect').value = this.value;" id="screenidid" type="number" value="0" max="{{maxscreens}}" min="0" placeholder="<screen>"/>
            %if hidescreens:
            </div>
            %end
    %if len(playingscreens) > 0:
        <input value="Stop" type="submit" class="w3-button" id="mpv_stop" formaction="/stop"/>
    %end
        <br>
        Background (quieter) <input name="background" class="w3-check" type="checkbox"/>
        Play Playlist <input name="playplaylist" checked="checked" class="w3-check" type="checkbox"/>
        Loop <input name="loop" class="w3-check" type="checkbox"/>
        <br>
        <input name="stream_path" id="stream_pathid" type="text" class="w3-input w3-animate-input" placeholder="<Url/File>" autofocus=true value="{{currentfile}}"/>
        <input value="Play" class="w3-gray w3-button" type="submit" id="mpv_play" formaction="/start"/>
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
  </main>
</body>
</html>
