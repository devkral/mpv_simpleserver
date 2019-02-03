<div>
  <h3 style="margin-left:10px">Files: {{currentdir}}</h3>
  <hr style="margin: 0 0 5px 0"/>
  <ul>
  %for playfile, playaction, realfile in playfiles:
    <li class="w3-ul w3-border">
    %if playaction == "file":
      <a href="#" onclick='document.getElementById("stream_pathid").value="{{realfile}}"' style="color: #0000FF; word-wrap: break-word;cursor: pointer;">{{playfile}}</a>
    %end
    %if playaction == "dir":
      <a href="/index/{{realfile}}" style="color: #000000;">{{playfile}}</a>
    %end
  </li>
  %end
</ul>
</div>
