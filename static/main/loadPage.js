const market_status = document.querySelector('#market-status').textContent
const ws_url = 'wss://' + window.location.host + '/ws/graph/';
const socket = new WebSocket(ws_url);

const ws_url2 = 'wss://' + window.location.host + '/ws/tweet/';
const tweetSocket = new WebSocket(ws_url2);

const waitForOpenConnection = (socket) => {
    return new Promise((resolve, reject) => {
        const maxNumberOfAttempts = 10
        const intervalTime = 200 //ms

        let currentAttempt = 0
        const interval = setInterval(() => {
            if (currentAttempt > maxNumberOfAttempts - 1) {
                clearInterval(interval)
                reject(new Error('Maximum number of attempts exceeded'))
            } else if (socket.readyState === socket.OPEN) {
                clearInterval(interval)
                resolve()
            }
            currentAttempt++
        }, intervalTime)
    })
}

const sendMessage = async (socket, msg) => {
    if (socket.readyState !== socket.OPEN) {
        try {
            await waitForOpenConnection(socket)
            socket.send(msg)
        } catch (err) { console.error(err) }
    } else {
        socket.send(msg)
    }
}

//load appropriate graph on page load, also tweets
$( document ).ready(function() {
    if (document.URL==window.location.origin+'/'){ //loading root URL
        document.querySelector('#stock-selection').selectedIndex = 1
    }else{
        document.querySelector('#data-mode').value = document.URL.split('/').slice(-3)[0]
        document.querySelector('#stock-selection').value = document.URL.split('/').slice(-2)[0]
        document.querySelector('#tweet-count').value = document.URL.split('/').slice(-1)[0]
    }

    var numStocks = document.getElementById("stockList").getElementsByTagName("li").length

    Plotly.newPlot('chart',plotData,layout);
    document.querySelector('.user-select-none.svg-container').firstElementChild.style.background = 'none';
    
    if (numStocks>0){
        message = JSON.stringify({
            'data_mode': document.querySelector('#data-mode').value,
            'stock_select': document.querySelector('#stock-selection').value,
        });
        
        if (market_status=="Closed" && document.querySelector('#data-mode').value=="realTime"){
            document.querySelector('#update-error').style.display = "block";
        }else{
            document.querySelector('#update-error').style.display = "none";
        }
        sendMessage(socket,message);

        //load tweets
        tweet_msg = JSON.stringify({
            'stock_select': '$'+document.querySelector('#stock-selection').value,
            'tweet_count': document.querySelector('#tweet-count').value,
        });
        sendMessage(tweetSocket,tweet_msg);
    }else{
        document.querySelector('#stock-selection').selectedIndex = 0
    }

});