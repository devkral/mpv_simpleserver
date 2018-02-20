<!DOCTYPE html>
<html>
<head>
  <title>Play Music</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link rel="stylesheet" type="text/css" href="static/w3.css"/>
  <style type="text/css">
  @media (min-width:601px){
    .resp-sidebar {
      height: 100%;
      /*width: 200px;*/
      width: 20%;
      right:10px;
      /*bottom: 10px;*/
      background-color: #fff;
      position: fixed !important;
      z-index: 1;
      overflow: hidden;
    }
  }
  .mpvformcontrol {
    border-right: 1px solid #ccc;
    border-bottom: 1px solid #ccc;
    margin-left: 2px;
    margin-right: 2px;
  }
  </style>
</head>
<body class="w3-blue">
  <header class="w3-top w3-bar w3-black">
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
  <div style="margin-top:100px">
    <aside class="w3-bar-block w3-card-4 w3-white w3-mobile resp-sidebar" style="">
      <h2 class="w3-bar-item" style="margin-left: 10px;">Playing:</h2>
      <hr style="margin: 0 0 5px 0"/>
      %for screennum, playingfile, hasaudio, isbackground, isloop in playingscreens:
        <a class="w3-bar-item w3-grey w3-button" onclick='document.getElementById("top-screenselect").value="{{screennum}}"; document.getElementById("content-screenselect").value="{{screennum}}";document.getElementById("stream_pathid").value="{{playingfile}}";arguments[0].stopPropagation();'><b>{{screennum}}</b>: {{playingfile}}
          <small class="">
            %if not hasaudio:
                mute
            %elif isbackground:
                background
            %end
            %if isloop:
                looped
            %end
          </small>
        </a>
      %end
    </aside>
    <main class="w3-white w3-content">
      <h1 style="margin-left: 30px">Enter Music to play:</h1>
      <hr style="margin: 0 0 5px 0"/>
      <div>
        <form class="" method="post">
          %if hidescreens == True:
          <div hidden>
          %end
            Screen: <input name="screenid" id="content-screenselect" class="w3-button onblur="document.getElementById('top-screenselect').value = this.value;" id="screenidid" type="number" value="0" max="{{maxscreens}}" min="0" placeholder="<screen>"/>
          %if hidescreens:
          </div>
          %end
          <div>
          </div>
          <input name="stream_path" id="stream_pathid" type="text" class="w3-input w3-animate-input" placeholder="<Url/File>" autofocus=true value="{{currentfile}}"/>
          <div>
            <input value="Play" class="w3-gray w3-button" type="submit"formaction="/start"/>
            %if len(playingscreens) > 0:
              <input value="Stop" type="submit" class="w3-gray w3-button" formaction="/stop"/>
            %end
            <span style="margin-left: 10px">
              <span class="mpvformcontrol w3-tooltip">
                Background <span class="w3-text w3-white w3-card-4" style="padding:3px;position:absolute;left:0;bottom:30px" ><em>background plays quieter</em></span> <input name="background" class="w3-check" type="checkbox"/>
              </span>
              <span class="mpvformcontrol w3-tooltip">
                Playlist <span class="w3-text w3-white w3-card-4" style="padding:3px;position:absolute;left:0;bottom:30px" ><em>play whole playlist</em></span> <input name="playplaylist" checked="checked" class="w3-check" type="checkbox"/>
              </span>
              <span class="mpvformcontrol w3-tooltip">
                Loop <span class="w3-text w3-white w3-card-4" style="padding:3px;position:absolute;left:0;bottom:30px" ><em>repeat video/playlist</em></span> <input name="loop" class="w3-check" type="checkbox"/>
              </span>
            </span>
          </div>
        </form>
      </div>
      <hr/>
      <div class="w3-row-padding" style="padding-bottom:10px">
        <div class="w3-col s12 l6">
          <div class="w3-card-4" style="height:200px;">
            %include('mpv_simpleserver/provider/files.tpl', **locals())
          </div>
        </div>
        <div class="w3-col s12 l6">
          <div class="w3-card-4" style="height:200px">
            <iframe src="https://youtube.com/embed?listType=search&list=music" style="border:none;" width="100%" height="100%"></iframe>
          </div>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
