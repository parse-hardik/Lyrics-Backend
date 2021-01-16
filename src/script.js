const userAction = () =>{
    var inputVal = document.getElementById("myInput").value;
    const res =  fetch('http://localhost:5000/getQuery',{
        method: 'POST',
        body: JSON.stringify({
            query: inputVal,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
        .then(data =>{
            if(data){
                data.result.forEach(async id => {
                    await fetch(`https://api.musixmatch.com/ws/1.1/track.get?format=jsonp&callback=callback&track_id=${id}&apikey=7a65ab716d1257b58c733426e8ee24a1`)
                    .then(function(response) {
                        // The response is a Response instance.
                        // You parse the data into a useable format using `.json()`
                        return response.text();
                      })
                      .then(data => {
                        function callback(data) {
                          console.log(data.message.body.track)
                          let container = document.getElementById("fm");
                          let bapu = data.message.body.track;
                            // for (let i = 1; i <= 10; i++) {
                                let myDiv = document.createElement("div");
                                // myDiv.id
                                myDiv.innerHTML = "<div class=\"wrapper\">"
                                + "<div class=\"song hvr-ripple-out\">" 
                                + "<div class=\"song-text\">" 
                                + "<h1>" + bapu.track_name + "</h1>" 
                                + "<h2>" + bapu.artist_name + "</h2>" 
                                + "<h3>" + bapu.album_name+ "</h3>" 
                                + "</div>" 
                                + "<div class=\"btn\">" 
                                + "<a href=\"" + bapu.track_edit_url + "\">all lyrics</a>" 
                                + "<a href=\"https://www.youtube.com/results?search_query="+bapu.track_name+">view song</a>" 
                                + "</div>" 
                                + "</div>" 
                                + "</div>" 
                                container.append(myDiv);
                        }
                        eval(data)
                        // console.log(data)
                      })
                })
            }
        });
    // console.log(myJson);
}

/*
    <div class="song hvr-ripple-out">
          <div class="song-text">
            <h1>Amaze Song</h1>
            <h2>by Superb Artist</h2>
            <h3>in the wonderful album</h3>
            <p>ye hain gaano ke lyrics</br> lyrics hain ye gaano ke</br>gaano ke lyrics ye hain...</p>
          </div>
          <div class="btn">
            <button type="button">all lyrics</button>
            <button type="button">view song</button>
          </div>
        </div>
*/