<script>
  async function search_invidous(event){
    event.preventDefault();
    let master_invidious = document.getElementById("invidous_results");
    while (master_invidious.firstChild) {
        master_invidious.removeChild(master_invidious.firstChild);
    }
    for(let page=1; page<3; ++page){
      req = new Request(`https://www.invidio.us/api/v1/search?q=${event.target.q.value}&page=${page}`, {
          method: 'GET',
          mode: "cors",
      });
      await fetch(req).then(function(response) {return response.json(); }).then(function(data) {
        for(let count=0; count<data.length; count++){
          let minor_invidious = document.createElement("li")
          if (data[count].type == "video"){
            minor_invidious.innerHTML = `<a href="#" onclick='document.getElementById("stream_pathid").value="https://invidio.us/watch?v=${data[count].videoId}";return false' style='color: #0000FF; word-wrap: break-word;cursor: pointer;text-decoration: none;'>${data[count].title}<small style="margin-left:10px" class="w3-text-grey">${Math.trunc(data[count].lengthSeconds/60)}:${("0" + data[count].lengthSeconds%60).slice(-2)}</small></a>`;
          } else if(data[count].type == "playlist") {
            minor_invidious.innerHTML = `<a href="#" onclick='document.getElementById("stream_pathid").value="https://invidio.us/watch?v=${data[count].playlistId}";return false' style='color: #0000FF; word-wrap: break-word;cursor: pointer;text-decoration: none;'>${data[count].title}<small style="margin-left:10px" class="w3-text-grey">(Playlist)</small></a>`;
          } else {
            continue;
          }
          master_invidious.appendChild(minor_invidious);
        }
      })
    }
    return false;
  };
</script>
<div>
  <div style="height:90px">
    <h3 style="margin-left:10px">Invidious:</h3>
    <hr style="margin: 0 0 5px 0"/>
    <form method="GET" onsubmit="return search_invidous(event)">
      <input name="q" style="margin-left:10px" type="search"><input style="margin-left:10px" type="submit" value="Send"></input>
    </form>
  </div>
  <div style="height:510px; width:100%;overflow-y: auto;">
    <ul id="invidous_results" class="w3-ul w3-border"></ul>
  </div>
</div>
