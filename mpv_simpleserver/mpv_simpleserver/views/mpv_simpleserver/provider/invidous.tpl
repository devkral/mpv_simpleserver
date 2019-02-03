<script>
  async function search_invidous(event){
    event.preventDefault();
    req = new Request(`https://www.invidio.us/api/v1/search?q=${event.target.q.value}`, {
        method: 'GET',
        mode: "cors",
    });
    await fetch(req).then(function(response) {return response.json(); })
      .then(function(data) {
      let master_invidious = document.getElementById("invidous_results");
      while (master_invidious.firstChild) {
          master_invidious.removeChild(master_invidious.firstChild);
      }

      for(let count=0; count<data.length; count++){
        let minor_invidious = document.createElement("li")
        minor_invidious.innerHTML = `<a class="" onclick='document.getElementById("stream_pathid").value="https://invidio.us/watch?v=${data[count].videoId}";return false' style='color: #0000FF; word-wrap: break-word;cursor: pointer;'>${data[count].title}</a>`
        master_invidious.appendChild(minor_invidious);
      }
    })
    return false;
  };
</script>
<div>
  <h3 style="margin-left:10px">Invidious:</h3>
  <hr style="margin: 0 0 5px 0"/>
  <form method="GET" onsubmit="return search_invidous(event)">
    <input name="q" style="margin-left:10px" type="search"><input style="margin-left:10px" type="submit" value="Send"></input>
  </form>
  <div style="height:500px; width:100%;overflow-y: auto;">
    <ul id="invidous_results" class="w3-ul w3-border"></ul>
  </div>
</div>
