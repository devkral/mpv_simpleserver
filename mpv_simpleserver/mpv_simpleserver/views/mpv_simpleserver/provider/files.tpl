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
      while (master_index.firstChild) {
          master_index.removeChild(master_index.firstChild);
      }

      for(let count=0; count<data.playfiles.length; count++){
        let minor_index = document.createElement("li")
        if (data.playfiles[count][1] == "dir"){
          minor_index.innerHTML = `<a onclick='return list_dir(event, "${data.playfiles[count][2]}")' style='color: #000000; word-wrap: break-word; cursor: pointer;'>${data.playfiles[count][0]}</a>`
        } else {
          minor_index.innerHTML = `<a onclick='document.getElementById("stream_pathid").value="${data.playfiles[count][2]}";return false' style='color: #0000FF; word-wrap: break-word;cursor: pointer;'>${data.playfiles[count][0]}</a>`
        }
        master_index.appendChild(minor_index);
      }
    })
    return false;
  };
</script>
<div>
  <div style="height:90px">
    <h3 style="margin-left:10px">Files: {{currentdir}}</h3>
    <hr style="margin: 0 0 5px 0"/>
  </div>
  <div style="height:510px; width:100%;overflow-y: auto;">
    <ul class="w3-ul w3-border" id="index_results">
    %for name, playaction, realfile in playfiles:
      <li>
      %if playaction == "file":
        <a href="#" onclick='document.getElementById("stream_pathid").value="{{realfile}}";return false' style="color: #0000FF; word-wrap: break-word;cursor: pointer;">{{name}}</a>
      %end
      %if playaction == "dir":
        <a href="/index/{{realfile}}" onclick='return list_dir(event, "{{realfile}}")' style="color: #000000; word-wrap: break-word;cursor: pointer;">{{name}}</a>
      %end
    </li>
    %end
    </ul>
  </div>
</div>
