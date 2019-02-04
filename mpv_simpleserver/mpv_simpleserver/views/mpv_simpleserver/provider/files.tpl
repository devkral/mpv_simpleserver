<script>
  async function list_dir(event, dirname){
    event.preventDefault();
    req = new Request(`/json/${dirname}`, {
        method: 'GET',
        mode: "same-origin",
    });
    await fetch(req).then(function(response) {return response.json(); })
      .then(function(data) {
      let master_index = document.getElementById("index_results");
      let files_currentdir = document.getElementById("files_currentdir");
      while (master_index.firstChild) {
          master_index.removeChild(master_index.firstChild);
      }
      files_currentdir.innerText = "/"+data.currentdir;

      for(let count=0; count<data.playfiles.length; count++){
        let minor_index = document.createElement("li")
        if (data.playfiles[count][1] == "dir"){
          minor_index.innerHTML = `<a href="/index/${data.playfiles[count][2]}" onclick='return list_dir(event, "${data.playfiles[count][2]}")' style='color: #000000; word-wrap: break-word; cursor: pointer;text-decoration: none;'>${data.playfiles[count][0]}</a>`
        } else if(data.playfiles[count][1] == "file") {
          minor_index.innerHTML = `<a href="#" onclick='document.getElementById("stream_pathid").value="${data.playfiles[count][2]}";return false' style='color: #0000FF; word-wrap: break-word;cursor: pointer;text-decoration: none;'>${data.playfiles[count][0]}</a>`
        }
        master_index.appendChild(minor_index);
      }
    })
    return false;
  };
</script>
<div>
  <div style="height:90px">
    <h3 style="margin-left:10px">Files:</h3>
    <hr style="margin: 0 0 5px 0"/>
    <span id="files_currentdir" style="margin-left:10px;">/{{currentdir}}</span>
  </div>
  <div style="height:510px; width:100%;overflow-y: auto;">
    <ul class="w3-ul w3-border" id="index_results">
    %for name, playaction, realfile in playfiles:
      <li>
      %if playaction == "dir":
        <a href="/index/{{realfile}}" onclick='return list_dir(event, "{{realfile}}")' style="color: #000000; word-wrap: break-word;cursor: pointer;text-decoration: none;">{{name}}</a>
      %elif playaction == "file":
        <a href="#" onclick='document.getElementById("stream_pathid").value="{{realfile}}";return false' style="color: #0000FF; word-wrap: break-word;cursor: pointer;text-decoration: none;">{{name}}</a>
      %end
    </li>
    %end
    </ul>
  </div>
</div>
