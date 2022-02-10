tweetSocket.onmessage = function(event){
    var data = JSON.parse(event.data);
    var display = document.querySelector('#tweet-feed');
    
    for (let i = 0; i < data.ids.length; i++){
        id = data.ids[i];
        twttr.widgets.createTweet(
            id,
            display,
            {
                theme: 'dark'
            }
        );
    }
}