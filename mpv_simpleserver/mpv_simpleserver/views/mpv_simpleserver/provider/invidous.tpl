<script>
  async function search_invidous(event){
    event.preventDefault();
    req = new Request(`https://www.invidio.us/api/v1/search?q=${event.target.q.value}`, {
        method: 'GET',
        mode: "cors",
    });
    await fetch(req).then(function(response) {console.log(response); return response.json(); })
      .then(function(data) {
      let masterul = document.getElementById("invidous_results");
      while (masterul.firstChild) {
          masterul.removeChild(masterul.firstChild);
      }

      for(let count=0; count<data.length; count++){
        let minorli = document.createElement("li")
        minorli.innerHTML = `<a class="w3-bar-item w3-grey w3-button" onclick='document.getElementById("stream_pathid").value="${data[count].authorUrl}";arguments[0].stopPropagation();'>${data[count].name}</a>`
        masterul.appendChild(minorli);
      }
    })
    return false;
  };
</script>
<div>
  <h3 style="margin-left:10px">Invidious:</h3>
  <hr style="margin: 0 0 5px 0"/>
  <form method="GET" onsubmit="return search_invidous(event)">
    <input name="q" style="margin-left:10px" type="search"><br/>
    <input style="margin-left:10px" type="submit">
  </form>
  <div style="height:350px;overflow: auto;">
    <ul id="invidous_results">
    </ul>
  </div>
</div>
