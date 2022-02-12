var cnt = 0;
var limit = 10;

var trace1 = {
    x:[],
    y:[],
    mode: 'lines+markers',
    marker: {
        color: 'yellow',
        size: 8
    },
    line: {
        color: 'yellow',
        width: 2
    },
    name: 'Close'
};
var trace2 = {
    x:[],
    y:[],
    mode: 'lines+markers',
    marker: {
        color: 'red',
        size: 8
    },
    line: {
        color: 'red',
        width: 2
    },
    name: 'Ask'
};
var trace3 = {
    x:[],
    y:[],
    mode: 'lines+markers',
    marker: {
        color: '#1587F2',
        size: 8
    },
    line: {
        color: '#1587F2',
        width: 2
    },
    name: 'Historical'
};

var plotData = [trace1,trace2]
var layout = {
    xaxis: {
        range: [1, limit],
        linecolor: 'black',
        linewidth: 2,
        mirror: true,
        tickfont : {
            size : 16,
            color : plotTickColor,
        }
    },
    yaxis: {
        linecolor: 'black',
        linewidth: 2,
        mirror: true,
        gridcolor: gridColor,
        //title: 'Price (USD)',
        tickformat: '$',
        tickfont : {
            size : 16,
            color : plotTickColor,
        }
    },
    plot_bgcolor: '#444',
    showlegend: true,
    legend: {
        x: 1,
        xanchor: 'right',
        y: 1,
        bgcolor: '#444',
        font: {
            family: 'sans-serif',
            size: 12,
            color: '#FFFFFF'
        },
    },
    title: {
        text: '',
        font: {
            size: 20,
            color: 'white'
        },
    }
};

socket.onmessage = function(event){
    var data = JSON.parse(event.data);
    if (data.data_mode=='realTime'){
        var today = new Date();
        var time = padZero(today.getHours()) + ":" + padZero(today.getMinutes()) + ":" + padZero(today.getSeconds());
        layout.title.text = data.stock_select + ': Real Time Quotes';
        
        if(market_status=="Closed"){
            Plotly.extendTraces('chart',{ 
                x: [[time]],
                y: [[data.close]]
            }, [0], limit);
        }else{
            Plotly.extendTraces('chart',{ 
                x: [[time]],
                y: [[data.ask]]
            }, [1], limit); //keep only [limit] most recent points
        }
        //console.log(time+': '+data.ask.toFixed(2));

    }else{
        processHistorical(data.x_val,data.y_val)
    }
    //document.querySelector('.user-select-none.svg-container').firstElementChild.style.backgroundColor = plotColor;
    document.querySelector('.user-select-none.svg-container').firstElementChild.style.background = 'none';
}

function processHistorical(x_val,y_val){
    trace3.x = x_val
    trace3.y = y_val
    var selection = document.querySelector('#data-mode')
    var data_mode = selection.options[selection.selectedIndex].text
    var stock_select = document.querySelector('#stock-selection').value
    Plotly.newPlot('chart',[trace3],{
        title: {
            text: stock_select + ': ' + data_mode,
            font: {
                size: 20,
                color: 'white'
            },
        },
        xaxis: {
            tickfont: {
                size: 16,
                color: 'white',
            },
            gridcolor: gridColor, 
        },
        yaxis: {
            tickformat: '$',
            tickfont: {
                size: 16,
                color: 'white',
            },
            gridcolor: gridColor, 
        }
    });
}

document.querySelector('#update-btn').addEventListener('click', handleUpdate)

function handleUpdate(){
    var data_mode = document.querySelector('#data-mode').value;
    var stock_select = document.querySelector('#stock-selection').value;
    var tweet_count = document.querySelector('#tweet-count').value;
    if (stock_select=='none'){
        alert('Please select a stock!');
    }else{
        document.getElementById('update-link').href='//'+window.location.host+`/update/${data_mode}/${stock_select}/${tweet_count}`;
    }
}

function padZero(num){
    if (num<10){
        return '0'+String(num)
    }else{
        return String(num)
    }
}
